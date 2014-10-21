from flask import Flask, render_template, Response
import json
import urllib2
import os
app = Flask(__name__, static_url_path='')


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


@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('static', path))


if __name__ == "__main__":
    app.run(debug=True)