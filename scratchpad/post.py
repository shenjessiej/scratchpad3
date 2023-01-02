from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from scratchpad.db import get_db
from scratchpad.util import generate_random_url

bp = Blueprint('post', __name__)

defaulttitle = "SCRATCHPAD 3: the muppet movie"
intro = """<style>
        body {background: #9bba8f;}
          .container {
            background: #fff;
            padding: 50px;
            margin: 50px auto;
            width: 400px;
            font-family: sans-serif;
            border-radius: 10px;
          }
        </style>
        <div class="container">
            <h1>scratchpad 3</h1>
          <p>Hello! This is a simple web-based live-reload HTML/CSS/JS text editor! You can do code-y things here like in old Scratchpad.<p> 
          <p>NEW: All urls are shareable and editable! Click the '+' at the top right to make a new page! Please keep track of the URLs on your own, as your browser cache will only save the most recently edited one. </p>
         <p>  DM <b>tom nook apologist#7578</b> on discord if you encounter any bugs! 
        </div><br>"""

@bp.route('/', methods=['GET','POST'])
def index():
    # on initial load, open index page to use js to check if url is stored in localstage/cache
    return render_template('index.html')

# when new page is first created / saved
@bp.route('/newpage')
def newpage():

    #initialize the database
    db = get_db()

    # generate new random url and default code content
    rand_url = generate_random_url()
    code_content = intro 
    page_title = defaulttitle

    # save code content with url identifier into database
    db.execute(
        'INSERT INTO post (url_identifier, code_content, page_title) VALUES (?, ?, ?)',
        (rand_url, code_content, page_title)
    )
    db.commit()

    # redirect to page of the new url
    return redirect(url_for('post.code_page', url_identifier=rand_url))

# when page is first loaded with a url that is in database
@bp.route('/<url_identifier>')
def code_page(url_identifier):

    #initialize the database
    db = get_db()

    # read post from db using url identifier
    posts = db.execute(
        'SELECT * FROM post WHERE url_identifier = ?', (url_identifier,)
    ).fetchone()
    
    # if post is not in db, then return default text
    #if posts is None:
    #    return render_template('base.html', post=intro, rand_url=url_identifier)
    # else, return the saved text from db
    #else:
    return render_template('base.html', post=posts[2], title=posts[3], rand_url=url_identifier)

# on editor change, save code content to db using url identifier
@bp.route('/save_content', methods=['POST'])
def save_code_to_db():
    if request.method == "POST":
        url_identifier = request.values.get('url_identifier')
        code_content = request.values.get('code_content')
        page_title = request.values.get('page_title')

        db_parameters = [code_content, url_identifier]

        #initialize the database
        db = get_db()

        db.execute(
            'UPDATE post SET code_content = ?, page_title = ? WHERE url_identifier = ?', 
            (code_content, page_title, url_identifier)
        )
        db.commit()

        return db_parameters
