from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/upload")
def upload():
	return render_template("upload/index.html")

@app.route("/result")
def result():
	return render_template("upload/result.html")

if __name__ == '__main__':
	app.run(debug=True)