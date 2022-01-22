# %%
import numpy as np
import torch
import random
from transformers import BertTokenizerFast, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
from transformers.file_utils import is_tf_available, is_torch_available, is_torch_tpu_available
from datasets import load_dataset
from sklearn.metrics import accuracy_score
from os.path import join

# save info
model_save_path = "/Volumes/GoogleDrive-109758737031747231314/My Drive/ml_models"
model_save_name = "emotion-bert-base-uncased"
save_path = join(model_save_path, model_save_name)

# get_target_names
emotion_dataset = load_dataset("emotion")
target_names = emotion_dataset['train'].features['label'].names

# reload our model/tokenizer. Optional, only usable when in Python files instead of notebooks
model = BertForSequenceClassification.from_pretrained(save_path, num_labels=len(target_names))
tokenizer = BertTokenizerFast.from_pretrained(save_path)

def get_prediction(text):
    # prepare our text into tokenized sequence
    inputs = tokenizer(text, padding=True, truncation=True, max_length=max_length, return_tensors="pt")
    # perform inference to our model
    outputs = model(**inputs)
    # get output probabilities by doing softmax
    probs = outputs[0].softmax(1)
    # executing argmax function to get the candidate label
    return target_names[probs.argmax()]

# Example #1
text = """
This is amazing! I'm so happy.
"""
print(get_prediction(text))
