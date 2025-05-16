from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import current_user, login_required
from app import db
from app.forms.user_forms import ProfileForm, ChangePasswordForm, AccountSettingsForm, ExportConsentForm
from app.models.user import User
from app.utils.export import export_data_to_csv
from datetime import datetime
import logging
import io
import json

bp = Blueprint('user', __name__, url_prefix='/user')
logger = logging.getLogger(__name__)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    form = ProfileForm()
    
    if request.method == 'GET':
        # Pre-populate form with current data
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.gender.data = current_user.gender
        form.birth_date.data = current_user.birth_date
        form.height.data = current_user.height
        form.weight.data = current_user.weight
    
    if form.validate_on_submit():
        try:
            # Update user profile
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.gender = form.gender.data
            current_user.birth_date = form.birth_date.data
            current_user.height = form.height.data
            current_user.weight = form.weight.data
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.profile'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating profile: {str(e)}", exc_info=True)
            flash('An error occurred while updating your profile.', 'danger')
    
    return render_template('user/profile.html', form=form, title='My Profile')

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        try:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('user.profile'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error changing password: {str(e)}", exc_info=True)
            flash('An error occurred while changing your password.', 'danger')
    
    return render_template('user/change_password.html', form=form, title='Change Password')

@bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """Account settings page"""
    form = AccountSettingsForm()
    
    if request.method == 'GET':
        form.email.data = current_user.email
    
    if form.validate_on_submit():
        try:
            # Check which form was submitted
            if 'submit_email' in request.form and form.confirm_email.data:
                current_user.email = form.email.data
                db.session.commit()
                flash('Email updated successfully!', 'success')
                return redirect(url_for('user.account'))
            
            elif 'submit_delete' in request.form and form.delete_account.data:
                if form.delete_confirmation.data == "DELETE":
                    # Mark account as inactive instead of actually deleting
                    current_user.is_active = False
                    db.session.commit()
                    flash('Your account has been deactivated.', 'info')
                    return redirect(url_for('auth.logout'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating account: {str(e)}", exc_info=True)
            flash('An error occurred while updating your account.', 'danger')
    
    return render_template('user/account.html', form=form, title='Account Settings')

@bp.route('/export_data', methods=['GET', 'POST'])
@login_required
def export_data():
    """Export user data as CSV with consent"""
    form = ExportConsentForm()
    
    if form.validate_on_submit() and form.confirm_export.data:
        try:
            # Get date range if provided
            start_date = form.start_date.data if hasattr(form, 'start_date') and form.start_date.data else None
            end_date = form.end_date.data if hasattr(form, 'end_date') and form.end_date.data else None
            
            memory_file = export_data_to_csv(current_user, start_date, end_date)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return send_file(
                memory_file,
                download_name=f'healthtrack_data_{current_user.username}_{timestamp}.zip',
                as_attachment=True,
                mimetype='application/zip'
            )
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}", exc_info=True)
            flash('An error occurred while exporting your data.', 'danger')
            return redirect(url_for('user.profile'))
    
    return render_template('user/export_consent.html', form=form, title='Export Data')

@bp.route('/export_data/<format>', methods=['GET'])
@login_required
def export_data_format(format):
    """Export user data in specific format"""
    try:
        # Get date range from query parameters if provided
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
        
        if format == 'csv':
            memory_file = export_data_to_csv(current_user, start_date, end_date)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return send_file(
                memory_file,
                download_name=f'healthtrack_data_{current_user.username}_{timestamp}.zip',
                as_attachment=True,
                mimetype='application/zip'
            )
        elif format == 'json':
            # Export as JSON
            data = current_user.export_data(start_date, end_date)
            memory_file = io.BytesIO()
            memory_file.write(json.dumps(data, indent=2).encode('utf-8'))
            memory_file.seek(0)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return send_file(
                memory_file,
                download_name=f'healthtrack_data_{current_user.username}_{timestamp}.json',
                as_attachment=True,
                mimetype='application/json'
            )
        elif format == 'pdf':
            # Redirect to generate PDF report
            return redirect(url_for('user.profile'))
        else:
            flash('Unsupported export format.', 'danger')
            return redirect(url_for('user.export_data'))
    except Exception as e:
        logger.error(f"Error exporting data in format {format}: {str(e)}", exc_info=True)
        flash('An error occurred while exporting your data.', 'danger')
        return redirect(url_for('user.export_data')) 