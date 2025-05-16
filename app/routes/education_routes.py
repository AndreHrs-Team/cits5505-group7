import os
import requests
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from icalendar import Calendar
from dateutil.rrule import rrulestr

from app import db
from app.models.education_event import EducationEvent
from app.forms.education_forms import AddEventForm

bp = Blueprint('education', __name__, url_prefix='/education')


def is_class(ev):
    """Return True for course events (not exams or clubs)."""
    text = (ev.title or '').lower()
    return 'exam' not in text and 'club' not in text


def is_exam(ev):
    """Return True for exam events."""
    text = ((ev.title or '') + ' ' + (ev.notes or '')).lower()
    return 'exam' in text


def is_club(ev):
    """Return True for club events."""
    text = ((ev.title or '') + ' ' + (ev.notes or '')).lower()
    return 'club' in text


@bp.route('/import', methods=['POST'])
@login_required
def import_ics():
    """
    Import a .ics file from either an uploaded file or a URL and expand RRULEs into individual DB rows.
    Old schedule entries for this user will be deleted before importing.
    """
    import_type = request.form.get('import_type')
    cal_data = None
    
    if import_type == 'url':
        # Import from URL
        ics_url = request.form.get('ics_url')
        if not ics_url:
            flash("Please provide a valid ICS URL.", "warning")
            return redirect(url_for('education.schedule'))
            
        try:
            response = requests.get(ics_url)
            if response.status_code != 200:
                flash(f"Failed to download ICS file: HTTP {response.status_code}", "danger")
                return redirect(url_for('education.schedule'))
                
            cal_data = response.content
            
        except Exception as e:
            flash(f"Error downloading ICS file: {str(e)}", "danger")
            return redirect(url_for('education.schedule'))
    else:
        # Import from uploaded file
        ics_file = request.files.get('ics_file')
        if not ics_file or not ics_file.filename.lower().endswith('.ics'):
            flash("Please upload a valid .ics file.", "warning")
            return redirect(url_for('education.schedule'))

        filepath = os.path.join(
            current_app.instance_path,
            'uploads',
            f"{current_user.id}_{ics_file.filename}"
        )
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        ics_file.save(filepath)

        with open(filepath, 'rb') as f:
            cal_data = f.read()

    # Parse the calendar data
    try:
        cal = Calendar.from_ical(cal_data)
    except Exception as e:
        flash(f"Failed to parse ICS data: {str(e)}", "danger")
        return redirect(url_for('education.schedule'))

    # delete old entries
    EducationEvent.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    term_start = datetime(2025, 2, 1, tzinfo=timezone.utc)
    term_end   = datetime(2025, 8, 31, 23, 59, 59, tzinfo=timezone.utc)

    count = 0
    for comp in cal.walk():
        if comp.name != "VEVENT":
            continue

        dtstart_prop = comp.get('dtstart')
        dtstart_raw = dtstart_prop.dt

        # keep dtstart timezone-aware UTC
        if isinstance(dtstart_raw, datetime):
            if dtstart_raw.tzinfo:
                dtstart = dtstart_raw.astimezone(timezone.utc)
            else:
                dtstart = dtstart_raw.replace(tzinfo=timezone.utc)
        else:
            dtstart = datetime.combine(
                dtstart_raw,
                datetime.min.time(),
                tzinfo=timezone.utc
            )

        summary = comp.get('summary')
        desc    = comp.get('description')
        loc     = comp.get('location') or ''

        if comp.get('rrule'):
            ical_lines = comp.to_ical().decode().splitlines()
            rrule_line = next(line for line in ical_lines if line.startswith('RRULE:'))
            rule = rrulestr(rrule_line, dtstart=dtstart)

            for occ in rule.between(term_start, term_end, inc=True):
                ev = EducationEvent(
                    user_id=current_user.id,
                    title=summary,
                    description=desc,
                    date=occ.date(),
                    time=occ.timetz() if hasattr(occ, 'timetz') else occ.time(),
                    notes=loc
                )
                db.session.add(ev)
                count += 1
        else:
            ev = EducationEvent(
                user_id=current_user.id,
                title=summary,
                description=desc,
                date=dtstart.date(),
                time=dtstart.timetz(),
                notes=loc
            )
            db.session.add(ev)
            count += 1

    db.session.commit()
    flash(f"Imported {count} events successfully.", "success")
    return redirect(url_for('education.schedule'))


@bp.route('/add', methods=['POST'])
@login_required
def add_event():
    """
    Handle manual addition of a single event via the AddEventForm.
    """
    form = AddEventForm()
    if form.validate_on_submit():
        ev = EducationEvent(
            user_id=current_user.id,
            title=form.title.data,
            date=form.date.data,
            time=form.time.data,
            notes=getattr(form, 'location', None) and form.location.data or ''
        )
        db.session.add(ev)
        db.session.commit()
        flash("Event added successfully.", "success")
    else:
        for field, errors in form.errors.items():
            for err in errors:
                flash(f"{getattr(form, field).label.text}: {err}", "danger")
    return redirect(url_for('education.schedule'))


@bp.route('/', endpoint='schedule')
@bp.route('/schedule')
@login_required
def schedule():
    """
    Render this week's class schedule plus:
     - all upcoming exams
     - club events in the next 7 days
    """
    form = AddEventForm()

    # 1) This week's lectures
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week   = start_of_week + timedelta(days=6)

    week_events = (
        EducationEvent.query
        .filter(
            EducationEvent.user_id == current_user.id,
            EducationEvent.date.between(start_of_week, end_of_week)
        )
        .order_by(EducationEvent.date, EducationEvent.time)
        .all()
    )

    schedule_dict = defaultdict(list)
    for ev in filter(is_class, week_events):
        label = ev.date.strftime('%A, %d %B %Y')
        time_str = ev.time.strftime('%H:%M')
        schedule_dict[label].append(f"{time_str} {ev.title}")

    # 2) All future events
    all_events = (
        EducationEvent.query
        .filter(EducationEvent.user_id == current_user.id)
        .order_by(EducationEvent.date, EducationEvent.time)
        .all()
    )

    now = datetime.now()
    one_week_later = now + timedelta(days=7)

    # collect exams
    upcoming_exams = [
        {'title': ev.title, 'start': datetime.combine(ev.date, ev.time).isoformat()}
        for ev in all_events
        if is_exam(ev) and datetime.combine(ev.date, ev.time) > now
    ]

    # collect clubs next week
    upcoming_clubs = [
        {'title': ev.title, 'start': datetime.combine(ev.date, ev.time).isoformat()}
        for ev in all_events
        if is_club(ev)
            and now <= datetime.combine(ev.date, ev.time) <= one_week_later
    ]

    upcoming_events = sorted(
        upcoming_exams + upcoming_clubs,
        key=lambda item: item['start']
    )

    return render_template(
        'education/schedule.html',
        form=form,
        schedule=schedule_dict,
        upcoming_events=upcoming_events
    )


@bp.route('/calendar')
@login_required
def calendar():
    """
    Render the full calendar view of all events.
    """
    all_events = (
        EducationEvent.query
        .filter(EducationEvent.user_id == current_user.id)
        .order_by(EducationEvent.date, EducationEvent.time)
        .all()
    )
    events = [
        {'title': ev.title, 'start': datetime.combine(ev.date, ev.time).isoformat()}
        for ev in all_events
    ]
    return render_template(
        'education/calendar.html',
        calendar_data=events
    )
