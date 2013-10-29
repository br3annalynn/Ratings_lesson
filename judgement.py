from flask import Flask, render_template, redirect, request
import model
app = Flask(__name__)

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("index.html", users=user_list)

@app.route("/process_login")
def process_login():
    pass

@app.route("/register")
def register():
    pass

if __name__ == "__main__":
    app.run(debug = True)

