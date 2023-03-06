from flask import Blueprint, render_template, request, Flask, jsonify

from Classes.Model import Model
from Classes.RnnModel import RnnModel

views = Blueprint(__name__, "views")
app = Flask(__name__)


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/from", methods=["POST"])
def form():
    userStory = request.form.get("userstory")
    print(userStory)
    choice = 1

    if choice == 1:
        deep_se_model = Model('./models/deep_se_model_with_10.h5', './models/my_dict_deep_se.pickle',
                              './models/deep_se_model_with_10.json')
        model = deep_se_model.open_model()
        my_dict = deep_se_model.open_dict()

        tokenizer = Model.tokenize(my_dict)
        seq = Model.text_to_sequence(userStory.lower(), tokenizer)
        print(seq)
        pad = Model.text_pad_sequence(seq)
        print(pad)
        predict_sp = Model.predict_storyPoint(model, pad)
        print(predict_sp)
        final_sp = Model.round_sp(predict_sp)
        print(len(final_sp))
    elif choice == 2:
        rnn_model = RnnModel('./models/rnn_model.h5', './models/my_dict.pickle')
        model = rnn_model.open_model_rnn()
        print(model)
        my_dict = rnn_model.open_dict()
        print(my_dict)
        tokenizer = Model.tokenize(my_dict)
        seq = Model.text_to_sequence(userStory, tokenizer)
        print(seq)
        pad = Model.text_pad_sequence(seq)
        print(pad)
        predict_sp = Model.predict_storyPoint(model, pad)
        print(predict_sp)
        final_sp = Model.round_sp(predict_sp)
        print(len(final_sp))
        print(Model.max_occurrence(final_sp))

    spValue = Model.max_occurrence(final_sp)

    return render_template("form.html", user_story=userStory, story_point=spValue[0])


@views.route('/getStoryPoint', methods=['GET'])
def get_users():
    new_user = request.get_json()
    print(new_user)
    return jsonify({'users': [
        {
            'id': 1,
            'name': 'John'
        },
        {
            'id': 2,
            'name': 'Jane'
        }
    ]})
