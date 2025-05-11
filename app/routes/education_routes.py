from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.utils.decorators import admin_required
from app.utils.cache_utils import invalidate_dashboard_cache

bp = Blueprint('education', __name__, url_prefix='/education')


@bp.route('/')
@login_required
def render_education_page():
    return render_template('education/education.html', title="education")

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.forms.education_forms import AddEventForm
from app.models.education_event import EducationEvent
from app import db
from datetime import datetime, timedelta
import os

bp = Blueprint('education', __name__, url_prefix='/education')

@bp.route('/add', methods=['POST'])
@login_required
def add_event():
    form = AddEventForm()
    if form.validate_on_submit():
        event = EducationEvent(
            user_id=current_user.id,
            title=form.title.data,
            description=None,
            date=form.date.data,
            time=form.time.data,
            notes=form.notes.data
        )
        db.session.add(event)
        db.session.commit()
    return redirect(url_for('education.render_education_page'))


@bp.route('/import', methods=['POST'])
@login_required
def import_ics():
    ics_file = request.files.get('ics_file')
    if ics_file and ics_file.filename.endswith('.ics'):
        file_path = os.path.join('uploads', f"{current_user.id}_{ics_file.filename}")
        os.makedirs('uploads', exist_ok=True)
        ics_file.save(file_path)


        print(f".ics file saved to: {file_path}")

    return redirect(url_for('education.render_education_page'))

@bp.route('/', methods=['GET'])
@bp.route('/schedule', methods=['GET'])
@login_required
def schedule():
    """
    Render this week’s schedule, list all future events,
    and build 'upcoming_events' for client-side alarms.
    """
    form = AddEventForm()

    
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    
    week_events = EducationEvent.query.filter(
        EducationEvent.user_id == current_user.id,
        EducationEvent.date >= start_of_week,
        EducationEvent.date <= end_of_week
    ).order_by(EducationEvent.date.asc(), EducationEvent.time.asc()).all()

    
    schedule = {}
    for event in week_events:
        day_str = event.date.strftime('%A, %d %B %Y')
        time_str = event.time.strftime('%H:%M')
        schedule.setdefault(day_str, []).append(f"{time_str} {event.title}")

    
    all_events = EducationEvent.query.filter_by(user_id=current_user.id).order_by(EducationEvent.date.asc()).all()

    return render_template(
        'education/schedule.html',
        form=form,
        schedule=schedule_dict,
        events=all_events,
        upcoming_events=upcoming_events
    )


@bp.route('/calendar')
@login_required
def import_ics():
    ics_file = request.files.get('ics_file')
    if ics_file and ics_file.filename.endswith('.ics'):
        file_path = os.path.join('uploads', f"{current_user.id}_{ics_file.filename}")
        os.makedirs('uploads', exist_ok=True)
        ics_file.save(file_path)

        
        print(f".ics file saved to: {file_path}")

    return redirect(url_for('education.render_education_page'))


@bp.route('/add', methods=['POST'])
@login_required
def add_event():
    """
    Handle modal form submission to add a single event.
    """
    form = AddEventForm()
    if form.validate_on_submit():
        event = EducationEvent(
            user_id=current_user.id,
            title=form.title.data,
            description='',  
            date=form.date.data,
            time=form.time.data,
            notes=form.notes.data
        )
        db.session.add(new_ev)
        db.session.commit()
        flash("Event added successfully.", "success")
    else:
        flash("Failed to add event. Please check your input.", "danger")
    return redirect(url_for('education.schedule'))


@bp.route('/import', methods=['POST'])
@login_required
def import_ics():
    """
    Import a .ics file from CAS into EducationEvent records.
    """
    ics_file = request.files.get('ics_file')
    if not ics_file or not ics_file.filename.lower().endswith('.ics'):
        flash("Please upload a valid .ics file.", "warning")
        return redirect(url_for('education.schedule'))

    # Save upload into instance/uploads/
    upload_dir = os.path.join(current_app.instance_path, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, f"{current_user.id}_{ics_file.filename}")
    ics_file.save(filepath)

    # Parse calendar and create events
    with open(filepath, 'rb') as f:
        cal = Calendar.from_ical(f.read())
        for comp in cal.walk():
            if comp.name == "VEVENT":
                dtstart    = comp.get('dtstart').dt
                event_date = dtstart.date()
                event_time = dtstart.time() if hasattr(dtstart, 'time') else None

                ev = EducationEvent(
                    user_id    = current_user.id,
                    title      = comp.get('summary'),
                    description= comp.get('description'),
                    date       = event_date,
                    time       = event_time,
                    notes      = comp.get('location') or ''
                )
                db.session.add(ev)
        db.session.commit()

    flash("Schedule imported from .ics!", "success")
    return redirect(url_for('education.schedule'))
