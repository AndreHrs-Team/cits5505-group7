from datetime import datetime, timedelta
from app import db
from app.models.achievement import Achievement, UserAchievement
from app.models.user import User
from app.models.activity import Activity
from app.models.weight import Weight
from app.models.sleep import Sleep
from app.models.heart_rate import HeartRate
from app.models.goal import Goal
from flask import flash
from sqlalchemy import func

def check_achievements_for_user(user_id):
    """Check all achievements for a user"""
    user = User.query.get(user_id)
    if not user:
        return []
    
    earned_achievements = []
    
    # Get all achievements
    achievements = Achievement.query.all()
    
    # Get user's already earned achievements
    earned_ids = [ua.achievement_id for ua in UserAchievement.query.filter_by(user_id=user_id).all()]
    
    # Check each achievement
    for achievement in achievements:
        # Skip if already earned
        if achievement.id in earned_ids:
            continue
        
        # Check achievement based on type
        earned = False
        
        if achievement.category == 'steps':
            earned = check_steps_achievement(user, achievement)
        elif achievement.category == 'weight':
            earned = check_weight_achievement(user, achievement)
        elif achievement.category == 'sleep':
            earned = check_sleep_achievement(user, achievement)
        elif achievement.category == 'heart_rate':
            earned = check_heart_rate_achievement(user, achievement)
        elif achievement.category == 'general':
            earned = check_general_achievement(user, achievement)
        
        # If earned, add to database
        if earned:
            user_achievement = UserAchievement(
                user_id=user_id,
                achievement_id=achievement.id
            )
            db.session.add(user_achievement)
            earned_achievements.append(achievement)
    
    if earned_achievements:
        db.session.commit()
    
    return earned_achievements

def check_achievements_for_goal(user_id, goal):
    """Check achievements related to goal completion"""
    user = User.query.get(user_id)
    if not user:
        return []
    
    earned_achievements = []
    
    # Get goal-related achievements for this category
    achievements = Achievement.query.filter_by(
        goal_related=True,
        category=goal.category
    ).all()
    
    # Get user's already earned achievements
    earned_ids = [ua.achievement_id for ua in UserAchievement.query.filter_by(user_id=user_id).all()]
    
    # Check each achievement
    for achievement in achievements:
        # Skip if already earned
        if achievement.id in earned_ids:
            continue
        
        # Check if goal completion triggers this achievement
        earned = False
        
        # Example: Milestone achievement for completing a goal
        if achievement.condition_type == 'milestone' and goal.completed:
            # Check if the goal's target meets the achievement condition
            if goal.target_value >= achievement.condition_value:
                earned = True
        
        # Example: Streak achievement for completing multiple goals
        elif achievement.condition_type == 'streak':
            # Count completed goals in category
            completed_count = Goal.query.filter_by(
                user_id=user_id,
                category=goal.category,
                completed=True
            ).count()
            
            if completed_count >= achievement.condition_value:
                earned = True
        
        # If earned, add to database
        if earned:
            user_achievement = UserAchievement(
                user_id=user_id,
                achievement_id=achievement.id
            )
            db.session.add(user_achievement)
            earned_achievements.append(achievement)
    
    if earned_achievements:
        db.session.commit()
        
        # Flash messages for earned achievements
        for achievement in earned_achievements:
            flash(f'Achievement unlocked: {achievement.name}', 'success')
    
    return earned_achievements

def check_steps_achievement(user, achievement):
    """Check if user has earned a steps-related achievement"""
    if achievement.condition_type == 'milestone':
        # 按天分组，统计每天总步数（只统计 activity_type='steps'）
        daily_steps = db.session.query(
            func.date(Activity.timestamp),
            func.sum(Activity.value)
        ).filter(
            Activity.user_id == user.id,
            Activity.activity_type == 'steps',
            Activity.value != None
        ).group_by(func.date(Activity.timestamp)).all()
        max_steps = max((s[1] or 0) for s in daily_steps) if daily_steps else 0
        return max_steps >= achievement.condition_value

    elif achievement.condition_type == 'streak':
        # streak: 连续N天每天都达标
        daily_steps = db.session.query(
            func.date(Activity.timestamp),
            func.sum(Activity.value)
        ).filter(
            Activity.user_id == user.id,
            Activity.activity_type == 'steps',
            Activity.value != None
        ).group_by(func.date(Activity.timestamp)).all()
        if not daily_steps:
            return False
        # 构建日期到步数的映射
        steps_by_date = {datetime.strptime(str(row[0]), '%Y-%m-%d').date(): row[1] or 0 for row in daily_steps}
        sorted_dates = sorted(steps_by_date.keys())
        streak_days = int(achievement.condition_value)
        for i in range(len(sorted_dates) - streak_days + 1):
            if all(steps_by_date.get(sorted_dates[i + j], 0) >= 5000 for j in range(streak_days)):
                return True
        return False
    return False

