from flask import flash, redirect, request, url_for, render_template
from app.forms.finance_forms import CategoryForm
from app.services.finance.category_service import CategoryService
from app.models.finance.category import Category

class CategoryController:
    @staticmethod
    def handle_categories_page(current_user, form=None):
        if form is None:
            form = CategoryForm()

        # Pre-populate is_global if editing a global category
        if request.method == 'GET' and form.id.data:
            category = Category.query.get(form.id.data)
            if category:
                form.is_global.data = category.user_id is None

        if form.validate_on_submit():
            # Only allow admin to create/edit global categories
            if form.is_global.data and not current_user.is_admin:
                flash('You do not have permission to create global categories.', 'error')
                return redirect(url_for('finance.render_finance_categories_page'))

            if form.id.data:  # Edit mode
                success, error = CategoryService.update_category(form.id.data, current_user.id, form)
                flash_message = 'Category updated successfully!' if success else f'Error updating category: {error}'
            else:  # Create mode
                success, error = CategoryService.create_category(current_user.id, form)
                flash_message = 'Category created successfully!' if success else f'Error creating category: {error}'
            
            flash(flash_message, 'success' if success else 'error')
            return redirect(url_for('finance.render_finance_categories_page'))

        # Get categories for data table
        categories = CategoryService.get_user_categories(current_user.id)
        
        # Get chart data
        category_stats = CategoryService.get_category_stats(current_user.id)
        chart_data = CategoryController._prepare_chart_data(categories, category_stats)
        
        return render_template('finance/finance_categories.html.j2', 
                            form=form, 
                            categories=categories,
                            chart_data=chart_data,
                            current_user=current_user)
    @staticmethod
    def _prepare_chart_data(categories, category_stats):
        return {
            'labels': [cat.name for cat in categories],
            'sum': [next((stat.sum for stat in category_stats if stat.id == cat.id), 0) 
                   for cat in categories],
            'avg': [next((stat.avg for stat in category_stats if stat.id == cat.id), 0) 
                   for cat in categories],
            'max': [next((stat.max for stat in category_stats if stat.id == cat.id), 0) 
                   for cat in categories],
            'min': [next((stat.min for stat in category_stats if stat.id == cat.id), 0) 
                   for cat in categories],
            'x_label': 'Categories',
            'title': 'Category Activity (Last 28 Days)'
        }