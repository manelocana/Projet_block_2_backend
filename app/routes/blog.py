

from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.models.post import Post
from app.extensions import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required
from app.forms.blog import BlogForm



blog_bp = Blueprint('blog', __name__)





@blog_bp.route('/blog')
def blog():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('blog/blog.html', posts=posts)


@blog_bp.route('/blog/<int:post_id>')
def blog_article(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog/blog_article.html', post=post)


@blog_bp.route('/blog/new', methods=['GET', 'POST'])
@login_required
def blog_new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form.get('content')
        image_file = request.files.get('image')

        image_filename=None
        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'blog')
            os.makedirs(upload_path, exist_ok=True)
            image_file.save(os.path.join(upload_path, image_filename))
        
        new_post = Post(title=title, content=content, image=image_filename)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog.blog'))
    return render_template('blog/blog_new.html')


@blog_bp.route('/blog/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def blog_edit(post_id):
    post = Post.query.get_or_404(post_id)
    form = BlogForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        # voir si on monte le img
        image_file = request.files.get('image')
        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'blog')
            os.makedirs(upload_path, exist_ok=True)

            # effacer img anncienne
            if post.image:
                old_path = os.path.join(upload_path, post.image)
                if os.path.exists(old_path):
                    os.remove(old_path)

            image_file.save(os.path.join(upload_path, image_filename))
            post.image = image_filename

        db.session.commit()
        return redirect(url_for('blog.blog_article', post_id=post.id))
    return render_template('blog/blog_edit.html', post=post, form=form)


@blog_bp.route('/blog/<int:post_id>/delete', methods=['POST'])
@login_required
def blog_delete(post_id):
    post = Post.query.get_or_404(post_id)

    if post.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'blog', post.image)
        
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('blog.blog'))