def check_weight_achievement(user, achievement):
    """Check if user has earned a weight-related achievement"""
    weights = Weight.query.filter_by(user_id=user.id).order_by(Weight.timestamp).all()
    if not weights:
        return False
    if achievement.condition_type == 'milestone':
        # milestone: e.g. 记录第一次体重
        return len(weights) >= achievement.condition_value
    elif achievement.condition_type == 'improvement':
        # improvement: e.g. 体重变化
        first_weight = weights[0].value
        latest_weight = weights[-1].value
        difference = abs(latest_weight - first_weight)
        return difference >= achievement.condition_value
    elif achievement.condition_type == 'streak':
        # streak: 连续打卡
        streak_days = int(achievement.condition_value)
        dates = set(w.timestamp.date() for w in weights if w.timestamp)
        if not dates:
            return False
        sorted_dates = sorted(dates)
        for i in range(len(sorted_dates) - streak_days + 1):
            if all(sorted_dates[i + j] == sorted_dates[i] + timedelta(days=j) for j in range(streak_days)):
                return True
        return False
    return False

def check_sleep_achievement(user, achievement):
    """Check if user has earned a sleep-related achievement"""
    sleeps = Sleep.query.filter_by(user_id=user.id).all()
    if not sleeps:
        return False
    if achievement.condition_type == 'milestone':
        # milestone: 记录第一次睡眠
        return len(sleeps) >= achievement.condition_value
    elif achievement.condition_type == 'streak':
        # streak: 连续打卡
        streak_days = int(achievement.condition_value)
        dates = set(s.timestamp.date() for s in sleeps if s.timestamp)
        if not dates:
            return False
        sorted_dates = sorted(dates)
        for i in range(len(sorted_dates) - streak_days + 1):
            if all(sorted_dates[i + j] == sorted_dates[i] + timedelta(days=j) for j in range(streak_days)):
                return True
        return False
    return False

def check_heart_rate_achievement(user, achievement):
    """Check if user has earned a heart-rate-related achievement"""
    heart_rates = HeartRate.query.filter_by(user_id=user.id).all()
    if not heart_rates:
        return False
    if achievement.condition_type == 'milestone':
        # milestone: 记录第一次心率
        return len(heart_rates) >= achievement.condition_value
    elif achievement.condition_type == 'streak':
        # streak: 连续打卡
        streak_days = int(achievement.condition_value)
        dates = set(hr.timestamp.date() for hr in heart_rates if hr.timestamp)
        if not dates:
            return False
        sorted_dates = sorted(dates)
        for i in range(len(sorted_dates) - streak_days + 1):
            if all(sorted_dates[i + j] == sorted_dates[i] + timedelta(days=j) for j in range(streak_days)):
                return True
        return False
    elif achievement.condition_type == 'improvement':
        # improvement: 比较历史平均心率
        if len(heart_rates) < 2:
            return False
        old_avg = sum(hr.value for hr in heart_rates[:-1]) / (len(heart_rates) - 1)
        recent = heart_rates[-1]
        improvement = old_avg - recent.value
        return improvement >= achievement.condition_value
    return False

def check_general_achievement(user, achievement):
    """Check general achievements like app usage"""
    if achievement.condition_type == 'milestone':
        # milestone: 例如所有类别都打卡
        steps_count = Activity.query.filter_by(user_id=user.id).count()
        weight_count = Weight.query.filter_by(user_id=user.id).count()
        sleep_count = Sleep.query.filter_by(user_id=user.id).count()
        heart_rate_count = HeartRate.query.filter_by(user_id=user.id).count()
        total_data_points = steps_count + weight_count + sleep_count + heart_rate_count
        return total_data_points >= achievement.condition_value
    elif achievement.condition_type == 'goal':
        # goal: 各类别都设置目标
        goal_categories = set(g.category for g in Goal.query.filter_by(user_id=user.id).all())
        return {'steps', 'weight', 'sleep', 'heart_rate'}.issubset(goal_categories)
    return False 