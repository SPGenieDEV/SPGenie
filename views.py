from flask import Blueprint, render_template, request

views = Blueprint(__name__, "views")

@views.route("/")
def home ():
    return render_template("index.html")

@views.route("/from", methods=["POST"])
def form ():    
    userStory = request.form.get("userstory")
    return render_template("form.html", user_story= userStory)