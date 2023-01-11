from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
import tensorflow as tf
import pickle


class Model:

    def __init__(self, model_path, dic_path, model_json=None):
        self.model_path = model_path
        self.dic_path = dic_path
        self.model_json = model_json

    def open_model(self):
        with open(self.model_json, 'r') as f:
            print(self.model_json)
            model = tf.keras.models.model_from_json(f.read())
        model.load_weights(self.model_path)
        return model

    def open_dict(self):
        with open(self.dic_path, "rb") as f:
            my_dict_loaded = pickle.load(f)
        return my_dict_loaded

    @staticmethod
    def tokenize_function(dict):
        # tokenize text according to your language
        token_list = dict
        return token_list

    @staticmethod
    def tokenize(dic):
        # token_list = self.tokenize_function(dic)
        tokenizer = Tokenizer()
        tokenizer.word_index = dic
        return tokenizer

    @staticmethod
    def text_to_sequence(text, tokenizer):
        seq = tokenizer.texts_to_sequences([text])
        return seq

    @staticmethod
    def text_pad_sequence(seq):
        pad = pad_sequences(seq, maxlen=1000, padding='post')
        return pad

    @staticmethod
    def predict_storyPoint(model, pad):
        print(pad.shape)
        predict = model.predict(pad)
        return predict

    @staticmethod
    def round_sp(predict):
        pred2 = [x.round().astype(int) for x in predict]
        print(pred2)
        return pred2

    @staticmethod
    def max_occurrence(array):
        return max(array, key=array.count)
