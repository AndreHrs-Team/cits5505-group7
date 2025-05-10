from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.utils.decorators import admin_required
from app.utils.cache_utils import invalidate_dashboard_cache

# Register a Blueprint for education routes
bp = Blueprint('education', __name__, url_prefix='/education')

# Route: Education main page
@bp.route('/')
@login_required
def render_education_page():
    return render_template('education/education.html', title="Education")

# Route: Handle form submission for adding a new education event
@bp.route('/add-event', methods=['POST'])
@login_required
def add_education_event():
    event_type = request.form.get('event_type')
    event_date = request.form.get('event_date')
    notes = request.form.get('notes')

    # 🔸 You can store the data to the database here
    print("New event submitted:", event_type, event_date, notes)

    # Redirect back to the education page after submission
    return redirect(url_for('education.render_education_page'))
