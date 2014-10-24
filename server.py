from flask import Flask, render_template, Response, jsonify
import json
import urllib2
import os
app = Flask(__name__)


@app.route("/")
def get_home():
	return render_template('home.html')


@app.route("/feed/")
def get_feed():
	data = urllib2.urlopen('http://api.alexrecker.com/post/feed/')
	res = data.read()
	data.close()
	return Response(res, mimetype='text/xml')


@app.route("/<slug>/")
def get_slug(slug):
	return render_template('post.html', slug=slug)


def serialize_post(post):
	return {
		"title": post.title,
		"link": post.link,
		"date": post.date,
		"description": post.description,
		"image": post.image,
	}


if __name__ == "__main__":
    app.run(debug=True)