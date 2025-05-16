from datetime import datetime, timedelta
from app import db
from app.models.goal import Goal
from app.models.user import User
from app.models.activity import Activity
from app.models.weight import Weight
from app.models.sleep import Sleep
from app.models.heart_rate import HeartRate

class GoalService:
    @staticmethod
    def create_goal(user_id, category, target_value, unit, timeframe, start_date, end_date=None, 
                    progress_related=False, progress_baseline=None):
        """Create a new goal for the user"""
        goal = Goal(
            user_id=user_id,
            category=category,
            target_value=target_value,
            unit=unit,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            progress_related=progress_related,
            progress_baseline=progress_baseline
        )
        
        # Set initial current value
        GoalService.update_goal_progress(goal)
        
        db.session.add(goal)
        db.session.commit()
        
        return goal
    
    @staticmethod
    def update_goal_progress(goal):
        """Update the current progress of a goal"""
        user = User.query.get(goal.user_id)
        if not user:
            return
        
        # Calculate current value based on category and timeframe
        if goal.category == 'steps':
            GoalService._update_steps_goal(goal)
        elif goal.category == 'weight':
            GoalService._update_weight_goal(goal)
        elif goal.category == 'sleep':
            GoalService._update_sleep_goal(goal)
        elif goal.category == 'heart_rate':
            GoalService._update_heart_rate_goal(goal)
        
        # Check if goal is completed
        progress = goal.calculate_progress()
        if progress >= 100 and not goal.completed:
            goal.completed = True
            db.session.commit()
    
    @staticmethod
    def _update_steps_goal(goal):
        # First, check if target was met on any day between start_date and end_date
        # Get start and end dates of the goal
        goal_start = goal.start_date
        if not goal_start:
            goal_start = datetime.utcnow().date()
        elif hasattr(goal_start, 'date'):
            goal_start = goal_start.date()
            
        goal_end = goal.end_date
        if not goal_end:
            goal_end = datetime.utcnow().date()
        elif hasattr(goal_end, 'date'):
            goal_end = goal_end.date()
        
        # Ensure goal_start is not after goal_end
        if goal_start > goal_end:
            goal_start = goal_end
        
        # Initialize max steps found in the period
        max_daily_steps = 0
        current_date = datetime.utcnow().date()
        
        # Check each day in the goal period
        current_day = goal_start
        while current_day <= goal_end:
            # Get timeframe for this specific day (based on goal timeframe)
            if goal.timeframe == 'daily':
                day_start = datetime.combine(current_day, datetime.min.time())
                day_end = datetime.combine(current_day, datetime.max.time())
            elif goal.timeframe == 'weekly':
                # Get the week containing this day
                week_start = current_day - timedelta(days=current_day.weekday())
                day_start = datetime.combine(week_start, datetime.min.time())
                day_end = day_start + timedelta(days=7) - timedelta(microseconds=1)
            elif goal.timeframe == 'monthly':
                # Get the month containing this day
                month_start = current_day.replace(day=1)
                day_start = datetime.combine(month_start, datetime.min.time())
                # Get last day of month
                if month_start.month == 12:
                    next_month = month_start.replace(year=month_start.year+1, month=1)
                else:
                    next_month = month_start.replace(month=month_start.month+1)
                day_end = datetime.combine(next_month - timedelta(days=1), datetime.max.time())
            
            # Query activities for this timeframe
            activities = Activity.query.filter(
                Activity.user_id == goal.user_id,
                Activity.timestamp >= day_start,
                Activity.timestamp <= day_end
            ).all()
            
            # Sum steps for this day/period
            daily_steps = 0
            for activity in activities:
                if activity.total_steps is not None and activity.total_steps > 0:
                    daily_steps += activity.total_steps
                elif activity.activity_type == 'steps' and activity.value is not None:
                    daily_steps += int(activity.value)
            
            # Update max steps found
            max_daily_steps = max(max_daily_steps, daily_steps)
            
            # If we're checking today's date, save today's progress
            if current_day == current_date:
                todays_steps = daily_steps
            
            # Check if goal is reached
            if daily_steps >= goal.target_value:
                # Goal reached on this day!
                goal.current_value = daily_steps
                goal.completed = True
                db.session.commit()
                return
            
            # Move to next period based on timeframe
            if goal.timeframe == 'daily':
                current_day += timedelta(days=1)
            elif goal.timeframe == 'weekly':
                current_day += timedelta(days=7)
            elif goal.timeframe == 'monthly':
                # Move to first day of next month
                if current_day.month == 12:
                    current_day = current_day.replace(year=current_day.year+1, month=1, day=1)
                else:
                    current_day = current_day.replace(month=current_day.month+1, day=1)
        
        # If we reach here, goal wasn't completed in any day of the period
        
        # If today is within the goal period, use today's progress
        if goal_start <= current_date <= goal_end:
            # Use today's progress
            goal.current_value = todays_steps
        else:
            # Goal period has passed without completion, use the maximum progress achieved
            goal.current_value = max_daily_steps
        
        # Make sure goal is marked as not completed
        goal.completed = False
        db.session.commit()
    
    @staticmethod
    def _update_weight_goal(goal):
        # For weight, we take the latest weight record
        latest_weight = Weight.query.filter_by(user_id=goal.user_id).order_by(Weight.timestamp.desc()).first()
        
        if latest_weight:
            goal.current_value = latest_weight.value
            db.session.commit()
    
    @staticmethod
    def _update_sleep_goal(goal):
        # Get timeframe dates
        start_date, end_date = GoalService._get_timeframe_dates(goal)
        
        # Query sleep records in timeframe
        sleeps = Sleep.query.filter(
            Sleep.user_id == goal.user_id,
            Sleep.timestamp >= start_date,
            Sleep.timestamp <= end_date
        ).all()
        
        if goal.timeframe == 'daily':
            # Calculate average daily sleep
            if sleeps:
                avg_sleep = sum(sleep.duration or 0 for sleep in sleeps) / len(sleeps)
                goal.current_value = avg_sleep
        else:
            # Sum total sleep over period
            total_sleep = sum(sleep.duration or 0 for sleep in sleeps)
            goal.current_value = total_sleep
        
        db.session.commit()
    
    @staticmethod
    def _update_heart_rate_goal(goal):
        # Get timeframe dates
        start_date, end_date = GoalService._get_timeframe_dates(goal)
        
        # Query heart rate records in timeframe
        heart_rates = HeartRate.query.filter(
            HeartRate.user_id == goal.user_id,
            HeartRate.timestamp >= start_date,
            HeartRate.timestamp <= end_date
        ).all()
        
        if heart_rates:
            # Calculate average heart rate
            avg_hr = sum(hr.value for hr in heart_rates) / len(heart_rates)
            goal.current_value = avg_hr
            db.session.commit()
    
    @staticmethod
    def _get_timeframe_dates(goal):
        """Get the start and end dates based on goal timeframe"""
        # Use the goal's start_date if available, otherwise use today
        if goal.start_date:
            if hasattr(goal.start_date, 'date'):
                reference_date = goal.start_date.date()
            else:
                reference_date = goal.start_date  # Already a date object
        else:
            reference_date = datetime.utcnow().date()
        
        today = datetime.utcnow().date()
        
        # If the goal has an end_date and it's in the past, use that as the reference
        if goal.end_date:
            end_date_value = goal.end_date.date() if hasattr(goal.end_date, 'date') else goal.end_date
            if end_date_value < today:
                reference_date = end_date_value
        
        if goal.timeframe == 'daily':
            start_date = datetime.combine(reference_date, datetime.min.time())
            end_date = datetime.combine(reference_date, datetime.max.time())
        elif goal.timeframe == 'weekly':
            # For weekly goals, find the week that contains the reference date
            week_start = reference_date - timedelta(days=reference_date.weekday())
            start_date = datetime.combine(week_start, datetime.min.time())
            end_date = start_date + timedelta(days=7) - timedelta(microseconds=1)
        elif goal.timeframe == 'monthly':
            # For monthly goals, find the month that contains the reference date
            month_start = reference_date.replace(day=1)
            start_date = datetime.combine(month_start, datetime.min.time())
            # Get last day of month
            if month_start.month == 12:
                next_month = month_start.replace(year=month_start.year+1, month=1)
            else:
                next_month = month_start.replace(month=month_start.month+1)
            end_date = datetime.combine(next_month - timedelta(days=1), datetime.max.time())
        
        # If goal has explicit start_date or end_date, use those as boundaries
        if goal.start_date:
            start_date_obj = goal.start_date if isinstance(goal.start_date, datetime) else datetime.combine(goal.start_date, datetime.min.time())
            if start_date < start_date_obj:
                start_date = start_date_obj
            
        if goal.end_date:
            end_date_obj = goal.end_date if isinstance(goal.end_date, datetime) else datetime.combine(goal.end_date, datetime.max.time())
            if end_date > end_date_obj:
                end_date = end_date_obj
        
        return start_date, end_date 