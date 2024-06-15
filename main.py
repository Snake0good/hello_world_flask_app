from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello world!</p>"


# git add .
# git commit -m "my commit message"
# git push -u origin master