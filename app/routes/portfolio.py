from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.models.portfolio import Project
from app.extensions import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required



portfolio_bp = Blueprint('portfolio', __name__)




@portfolio_bp.route('/portfolio/projects/<string:page>')
def portfolio_static_project(page):
    return render_template(f'portfolio/projects/{page}.html')


@portfolio_bp.route('/portfolio')
def portfolio():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template('portfolio/portfolio.html', projects=projects)


@portfolio_bp.route('/portfolio/<int:project_id>')
def portfolio_project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('portfolio/projects/portfolio_project.html', project=project)


@portfolio_bp.route('/portfolio/new', methods=['GET', 'POST'])
@login_required
def portfolio_new():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image_file = request.files.get('image')
        image_filename = None

        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'portfolio')
            os.makedirs(upload_path, exist_ok=True)
            image_file.save(os.path.join(upload_path, image_filename))

        new_project = Project(title=title, description=description, image=image_filename)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('portfolio.portfolio'))
    return render_template('portfolio/portfolio_new.html')


@portfolio_bp.route('/portfolio/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def portfolio_edit(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        image_file = request.files.get('image')

        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'portfolio')
            os.makedirs(upload_path, exist_ok=True)
            image_file.save(os.path.join(upload_path, image_filename))
            project.image = image_filename

        db.session.commit()
        return redirect(url_for('portfolio.portfolio', project_id=project.id))
    return render_template('portfolio/portfolio_edit.html', project=project) 


@portfolio_bp.route('/portfolio/<int:project_id>/delete', methods=['POST'])
@login_required
def portfolio_delete(project_id):
    project = Project.query.get_or_404(project_id)

    if project.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'portfolio', project.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('portfolio.portfolio'))