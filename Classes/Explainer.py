import io
import pickle
import time

import nbconvert
from PIL import Image
# from PIL.Image import Image
from flask import Response
from selenium import webdriver
from lime.lime_text import LimeTextExplainer
from matplotlib import pyplot as plt


class Explainer:
    def __init__(self, model_path):
        self.model_path = model_path

    def open_model_explainer(self):
        with open(self.model_path, 'rb') as f:
            loaded_model = pickle.load(f)
            return loaded_model

    @staticmethod
    def explainer():
        labels = ['2', '8', '1', '3', '5', '4', '13', '20', '10', '21', '40', '17', '6']
        explainer = LimeTextExplainer(class_names=labels)
        return explainer

    @staticmethod
    def explain_instance(explainer, user_story, model, num_fea):
        exp = explainer.explain_instance(user_story,
                                         model.predict_proba, num_features=num_fea)
        return exp

    @staticmethod
    def get_all_the_list_of_words(exp):
        return exp.as_list()

    @staticmethod
    def get_plot(exp):
        fig = exp.as_pyplot_figure()
        fig_bytes = io.BytesIO()
        plt.savefig(fig_bytes, format='png')

        # Create a response object with the image data
        response = Response(fig_bytes.getvalue(), mimetype='image/png')
        return response

