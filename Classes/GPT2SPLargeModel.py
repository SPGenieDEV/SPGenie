import pandas as pd
import tokenization as tokenization
import torch
from transformers import GPT2Tokenizer, GPT2Config
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from tokenizers import Tokenizer
from Classes.GPT2SP import GPT2ForSequenceClassification as GPT2SPSeq
from Classes.GPT2SPModel import GPT2SPModel
from Classes.custom_transformers_interpret import SequenceClassificationExplainer


class GPT2SPLargeModel:
    DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    SEQUENCE_LEN = 20
    PAD_TOKEN_ID = None
    BATCH_SIZE_RATIO = None
    BATCH_SIZE = None
    TOKENIZER = None
    WITHIN_PROJECT = None
    TEXT = None
    KEY = None
    TOK = None
    TOKENIZER_MAPPING = {"#0": "gpt2_bpe", "#00": "gpt2_bpe", "#000": "gpt2_bpe",
                         "#2": "sp_word_level", "#22": "sp_word_level", "#222": "sp_word_level",
                         "#6": "wordpiece_sp", "#66": "wordpiece_sp", "#666": "wordpiece_sp",
                         "#7": "sentencepiece_sp", "#77": "sentencepiece_sp", "#777": "sentencepiece_sp"}

    PAD_TOKEN_ID_MAPPING = {"gpt2_bpe": 50256, "sp_word_level": 3, "wordpiece_sp": 0, "sentencepiece_sp": 0}

    def __init__(self, model_path, dic_path):
        super().__init__(model_path, dic_path, None)

    @staticmethod
    def load_trained_model(path):
        config = GPT2Config.from_pretrained('gpt2-large', num_labels=1, pad_token_id=50256)
        path = "models/GPTSP_Large_model"
        return GPT2SPSeq.from_pretrained(path, config=config)

    @staticmethod
    def tokenization(text_list):
        sequence_len = 20
        config = GPT2Config.from_pretrained('gpt2-large', num_labels=1, pad_token_id=50256)
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2-large', config=config)
        tokenizer.pad_token = '[PAD]'
        return tokenizer.batch_encode_plus(text_list, truncation=True, max_length=sequence_len, padding='max_length')

    @staticmethod
    def prepare_once_line(user_story, label):
        d = {'text': user_story, 'label': label, 'issuekey': "1234"}
        df = pd.DataFrame(data=d)
        test_text = df['text']
        tokens_test = GPT2SPLargeModel.tokenization(test_text)
        test_seq = torch.tensor(tokens_test['input_ids'])
        test_y = torch.tensor(label).type(torch.LongTensor)
        tensor_dataset = TensorDataset(test_seq, test_y)
        dataloader = DataLoader(tensor_dataset)
        return dataloader

    @staticmethod
    def do_inference_once(trained_model, test_dataloader):
        global TEXT, KEY
        XAI = True
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2-large')
        tokenizer.pad_token = '[PAD]'
        TOK = tokenizer
        cls_explainer = SequenceClassificationExplainer(trained_model, TOK)
        predictions = []
        true_labels = []
        batch = tuple(test_dataloader)
        b_input_ids, b_labels = batch[0]
        with torch.no_grad():
            logits = trained_model(b_input_ids)
        logits = logits['logits'].detach().cpu().numpy()
        label_ids = b_labels.to('cpu').numpy()
        predictions.append(logits)
        true_labels.append(label_ids)
        
        total_distance = 0
        index = 0
        print('Here predictions')
        print(predictions[0][0])

        return predictions[0][0]
