import os
import tempfile
from datetime import datetime
import json
from flask import current_app, render_template
from weasyprint import HTML, CSS
from app.models import User, SharedLink, Weight, HeartRate, Activity, Sleep, Goal, Achievement, UserAchievement
from app.models.finance.account import Account
from app.models.finance.transaction import Transaction
from app.models.finance.category import Category
from app.models.education_event import EducationEvent

class PDFService:
    """Service for generating PDF reports from shared health data"""
    
    @staticmethod
    def generate_shared_pdf(share_token):
        """Generate a PDF report from a shared link"""
        try:
            # Get shared link
            share_link = SharedLink.query.filter_by(share_token=share_token).first()
            if not share_link or share_link.is_expired():
                raise ValueError("Share link not found or expired")
            
            # Get user
            user = User.query.get(share_link.user_id)
            if not user:
                raise ValueError("User not found")
            
            # Get health data
            data = PDFService._get_shared_data(share_link)
            
            # Determine template based on template_type
            template = f'share/pdf/{share_link.template_type}.html'
            
            # Render HTML template with data
            html_content = render_template(
                template,
                share_link=share_link,
                user=user,
                name=user.get_full_name(),
                data=data,
                generated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            )
            
            # Create temporary file to save PDF
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
                temp_path = temp.name
            
            # Generate PDF from HTML
            HTML(string=html_content).write_pdf(
                temp_path,
                stylesheets=[
                    CSS(string='@page { size: A4; margin: 1cm; }')
                ]
            )
            
            return temp_path
        except Exception as e:
            current_app.logger.error(f"Error generating PDF: {str(e)}")
            raise
    
    @staticmethod
    def _get_shared_data(share_link):
        """Get data for PDF based on shared link settings"""
        # Get user
        user = User.query.get(share_link.user_id)
        
        # Parse modules
        try:
            modules = json.loads(share_link.modules)
        except:
            modules = ["dashboard", "heartrate", "activity", "weight", "sleep", "goals", "achievements"]
        
        # Initialize data dict
        data = {}
        
        # Add data based on modules and privacy level
        if "dashboard" in modules:
            data['dashboard'] = PDFService._get_dashboard_data(user.id, share_link)
        
        if "heartrate" in modules:
            data['heartrate'] = PDFService._get_heartrate_data(user.id, share_link)
            
        if "activity" in modules:
            data['activity'] = PDFService._get_activity_data(user.id, share_link)
            
        if "weight" in modules:
            data['weight'] = PDFService._get_weight_data(user.id, share_link)
            
        if "sleep" in modules:
            data['sleep'] = PDFService._get_sleep_data(user.id, share_link)
            
        if "goals" in modules and share_link.privacy_level != 'achievements':
            data['goals'] = PDFService._get_goals_data(user.id, share_link)
            
        if "achievements" in modules:
            data['achievements'] = PDFService._get_achievements_data(user.id, share_link)
            
        # Add finance and education data if those modules are present
        if "finance" in modules:
            data['finance'] = PDFService._get_finance_data(user.id, share_link)
            
        if "education" in modules:
            data['education'] = PDFService._get_education_data(user.id, share_link)
        
        return data
    
    @staticmethod
    def _get_dashboard_data(user_id, share_link):
        """Get dashboard data for PDF"""
        # Get data
        weights = Weight.query.filter(
            Weight.user_id == user_id,
            Weight.timestamp >= share_link.date_range_start,
            Weight.timestamp <= share_link.date_range_end
        ).order_by(Weight.timestamp.asc()).all()
        
        heart_rates = HeartRate.query.filter(
            HeartRate.user_id == user_id,
            HeartRate.timestamp >= share_link.date_range_start,
            HeartRate.timestamp <= share_link.date_range_end
        ).order_by(HeartRate.timestamp.asc()).all()
        
        activities = Activity.query.filter(
            Activity.user_id == user_id,
            Activity.timestamp >= share_link.date_range_start,
            Activity.timestamp <= share_link.date_range_end
        ).order_by(Activity.timestamp.asc()).all()
        
        sleeps = Sleep.query.filter(
            Sleep.user_id == user_id,
            Sleep.timestamp >= share_link.date_range_start,
            Sleep.timestamp <= share_link.date_range_end
        ).order_by(Sleep.timestamp.asc()).all()
        
        # Process activities to get daily summaries
        daily_activities = {}
        for activity in activities:
            date_key = activity.timestamp.date()
            if date_key not in daily_activities:
                daily_activities[date_key] = {
                    'date': date_key.strftime('%Y-%m-%d'),
                    'steps': 0,
                    'distance': 0,
                    'calories': 0
                }
            
            # Add steps from total_steps field if available
            if activity.total_steps is not None:
                daily_activities[date_key]['steps'] = max(daily_activities[date_key]['steps'], activity.total_steps)
            
            # Add distance from total_distance field if available
            if activity.total_distance is not None:
                daily_activities[date_key]['distance'] = max(daily_activities[date_key]['distance'], activity.total_distance)
            
            # Add calories from calories field if available
            if activity.calories is not None:
                daily_activities[date_key]['calories'] = max(daily_activities[date_key]['calories'], activity.calories)
            
            # Otherwise process by activity_type
            elif activity.activity_type == 'steps' and activity.value is not None:
                daily_activities[date_key]['steps'] += activity.value
            elif activity.activity_type == 'distance' and activity.value is not None:
                daily_activities[date_key]['distance'] += activity.value
            elif activity.activity_type == 'calories' and activity.value is not None:
                daily_activities[date_key]['calories'] += activity.value
        
        # Convert daily activity dict to list - sort by date ascending (small to large)
        activity_summary = [v for k, v in sorted(daily_activities.items())]
        
        # Process data based on privacy level
        if share_link.privacy_level == 'overview':
            # Return only aggregated data
            data = {
                'weights': [{'date': w.timestamp.strftime('%Y-%m-%d'), 'value': w.value, 'unit': w.unit} for w in weights[:7]],
                'heart_rates': [{'date': hr.timestamp.strftime('%Y-%m-%d'), 'value': hr.value, 'unit': hr.unit} for hr in heart_rates[:7]],
                'activities': activity_summary[:7],
                'sleeps': [{'date': s.timestamp.strftime('%Y-%m-%d'), 'duration': s.duration / 60} for s in sleeps[:7]],
                'summary': {
                    'weight': {'latest': weights[-1].value if weights else 0},
                    'heart_rate': {
                        'min': min([hr.value for hr in heart_rates]) if heart_rates else 0,
                        'max': max([hr.value for hr in heart_rates]) if heart_rates else 0,
                        'avg': sum([hr.value for hr in heart_rates]) / len(heart_rates) if heart_rates else 0
                    },
                    'activity': {
                        'avg_steps': sum([a['steps'] for a in activity_summary]) / len(activity_summary) if activity_summary else 0,
                        'total_steps': sum([a['steps'] for a in activity_summary]) if activity_summary else 0
                    },
                    'sleep': {
                        'avg_duration_hours': sum([s.duration for s in sleeps]) / len(sleeps) / 60 if sleeps else 0
                    }
                }
            }
        else:  # complete
            # Return all data
            data = {
                'weights': [w.to_dict() for w in weights],
                'heart_rates': [hr.to_dict() for hr in heart_rates],
                'activities': activity_summary,
                'sleeps': [s.to_dict() for s in sleeps],
                'summary': {
                    'weight': {'latest': weights[-1].value if weights else 0},
                    'heart_rate': {
                        'min': min([hr.value for hr in heart_rates]) if heart_rates else 0,
                        'max': max([hr.value for hr in heart_rates]) if heart_rates else 0,
                        'avg': sum([hr.value for hr in heart_rates]) / len(heart_rates) if heart_rates else 0
                    },
                    'activity': {
                        'avg_steps': sum([a['steps'] for a in activity_summary]) / len(activity_summary) if activity_summary else 0,
                        'total_steps': sum([a['steps'] for a in activity_summary]) if activity_summary else 0
                    },
                    'sleep': {
                        'avg_duration_hours': sum([s.duration for s in sleeps]) / len(sleeps) / 60 if sleeps else 0
                    }
                }
            }
        
        return data
    
    # Helper methods for other data types (similar to the API endpoints)
    @staticmethod
    def _get_heartrate_data(user_id, share_link):
        heart_rates = HeartRate.query.filter(
            HeartRate.user_id == user_id,
            HeartRate.timestamp >= share_link.date_range_start,
            HeartRate.timestamp <= share_link.date_range_end
        ).order_by(HeartRate.timestamp.asc()).all()
        
        if not heart_rates:
            return []
            
        # Group heart rates by day
        from collections import defaultdict
        daily_heart_rates = defaultdict(list)
        
        for hr in heart_rates:
            date_key = hr.timestamp.strftime('%Y-%m-%d')
            daily_heart_rates[date_key].append(hr)
            
        # Calculate daily stats
        heart_rate_data = []
        for date_key, hrs in sorted(daily_heart_rates.items()):
            values = [hr.value for hr in hrs if hr.value is not None]
            if values:
                heart_rate_data.append({
                    'date': date_key,
                    'value': round(sum(values) / len(values)),  # average value
                    'min': min(values),
                    'max': max(values),
                    'count': len(values),
                    'unit': hrs[0].unit
                })
        
        if share_link.privacy_level == 'overview':
            return heart_rate_data[:14]
        else:  # complete
            return heart_rate_data
    
    @staticmethod
    def _get_activity_data(user_id, share_link):
        activities = Activity.query.filter(
            Activity.user_id == user_id,
            Activity.timestamp >= share_link.date_range_start,
            Activity.timestamp <= share_link.date_range_end
        ).order_by(Activity.timestamp.asc()).all()
        
        # Process activities to get daily summaries
        daily_activities = {}
        for activity in activities:
            date_key = activity.timestamp.date()
            if date_key not in daily_activities:
                daily_activities[date_key] = {
                    'date': date_key.strftime('%Y-%m-%d'),
                    'steps': 0,
                    'distance': 0,
                    'calories': 0
                }
            
            # Add steps from total_steps field if available
            if activity.total_steps is not None:
                daily_activities[date_key]['steps'] = max(daily_activities[date_key]['steps'], activity.total_steps)
            
            # Add distance from total_distance field if available
            if activity.total_distance is not None:
                daily_activities[date_key]['distance'] = max(daily_activities[date_key]['distance'], activity.total_distance)
            
            # Add calories from calories field if available
            if activity.calories is not None:
                daily_activities[date_key]['calories'] = max(daily_activities[date_key]['calories'], activity.calories)
            
            # Otherwise process by activity_type
            elif activity.activity_type == 'steps' and activity.value is not None:
                daily_activities[date_key]['steps'] += activity.value
            elif activity.activity_type == 'distance' and activity.value is not None:
                daily_activities[date_key]['distance'] += activity.value
            elif activity.activity_type == 'calories' and activity.value is not None:
                daily_activities[date_key]['calories'] += activity.value
        
        # Convert daily activity dict to list - sort by date ascending (small to large)
        activity_summary = [v for k, v in sorted(daily_activities.items())]
        
        if share_link.privacy_level == 'overview':
            return activity_summary[:14]
        else:  # complete
            return activity_summary
    
    @staticmethod
    def _get_weight_data(user_id, share_link):
        weights = Weight.query.filter(
            Weight.user_id == user_id,
            Weight.timestamp >= share_link.date_range_start,
            Weight.timestamp <= share_link.date_range_end
        ).order_by(Weight.timestamp.asc()).all()
        
        if share_link.privacy_level == 'overview':
            return [{'date': w.timestamp.strftime('%Y-%m-%d'), 'value': w.value, 'unit': w.unit} for w in weights[:14]]
        else:  # complete
            return [w.to_dict() for w in weights]
    
    @staticmethod
    def _get_sleep_data(user_id, share_link):
        sleeps = Sleep.query.filter(
            Sleep.user_id == user_id,
            Sleep.timestamp >= share_link.date_range_start,
            Sleep.timestamp <= share_link.date_range_end
        ).order_by(Sleep.timestamp.asc()).all()
        
        if share_link.privacy_level == 'overview':
            return [{'date': s.timestamp.strftime('%Y-%m-%d'), 'duration': s.duration / 60} for s in sleeps[:14]]
        else:  # complete
            return [s.to_dict() for s in sleeps]
    
    @staticmethod
    def _get_goals_data(user_id, share_link):
        goals = Goal.query.filter(
            Goal.user_id == user_id,
            Goal.created_at >= share_link.date_range_start,
            Goal.created_at <= share_link.date_range_end
        ).order_by(Goal.created_at.asc()).all()
        
        return [g.to_dict() for g in goals]
    
    @staticmethod
    def _get_achievements_data(user_id, share_link):
        user_achievements = UserAchievement.query.filter(
            UserAchievement.user_id == user_id,
            UserAchievement.earned_at >= share_link.date_range_start,
            UserAchievement.earned_at <= share_link.date_range_end
        ).order_by(UserAchievement.earned_at.asc()).all()
        
        achievements = []
        for ua in user_achievements:
            achievement = Achievement.query.get(ua.achievement_id)
            if achievement:
                achievement_dict = achievement.to_dict()
                achievement_dict['earned_at'] = ua.earned_at.isoformat()
                achievements.append(achievement_dict)
        
        return achievements
        
    @staticmethod
    def _get_finance_data(user_id, share_link):
        """Get finance data for PDF"""
        # Get all accounts
        accounts = Account.query.filter_by(user_id=user_id).all()
        
        # Get transactions within date range
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= share_link.date_range_start,
            Transaction.date <= share_link.date_range_end
        ).order_by(Transaction.date.asc()).all()
        
        # Get all categories
        categories = Category.query.filter_by(user_id=user_id).all()
        
        return {
            'accounts': [a.to_dict() for a in accounts],
            'transactions': [t.to_dict() for t in transactions],
            'categories': [c.to_dict() for c in categories]
        }
    
    @staticmethod
    def _get_education_data(user_id, share_link):
        """Get education event data for PDF"""
        # Get education events within date range
        education_events = EducationEvent.query.filter(
            EducationEvent.user_id == user_id,
            EducationEvent.date >= share_link.date_range_start,
            EducationEvent.date <= share_link.date_range_end
        ).order_by(EducationEvent.date.asc()).all()
        
        return [
            {
                'id': e.id,
                'title': e.title,
                'description': e.description,
                'date': e.date.strftime('%Y-%m-%d'),
                'time': e.time.strftime('%H:%M') if e.time else None,
                'notes': e.notes
            }
            for e in education_events
        ] 