from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '''<p>Hello world! It's Jacob</p><img src="https://images.unsplash.com/photo-1513151233558-d860c5398176?q=80&w=1770&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" />'''


# git add .
# git commit -m "my commit message"
# git push -u origin master


# flask --app main run