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
