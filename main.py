from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Configure the database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/post'

# Disable tracking modifications to improve performance
app.config['SQLALCHEMY_TRACK_MODIFICIATIONS'] = False

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    author = db.Column(db.String(50))


    # These arguments represent the initial values you want to assign to the attributes of the Post object being created.
    # Initializes for the new object
    # What it is actually doing : 
        # new_post.title would be 'My Title'
        # new_post.description would be 'Some description'
        # new_post.author would be 'John Doe'

    def __init__(self,title,description,author):
        self.title = title
        self.description = description
        self.author = author
 
# In short,it defines a Marshmallow schema called PostSchema to specify how the data in a Post object should be transformed (serialized) into a simpler format. 
# using marshmallow here , we don't need to validate every objects field 
class PostSchema(ma.Schema):
    class Meta:
        fields = ("title","author","description")


# post_schema = PostSchema(): This line creates an instance of the PostSchema class. This instance can be used to serialize a single Post object into the desired format, according to the schema configuration.
# posts_schema = PostSchema(many=True): This line creates another instance of the PostSchema class, but with the many=True parameter. This indicates that the schema is used to serialize multiple Post objects (a collection of posts) into the desired format.
# 1 obj = 1 --- title , author, description
post_schema = PostSchema()  
posts_schema = PostSchema(many=True) 



@app.route('/get', methods = ['GET'])
def get():
    all_posts = Post.query.all()
    result = posts_schema.dump(all_posts)

    return jsonify(result) 



@app.route('/post_details/<id>', methods = ['GET'])
def post_details(id):
    all_posts = Post.query.get(id)
    result = post_schema.jsonify(all_posts)
    return result 


@app.route('/post_update/<id>', methods = ['PUT'])
def post_update(id):
    post = Post.query.get(id)
    title = request.json['title'] # we'll get here the user entered value
    author = request.json['author']
    description = request.json['description']

    post.title = title # here we update the db value to the user's entered value
    post.author = author
    post.description = description

    db.session.commit()

    return post_schema.jsonify(post)

@app.route('/delete_post/<id>', methods = ['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return post_schema.jsonify(post)



@app.route('/post', methods = ['POST'])
def add_post():
    title = request.json['title']
    author = request.json['author']
    description = request.json['description']

    my_posts = Post( title , author, description)
    db.session.add(my_posts)
    db.session.commit()

    return post_schema.jsonify(my_posts)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)