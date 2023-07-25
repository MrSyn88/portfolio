import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv
from peewee import MySQLDatabase, Model, CharField, TextField, DateTimeField, DoesNotExist, IntegrityError, \
    SqliteDatabase
from playhouse.shortcuts import model_to_dict
import datetime
import hashlib
from hashlib import md5
import re

NAME_PATTERN = r'^[a-zA-Z\s\'\-]+$'
EMAIL_PATTERN = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'

load_dotenv()
app = Flask(__name__, static_url_path='/static')

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
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


class InvalidPostException(Exception):
    "Raised when a post contains an empty field"
    pass


class InvalidNameException(Exception):
    "Raised when a post contains an invalid name"
    pass


class InvalidEmailException(Exception):
    "Raised when a post contains an invalid email"
    pass


mydb.connect()
mydb.create_tables([TimelinePost])


def handle_timeline_post(form):
    "handles POST form data"

    # takes the name, email, and content from the form and
    # sets them to "" if it's empty or nonexistent
    name = form.get("name", "").strip()
    email = form.get("email", "").strip()
    content = form.get("content", "").strip()

    # checks for empty fields
    if name == "" or email == "" or content == "":
        raise InvalidPostException("Empty field")

    # checks for a valid name
    if not re.match(NAME_PATTERN, name, re.U):
        raise InvalidNameException("Invalid name")

    # checks for a valid email
    if not re.match(EMAIL_PATTERN, email, re.U):
        raise InvalidEmailException("Invalid email")

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


def getGrav(email):
    "returns the gravatar link for the given email"
    return ("https://www.gravatar.com/avatar/" + hashlib.md5(email.encode("utf")).hexdigest() + "?s=100")


@app.route('/')
def index():
    try:
        #attempt to render the page
        return render_template('index.html', title="Home", url=os.getenv("URL"))
    except Exception as e:
        # Log the exception for debugging purposes if needed
        print(e)
        # Render the error template
        return render_template('error.html', title="Error", message="An error occurred.")


@app.route('/about')
def about():
    try:
        # attempt to render the page
        return render_template('about.html', title="About", url=os.getenv("URL"))
    except Exception as e:
        # Log the exception for debugging purposes if needed
        print(e)
        # Render the error template
        return render_template('error.html', title="Error", message="An error occurred.")


@app.route('/hobbies')
def hobbies():
    try:
        # attempt to render the page
        return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))
    except Exception as e:
        # Log the exception for debugging purposes if needed
        print(e)
        # Render the error template
        return render_template('error.html', title="Error", message="An error occurred.")


@app.route('/education')
def education():
    try:
        # attempt to render the page
        return render_template('education.html', title="Education", url=os.getenv("URL"))
    except Exception as e:
        # Log the exception for debugging purposes if needed
        print(e)
        # Render the error template
        return render_template('error.html', title="Error", message="An error occurred.")


@app.route('/projects')
def projects():
    try:
        # attempt to render the page
        return render_template('projects.html', title="Projects", url=os.getenv("URL"))
    except Exception as e:
        # Log the exception for debugging purposes if needed
        print(e)
        # Render the error template
        return render_template('error.html', title="Error", message="An error occurred.")


@app.route('/timeline', methods=['GET'])
def timeline():
    try:
        # sort posts and send them into the timeline page on load
        posts = [p for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
        return render_template('timeline.html', title="Timeline", url=os.getenv("URL"), posts=posts, getGrav=getGrav)
    except Exception as e:
        # Log the exception for debugging purposes if needed
        print(e)
        # Render the error template
        return render_template('error.html', title="Error", message="An error occurred.")


@app.route('/timeline', methods=['POST'])
def post_timeline_post():
    try:
        # try to send the POST request
        _ = handle_timeline_post(request.form)
        return jsonify({"message": "Post successful"}), 201

    except InvalidPostException as e:
        return jsonify({"error": str(e)}), 400

    except InvalidNameException as e:
        return jsonify({"error": str(e)}), 400

    except InvalidEmailException as e:
        return jsonify({"error": str(e)}), 400

    except IntegrityError as e:
        return jsonify({"error": "Database integrity error"}), 500

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        # try to send the POST request
        form = request.form.to_dict()
        result = handle_timeline_post(form)
        return jsonify(result), 201

    except InvalidPostException as e:
        return jsonify({'error': str(e)}), 400

    except InvalidNameException as e:
        return jsonify({'error': str(e)}), 400

    except InvalidEmailException as e:
        return jsonify({'error': str(e)}), 400

    except IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    try:
        # try to get the timeline posts
        timeline_posts = [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
        return {'timeline_posts': timeline_posts}

    except Exception as e:
        # Log the exception for debugging purposes if needed
        print(e)
        # Return an error JSON response
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    try:
        # try to delete the post with the post_id
        timeline_post = TimelinePost.get_by_id(post_id)
        timeline_post.delete_instance()
        return jsonify({'message': 'Timeline post deleted successfully'}), 200

    except DoesNotExist:
        return jsonify({'message': 'Timeline post not found'}), 404

    except IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="404", url=os.getenv("URL")), 404
