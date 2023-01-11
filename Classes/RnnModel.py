from Classes.Model import Model
import tensorflow as tf


class RnnModel(Model):
    def __init__(self, model_path, dic_path):
        super().__init__(model_path, dic_path, None)

    def open_model_rnn(self):
        print(self.model_path)
        model = tf.keras.models.load_model(self.model_path, compile=False)
        return model

