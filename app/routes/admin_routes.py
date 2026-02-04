


from flask import Blueprint, render_template
from flask_login import login_required
from app.decorators import role_required




admin_bp = Blueprint("admin", __name__)






@admin_bp.route("/admin")
@login_required
@role_required(["admin"])
def admin_dashboard():
    return render_template("admin/dashboard.html")
