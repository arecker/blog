from flask import Flask, render_template, Response
import json
import urllib2
import os
app = Flask(__name__)


@app.route("/")
def get_home():
	data = json.load(urllib2.urlopen('http://api.alexrecker.com/post/'))
	latest = data[0]
	return render_template('home.html', posts=data, latest=latest)


@app.route("/feed/")
def get_feed():
	data = urllib2.urlopen('http://api.alexrecker.com/post/feed/')
	res = data.read()
	data.close()
	return Response(res, mimetype='text/xml')


@app.route("/<slug>/")
def get_slug(slug):
	data = json.load(urllib2.urlopen('http://api.alexrecker.com/post/' + slug))
	return render_template('post.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)