from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(func):
    """
    Custom admin_required decorator to restrict access to admin panel and all routes related to Admin role.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.user_role != 'Admin':
            flash("You don't have permission to access this resource.", "error")
            return redirect(url_for("main.main_page"))
        return func(*args, **kwargs)
    return decorated_view