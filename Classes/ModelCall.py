import io
from io import BytesIO

import torch
from flask import Response, make_response
from matplotlib import pyplot as plt
from transformers import GPT2Config, GPT2Tokenizer

from Classes.Explainer import Explainer
from Classes.GPT2SPModel import GPT2SPModel
from Classes.GPT2SPMediumModel import GPT2SPMediumModel
from Classes.Model import Model
from Classes.RnnModel import RnnModel
from IPython.core.display import HTML

from Classes.custom_transformers_interpret import SequenceClassificationExplainer


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

        elif choice == 3 or choice == 4:
            if choice == 3:
                path = "models/GPT2SP_model"
                trained_model = GPT2SPModel.load_trained_model(path)
                trained_model.eval()
                user_story = user_story
                label = [3]
                test_dataloader = GPT2SPModel.prepare_once_line(user_story, label)
                prediction = GPT2SPModel.do_inference_once(trained_model, test_dataloader)
                final_sp = Model.round_sp(prediction)
                final_sp_value = final_sp[0]
            else:
                DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
                path = "models/GPTSP_Medium_model"
                trained_model = GPT2SPMediumModel.load_trained_model(path)
                trained_model.to(DEVICE)
                trained_model.eval()
                user_story = user_story
                label = [3]
                test_dataloader = GPT2SPMediumModel.prepare_once_line(user_story, label)
                print(test_dataloader)
                prediction = GPT2SPMediumModel.do_inference_once(trained_model, test_dataloader)
                final_sp = Model.round_sp(prediction)
                final_sp_value = [final_sp]
            return final_sp_value

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

    @staticmethod
    def call_to_explain_custom(user_story):
        DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        path = "models/GPTSP_Medium_model"
        trained_model = GPT2SPMediumModel.load_trained_model(path)
        trained_model.to(DEVICE)
        trained_model.eval()
        config = GPT2Config.from_pretrained('gpt2-medium', num_labels=1, pad_token_id=50256)
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium', config=config)
        tokenizer.pad_token = '[PAD]'
        cls_explainer = SequenceClassificationExplainer(trained_model, tokenizer)
        attrs = cls_explainer(user_story, ground_truth="N/A")
        return cls_explainer.visualize()

    @staticmethod
    def call_to_explain_test(user_story):
        explainer_instance = Explainer('./models/Explainer_model/explain.pkl')
        explainer_model = explainer_instance.open_model_explainer()
        explainer = Explainer.explainer()
        exp = Explainer.explain_instance(explainer, user_story, explainer_model, 5)
        list_of_words = Explainer.get_all_the_list_of_words(exp)
        # html = exp.show_in_notebook()

        display_obj = HTML(exp.as_html())

        # print(type(exp.show_in_notebook(text=True)))
        # buf = io.BytesIO(html)
        # plt.savefig(buf, format='png')
        # buf.seek(0)

        html_string = display_obj.data
        # Render the HTML template with the notebook results
        return html_string
        # html_content = exp.as_html()*****
        # create a Flask response with the HTML content
        # response = make_response(html_content) ****

        # response.headers['Content-Type'] = 'text/html' **
        # **** response.headers['Content-Disposition'] = 'attachment; filename=explanation.html'
        # return response ****
        # return html
