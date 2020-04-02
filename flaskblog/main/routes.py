from flask import Blueprint, request, render_template
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home') # add multiple decorators to allow the same function to be accessed via multiple routes
def home():
    page = request.args.get('page', 1, type=int)  # sets default page to 1, and throws error if not an integer
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3, page=page)
    return render_template('home.html', posts=posts)

# homepage is paginated
# access multiple pages via eg http://localhost:5000/home?page=3


@main.route('/about')
def about():
    return render_template('about.html', title='About')



