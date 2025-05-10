from app import db
from app.models.achievement import Achievement

def init_achievements():
    """Initialize predefined achievements"""
    achievements = [
        # Steps Achievements
        {
            'name': 'First Steps',
            'description': 'Record your first 1,000 steps',
            'category': 'steps',
            'icon': 'walking',
            'level': 'bronze',
            'condition_type': 'milestone',
            'condition_value': 1000,
            'trigger_type': 'progress'
        },
        {
            'name': 'Daily Walker',
            'description': 'Reach 5,000 steps in a day',
            'category': 'steps',
            'icon': 'shoe-prints',
            'level': 'silver',
            'condition_type': 'milestone',
            'condition_value': 5000,
            'trigger_type': 'progress'
        },
        {
            'name': 'Power Walker',
            'description': 'Reach 10,000 steps in a day',
            'category': 'steps',
            'icon': 'person-walking',
            'level': 'gold',
            'condition_type': 'milestone',
            'condition_value': 10000,
            'trigger_type': 'progress'
        },
        
        # Weight Achievements
        {
            'name': 'Weight Tracker',
            'description': 'Record your first weight measurement',
            'category': 'weight',
            'icon': 'weight',
            'level': 'bronze',
            'condition_type': 'milestone',
            'condition_value': 1,
            'trigger_type': 'progress'
        },
        {
            'name': 'Weight Goal Setter',
            'description': 'Set your first weight goal',
            'category': 'weight',
            'icon': 'bullseye',
            'level': 'silver',
            'condition_type': 'goal',
            'condition_value': 1,
            'trigger_type': 'goal'
        },
        {
            'name': 'Weight Goal Achiever',
            'description': 'Achieve your first weight goal',
            'category': 'weight',
            'icon': 'trophy',
            'level': 'gold',
            'condition_type': 'goal',
            'condition_value': 1,
            'trigger_type': 'goal'
        },
        
        # Heart Rate Achievements
        {
            'name': 'Heart Monitor',
            'description': 'Record your first heart rate measurement',
            'category': 'heart_rate',
            'icon': 'heart-pulse',
            'level': 'bronze',
            'condition_type': 'milestone',
            'condition_value': 1,
            'trigger_type': 'progress'
        },
        {
            'name': 'Heart Rate Explorer',
            'description': 'Record heart rate for 7 consecutive days',
            'category': 'heart_rate',
            'icon': 'heart',
            'level': 'silver',
            'condition_type': 'streak',
            'condition_value': 7,
            'trigger_type': 'progress'
        },
        {
            'name': 'Heart Rate Master',
            'description': 'Record heart rate for 30 consecutive days',
            'category': 'heart_rate',
            'icon': 'heart-circle',
            'level': 'gold',
            'condition_type': 'streak',
            'condition_value': 30,
            'trigger_type': 'progress'
        },
        
        # Sleep Achievements
        {
            'name': 'Sleep Tracker',
            'description': 'Record your first sleep data',
            'category': 'sleep',
            'icon': 'moon',
            'level': 'bronze',
            'condition_type': 'milestone',
            'condition_value': 1,
            'trigger_type': 'progress'
        },
        {
            'name': 'Sleep Regular',
            'description': 'Record sleep for 7 consecutive days',
            'category': 'sleep',
            'icon': 'bed',
            'level': 'silver',
            'condition_type': 'streak',
            'condition_value': 7,
            'trigger_type': 'progress'
        },
        {
            'name': 'Sleep Expert',
            'description': 'Record sleep for 30 consecutive days',
            'category': 'sleep',
            'icon': 'stars',
            'level': 'gold',
            'condition_type': 'streak',
            'condition_value': 30,
            'trigger_type': 'progress'
        },
        
        # General Achievements
        {
            'name': 'Data Enthusiast',
            'description': 'Record data in all categories (weight, heart rate, steps, sleep)',
            'category': 'general',
            'icon': 'chart-line',
            'level': 'bronze',
            'condition_type': 'milestone',
            'condition_value': 1,
            'trigger_type': 'combined'
        },
        {
            'name': 'Goal Setter',
            'description': 'Set goals in all categories',
            'category': 'general',
            'icon': 'list-check',
            'level': 'silver',
            'condition_type': 'goal',
            'condition_value': 1,
            'trigger_type': 'goal'
        },
        {
            'name': 'Goal Master',
            'description': 'Achieve goals in all categories',
            'category': 'general',
            'icon': 'crown',
            'level': 'gold',
            'condition_type': 'goal',
            'condition_value': 1,
            'trigger_type': 'goal'
        }
    ]
    
    # Add achievements to database
    for achievement_data in achievements:
        # Check if achievement already exists
        existing = Achievement.query.filter_by(name=achievement_data['name']).first()
        if not existing:
            achievement = Achievement(**achievement_data)
            db.session.add(achievement)
    
    try:
        db.session.commit()
        print("Achievements initialized successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing achievements: {str(e)}") 