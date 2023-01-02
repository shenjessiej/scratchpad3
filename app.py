from flask import Flask, render_template, jsonify, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from util import generate_random_url

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


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xgxonksytjtkkx:accde567c0f6c53dd5222626bc6bd0166a4b125ef53bdf3f4d9fa7d14816a06e@ec2-34-207-12-160.compute-1.amazonaws.com:5432/df25pccam6jup5'
    
db = SQLAlchemy(app)
app.app_context().push()

class Post(db.Model):
    # Defines the Table Name user
    __tablename__ = "post"

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url_identifier = db.Column(db.String(400), nullable=False)
    code_content = db.Column(db.Text, nullable=False)
    page_title = db.Column(db.String(200), nullable=False)

    def __init__(self, url_identifier, code_content, page_title):
        self.url_identifier = url_identifier
        self.code_content = code_content
        self.page_title = page_title

@app.route('/')
def index():
    # on initial load, open index page to use js to check if url is stored in localstage/cache
    return render_template('index.html')


# when new page is first created / saved
@app.route('/newpage')
def newpage():

    # generate new random url and default code content
    rand_url = generate_random_url()
    code_content = intro 
    page_title = defaulttitle

    # save code content with url identifier into database
    db.session.add(Post(rand_url, code_content, page_title))
    db.session.commit()

    # redirect to page of the new url
    return redirect(url_for('code_page', url_identifier=rand_url))


# when page is first loaded with a url that is in database
@app.route('/<url_identifier>')
def code_page(url_identifier):

    # read post from db using url identifier
    post = Post.query.filter_by(url_identifier=url_identifier).first()
    
    # if post is not in db, then return default text
    #if posts is None:
    #    return render_template('base.html', post=intro, rand_url=url_identifier)
    # else, return the saved text from db
    #else:
    return render_template('base.html', post=post.code_content, title=post.page_title, rand_url=url_identifier)


# on editor change, save code content to db using url identifier
@app.route('/save_content', methods=['POST'])
def save_code_to_db():
    if request.method == "POST":
        url_identifier = request.values.get('url_identifier')
        code_content = request.values.get('code_content')
        page_title = request.values.get('page_title')

        db_parameters = [code_content, url_identifier]

        #initialize the database
        post = Post.query.filter_by(url_identifier=url_identifier).first()
        post.code_content = code_content
        post.page_title = page_title
        db.session.commit()

        return db_parameters


if __name__=="__main__":
    db.create_all()
    app.run(debug=True)
