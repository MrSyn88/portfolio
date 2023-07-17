import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import MySQLDatabase, Model, CharField, TextField, DateTimeField, DoesNotExist
from playhouse.shortcuts import model_to_dict
import datetime
import hashlib
from hashlib import md5

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                        user=os.getenv("MYSQL_USER"),
                        password=os.getenv("MYSQL_PASSWORD"),
                        host=os.getenv("MYSQL_HOST"),
                        port=3306        
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb
        
mydb.connect()
mydb.create_tables([TimelinePost])

def getGrav(string):
    return ("https://www.gravatar.com/avatar/" + hashlib.md5(string.encode("utf")).hexdigest() + "?s=200")

@app.route('/')
def index():
    return render_template('index.html', title="Nicolas Ruiz", url=os.getenv("URL"))


@app.route('/about')
def about():
    return render_template('about.html', title="About", url=os.getenv("URL"))


@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))


@app.route('/education')
def education():
    return render_template('education.html', title="Education", url=os.getenv("URL"))


@app.route('/projects')
def projects():
    return render_template('projects.html', title="Projects", url=os.getenv("URL"))

@app.route('/timeline', methods=['GET'])
def timeline():
    posts = [p for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"), posts=posts, getGrav=getGrav)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="404", url=os.getenv("URL")), 404

@app.route('/timeline', methods=['POST'])
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    
    return jsonify(model_to_dict(timeline_post)), 201

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    try:
        timeline_post = TimelinePost.get_by_id(post_id)
        timeline_post.delete_instance()
        return jsonify({'message': 'Timeline post deleted successfully'}), 200
    except DoesNotExist:
        return jsonify({'message': 'Timeline post not found'}), 404
