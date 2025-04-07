from sqladmin import ModelView
from app.auth.models import User
from app.core.main_admin import register_admin

@register_admin 
class UserAdmin(ModelView, model=User):
    """Admin view for User model."""
    
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    
    column_list = [
        User.id,
        User.email,
        User.is_active,
        User.is_superuser,
        User.is_verified,
        User.first_name,
        User.last_name
    ]
    
    column_searchable_list = [
        User.email,
        User.first_name,
        User.last_name
    ]
    
    column_sortable_list = [
        User.email,
        User.is_active,
        User.is_verified,
        User.is_superuser
    ]
    
    column_details_exclude_list = [
        User.hashed_password
    ]
    
    form_excluded_columns = [
        User.hashed_password
    ]
    
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
