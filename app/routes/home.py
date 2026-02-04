from flask import Blueprint, render_template
from app.models.portfolio import Project
from app.models.post import Post


home_bp = Blueprint('home', __name__)



def get_projects():
    return Project.query.order_by(Project.id.desc()).all()

def get_posts(limit=3):
    return Post.query.order_by(Post.id.desc()).limit(limit).all()


@home_bp.route('/')
def home():
    projects = get_projects()
    posts = get_posts()
    return render_template('home.html', projects=projects, posts=posts, title='Home')