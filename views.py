from flask import Blueprint, render_template, request, Flask, jsonify

from Classes.Model import Model
from Classes.ModelCall import ModelCall
from Classes.RnnModel import RnnModel

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/from", methods=["POST"])
def form():
    user_story = request.form.get("userstory")
    print(user_story)
    choice = 1

    final_sp = ModelCall.call_to_model(1, user_story)

    sp_value = Model.max_occurrence(final_sp)

    return render_template("form.html", user_story=user_story, story_point=sp_value[0])


@views.route('/userStory', methods=['GET'])
def get_users():
    user_story = request.get_json()
    choice = request.args.get("choice")
    print(user_story['user_story'])
    final_sp = ModelCall.call_to_model(int(choice), str(user_story['user_story']))
    print(final_sp)
    sp_value = Model.max_occurrence(final_sp)
    print(sp_value[0])
    return jsonify({'story_point': str(sp_value[0])})
