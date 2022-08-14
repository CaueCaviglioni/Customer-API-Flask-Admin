from flask import Flask, session, abort, redirect, render_template, request
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from db import db
from db_connection import secrets
from models.customer import CustomerModel
from models.user import UserModel
from views.customer import CustomerView
import pymysql


app = Flask(__name__)
app.secret_key = "secret"

@app.before_first_request
def create_tables():
    db.create_all()

SECRET_KEY = secrets.get("SECRET_KEY")
DATABASE_USER = secrets.get("DATABASE_USER")
DATABASE_NAME = secrets.get("DATABASE_NAME")
DATABASE_PASSWORD = secrets.get("DATABASE_PASSWORD")
DATABASE_PORT = secrets.get("DATABASE_PORT")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost/{DATABASE_NAME}"
app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

admin = Admin(app, name = "freela", base_template = "layout.html", template_mode = "bootstrap3")
admin.add_view(CustomerView(CustomerModel, db.session, name = "Customers"))

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = UserModel.get_user(username = username)
        if username == user.username and password == user.password:
            session["logged_in"] = True
            return redirect("/admin")
        else:
            return render_template("login.html", failed = True)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug = True)

