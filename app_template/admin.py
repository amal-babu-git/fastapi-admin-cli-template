"""
Admin interface configuration for the ${app_name} app.
"""
from sqladmin import ModelView
from .models import ${model_name}
from app.core.main_admin import register_admin

@register_admin
class ${model_name}Admin(ModelView, model=${model_name}):
    """Admin interface for ${model_name}."""
    
    name = "${model_name}"
    name_plural = "${model_name_plural}"
    icon = "fa-solid fa-list"
    
    column_list = [
        ${model_name}.id,
        # Add your model fields here
        ${model_name}.created_at
    ]
    
    column_searchable_list = [
        # Add your searchable fields here
    ]
    
    column_sortable_list = [
        # Add your sortable fields here
        ${model_name}.created_at,
        ${model_name}.updated_at
    ]
    
    column_filters = [
        # Add your filterable fields here
        ${model_name}.created_at
    ]
    
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
