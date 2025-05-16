import csv
import io
import json
from datetime import datetime
import zipfile
from app.models.finance.account import Account
from app.models.finance.transaction import Transaction
from app.models.finance.category import Category
from app.models.education_event import EducationEvent

def export_data_to_csv(user, start_date=None, end_date=None):
    """
    Export user data to CSV files (one per data type)
    
    Args:
        user: User object with data to export
        start_date: Optional start date for filtering data
        end_date: Optional end date for filtering data
        
    Returns:
        BytesIO object containing a zip file with CSVs
    """
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w') as zf:
        # Export profile data
        if user:
            profile_data = io.StringIO()
            profile_writer = csv.writer(profile_data)
            
            # Write headers
            profile_writer.writerow([
                'Username', 'Email', 'First Name', 'Last Name', 'Gender', 
                'Birth Date', 'Height (cm)', 'Weight (kg)', 'Created At'
            ])
            
            # Write data
            profile_writer.writerow([
                user.username, 
                user.email,
                user.first_name or '',
                user.last_name or '',
                user.gender or '',
                user.birth_date.strftime('%Y-%m-%d') if user.birth_date else '',
                user.height or '',
                user.weight or '',
                user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else ''
            ])
            
            zf.writestr('profile.csv', profile_data.getvalue())
        
        # Export weight data
        if user.weights.count() > 0:
            weights_data = io.StringIO()
            weights_writer = csv.writer(weights_data)
            
            # Write headers
            weights_writer.writerow(['Date', 'Weight', 'Unit'])
            
            # Write data
            for weight in user.weights:
                # Skip if outside date range
                if (start_date and weight.timestamp.date() < start_date) or \
                   (end_date and weight.timestamp.date() > end_date):
                    continue
                    
                weights_writer.writerow([
                    weight.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    weight.value,
                    weight.unit or 'kg'
                ])
            
            zf.writestr('weights.csv', weights_data.getvalue())
        
        # Export heart rate data
        if user.heart_rates.count() > 0:
            hr_data = io.StringIO()
            hr_writer = csv.writer(hr_data)
            
            # Write headers
            hr_writer.writerow(['Date', 'Heart Rate (bpm)'])
            
            # Write data
            for hr in user.heart_rates:
                # Skip if outside date range
                if (start_date and hr.timestamp.date() < start_date) or \
                   (end_date and hr.timestamp.date() > end_date):
                    continue
                    
                hr_writer.writerow([
                    hr.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    hr.value
                ])
            
            zf.writestr('heart_rates.csv', hr_data.getvalue())
        
        # Export activity data
        if user.activities.count() > 0:
            activity_data = io.StringIO()
            activity_writer = csv.writer(activity_data)
            
            # Write headers
            activity_writer.writerow([
                'Date', 'Steps', 'Distance (km)', 'Calories', 'Activity Type'
            ])
            
            # Process activities by date to get meaningful daily summaries
            daily_activities = {}
            
            for activity in user.activities:
                # Skip if outside date range
                if (start_date and activity.timestamp.date() < start_date) or \
                   (end_date and activity.timestamp.date() > end_date):
                    continue
                
                date_key = activity.timestamp.date()
                if date_key not in daily_activities:
                    daily_activities[date_key] = {
                        'date': activity.timestamp.strftime('%Y-%m-%d'),
                        'steps': 0,
                        'distance': 0,
                        'calories': 0,
                        'activity_types': set()
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
                elif activity.activity_type == 'daily_summary':
                    # Already handled through total_* fields above
                    pass
                
                daily_activities[date_key]['activity_types'].add(activity.activity_type or 'unknown')
            
            # Write daily summary data
            for date, data in sorted(daily_activities.items(), reverse=True):
                activity_writer.writerow([
                    data['date'],
                    data['steps'] or 0,
                    data['distance'] or 0,
                    data['calories'] or 0,
                    ', '.join(data['activity_types'])
                ])
            
            zf.writestr('activities.csv', activity_data.getvalue())
        
        # Export sleep data
        if user.sleeps.count() > 0:
            sleep_data = io.StringIO()
            sleep_writer = csv.writer(sleep_data)
            
            # Write headers
            sleep_writer.writerow([
                'Date', 'Duration (min)', 'Deep Sleep (min)', 'Light Sleep (min)', 
                'REM Sleep (min)', 'Awake (min)', 'Quality', 'Start Time', 'End Time'
            ])
            
            # Write data
            for sleep in user.sleeps:
                # Skip if outside date range
                if (start_date and sleep.timestamp.date() < start_date) or \
                   (end_date and sleep.timestamp.date() > end_date):
                    continue
                    
                sleep_writer.writerow([
                    sleep.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    sleep.duration,
                    sleep.deep_sleep or '',
                    sleep.light_sleep or '',
                    sleep.rem_sleep or '',
                    sleep.awake or '',
                    sleep.quality or '',
                    sleep.start_time.strftime('%Y-%m-%d %H:%M:%S') if sleep.start_time else '',
                    sleep.end_time.strftime('%Y-%m-%d %H:%M:%S') if sleep.end_time else ''
                ])
            
            zf.writestr('sleep.csv', sleep_data.getvalue())
        
        # Export finance data
        if hasattr(user, 'accounts'):
            # Export accounts
            accounts = Account.query.filter_by(user_id=user.id).all()
            
            if accounts:
                accounts_data = io.StringIO()
                accounts_writer = csv.writer(accounts_data)
                
                # Write headers
                accounts_writer.writerow(['ID', 'Name', 'Type', 'Balance', 'Currency', 'Notes', 'Created At'])
                
                # Write data
                for account in accounts:
                    accounts_writer.writerow([
                        account.id,
                        account.name,
                        account.type,
                        account.balance,
                        account.currency or '',
                        account.note or '',
                        account.created_at.strftime('%Y-%m-%d %H:%M:%S') if account.created_at else ''
                    ])
                
                zf.writestr('finance_accounts.csv', accounts_data.getvalue())
            
            # Export transactions
            transactions_query = Transaction.query.filter_by(user_id=user.id)
            if start_date:
                transactions_query = transactions_query.filter(Transaction.date >= start_date)
            if end_date:
                transactions_query = transactions_query.filter(Transaction.date <= end_date)
            transactions = transactions_query.order_by(Transaction.date).all()
            
            if transactions:
                transactions_data = io.StringIO()
                transactions_writer = csv.writer(transactions_data)
                
                # Write headers
                transactions_writer.writerow([
                    'Date', 'Type', 'Account', 'Category', 'Amount', 'Title', 'Note'
                ])
                
                # Write data
                for tx in transactions:
                    transactions_writer.writerow([
                        tx.date.strftime('%Y-%m-%d %H:%M:%S') if tx.date else '',
                        tx.type,
                        tx.account.name if tx.account else '',
                        tx.category.name if tx.category else '',
                        tx.amount,
                        tx.title or '',
                        tx.note or ''
                    ])
                
                zf.writestr('finance_transactions.csv', transactions_data.getvalue())
                
            # Export categories
            categories = Category.query.filter_by(user_id=user.id).all()
            
            if categories:
                categories_data = io.StringIO()
                categories_writer = csv.writer(categories_data)
                
                # Write headers
                categories_writer.writerow(['ID', 'Name', 'Type', 'Created At'])
                
                # Write data
                for category in categories:
                    categories_writer.writerow([
                        category.id,
                        category.name,
                        category.type,
                        category.created_at.strftime('%Y-%m-%d %H:%M:%S') if category.created_at else ''
                    ])
                
                zf.writestr('finance_categories.csv', categories_data.getvalue())
        
        # Export education data
        education_query = EducationEvent.query.filter_by(user_id=user.id)
        if start_date:
            education_query = education_query.filter(EducationEvent.date >= start_date)
        if end_date:
            education_query = education_query.filter(EducationEvent.date <= end_date)
        education_events = education_query.order_by(EducationEvent.date).all()
        
        if education_events:
            education_data = io.StringIO()
            education_writer = csv.writer(education_data)
            
            # Write headers
            education_writer.writerow(['Date', 'Time', 'Title', 'Description', 'Notes'])
            
            # Write data
            for event in education_events:
                education_writer.writerow([
                    event.date.strftime('%Y-%m-%d') if event.date else '',
                    event.time.strftime('%H:%M:%S') if event.time else '',
                    event.title,
                    event.description or '',
                    event.notes or ''
                ])
            
            zf.writestr('education_events.csv', education_data.getvalue())
    
    memory_file.seek(0)
    return memory_file 