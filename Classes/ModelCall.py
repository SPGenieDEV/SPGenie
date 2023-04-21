from io import BytesIO

from flask import Response
from matplotlib import pyplot as plt

from Classes.Explainer import Explainer
from Classes.GPT2SPModel import GPT2SPModel
from Classes.Model import Model
from Classes.RnnModel import RnnModel
from IPython.core.display import HTML


class ModelCall:

    @staticmethod
    def call_to_model(choice, user_story):
        if choice == 1:
            deep_se_model = Model('./models/deep_se_model_with_10.h5', './models/my_dict_deep_se.pickle',
                                  './models/deep_se_model_with_10.json')
            model = deep_se_model.open_model()
            my_dict = deep_se_model.open_dict()

            tokenizer = Model.tokenize(my_dict)
            seq = Model.text_to_sequence(user_story.lower(), tokenizer)
            print(seq)
            pad = Model.text_pad_sequence(seq)
            print(pad)
            predict_sp = Model.predict_storyPoint(model, pad)
            print(predict_sp)
            final_sp = Model.round_sp(predict_sp)
            print(len(final_sp))
            return final_sp
        elif choice == 2:
            rnn_model = RnnModel('./models/rnn_model.h5', './models/my_dict.pickle')
            model = rnn_model.open_model_rnn()
            print(model)
            my_dict = rnn_model.open_dict()
            print(my_dict)
            tokenizer = Model.tokenize(my_dict)
            seq = Model.text_to_sequence(user_story, tokenizer)
            print(seq)
            pad = Model.text_pad_sequence(seq)
            print(pad)
            predict_sp = Model.predict_storyPoint(model, pad)
            print(predict_sp)
            final_sp = Model.round_sp(predict_sp)
            print(len(final_sp))
            print(Model.max_occurrence(final_sp))
            return final_sp

        elif choice == 3:
            trained_model = GPT2SPModel.load_trained_model()
            trained_model.eval()
            user_story = user_story
            label = [3]
            test_dataloader = GPT2SPModel.prepare_once_line(user_story, label)
            prediction = GPT2SPModel.do_inference_once(trained_model, test_dataloader)
            final_sp = Model.round_sp(prediction[0])
            return final_sp

    @staticmethod
    def call_to_explain(user_story):
        explainer_instance = Explainer('./models/Explainer_model/explain.pkl')
        explainer_model = explainer_instance.open_model_explainer()
        explainer = Explainer.explainer()
        exp = Explainer.explain_instance(explainer, user_story, explainer_model, 5)
        list_of_words = Explainer.get_all_the_list_of_words(exp)
        image_response = Explainer.get_plot(exp)
        """
        combined_data = 'hello'.encode() + b'\n' + image_response.get_data()
        final_response = Response(response=combined_data, status=200, mimetype='multipart/related')
        final_response.headers["Content-Disposition"] = "attachment; filename=response.txt"
        """
        # print(Explainer.get_all_the_list_of_words(exp))
        fig_bytes = BytesIO()
        plt.savefig(fig_bytes, format='png')

        # Create a response object with the image data
        response = Response(fig_bytes.getvalue(), mimetype='image/png')
        return response


