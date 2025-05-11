import os
from datetime import datetime, timedelta
from collections import defaultdict

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from icalendar import Calendar

from app import db
from app.models.education_event import EducationEvent
from app.forms.education_forms import AddEventForm

bp = Blueprint('education', __name__, url_prefix='/education')


@bp.route('/', methods=['GET'])
@bp.route('/schedule', methods=['GET'])
@login_required
def schedule():
    """
    Render this week’s schedule, list all future events,
    and build 'upcoming_events' for client-side alarms.
    """
    form = AddEventForm()

    # Calculate this week’s bounds (Monday–Sunday)
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week   = start_of_week + timedelta(days=6)

    # Fetch events in the current week
    week_events = (
        EducationEvent.query
        .filter(
            EducationEvent.user_id == current_user.id,
            EducationEvent.date >= start_of_week,
            EducationEvent.date <= end_of_week
        )
        .order_by(EducationEvent.date, EducationEvent.time)
        .all()
    )

    # Group weekly events by day label
    schedule_dict = defaultdict(list)
    for ev in week_events:
        day_label  = ev.date.strftime('%A, %d %B %Y')
        time_label = ev.time.strftime('%H:%M')
        schedule_dict[day_label].append(f"{time_label} {ev.title}")

    # Fetch *all* future events for the Upcoming section & alarms
    all_events = (
        EducationEvent.query
        .filter(EducationEvent.user_id == current_user.id)
        .order_by(EducationEvent.date, EducationEvent.time)
        .all()
    )

    # Build JSON-serializable upcoming_events (only those > now)
    now = datetime.now()
    upcoming_events = []
    for ev in all_events:
        ev_dt = datetime.combine(ev.date, ev.time)
        if ev_dt > now:
            upcoming_events.append({
                "title": ev.title,
                "start": ev_dt.isoformat()
            })

    return render_template(
        'education/schedule.html',
        form=form,
        schedule=schedule_dict,
        events=all_events,
        upcoming_events=upcoming_events
    )


@bp.route('/calendar')
@login_required
def calendar():
    """
    Render a FullCalendar month view populated from DB.
    """
    events = EducationEvent.query.filter_by(user_id=current_user.id).all()
    calendar_data = [
        {
            "title": ev.title,
            "start": datetime.combine(ev.date, ev.time).isoformat()
        }
        for ev in events
    ]
    return render_template(
        'education/calendar.html',
        calendar_data=calendar_data
    )


@bp.route('/add', methods=['POST'])
@login_required
def add_event():
    """
    Handle modal form submission to add a single event.
    """
    form = AddEventForm()
    if form.validate_on_submit():
        new_ev = EducationEvent(
            user_id    = current_user.id,
            title      = form.title.data,
            description= '',
            date       = form.date.data,
            time       = form.time.data,
            notes      = form.notes.data
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
