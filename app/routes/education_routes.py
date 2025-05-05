from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.forms.education_forms import AddEventForm
from app.models.education_event import EducationEvent
from app import db
from datetime import datetime
import os

bp = Blueprint('education', __name__, url_prefix='/education')


@bp.route('/')
@login_required
def render_education_page():
    form = AddEventForm()

    
    events = EducationEvent.query.filter_by(user_id=current_user.id).order_by(EducationEvent.date.asc()).all()

    
    schedule = {
        "Monday, 6 May 2025": ["09:00 - 11:00 CITS5505", "13:00 - 15:00 GRD110"],
        "Tuesday, 7 May 2025": ["10:00 - 12:00 CITS5508"]
    }

    return render_template(
        'education/education.html',
        title="Education",
        form=form,
        events=events,
        schedule=schedule
    )


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
