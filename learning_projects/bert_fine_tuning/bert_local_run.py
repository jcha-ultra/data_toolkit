# this script loads the locally saved huggingface model from `./bert_training_example.ipynb`

from transformers import BertTokenizerFast, BertForSequenceClassification
from datasets import load_dataset
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

# from https://colab.research.google.com/drive/18Qqox_QxJkOs80XVYaoLsdum0dX-Ilxb?usp=sharing#scrollTo=I4aAwDGZXnyk
def get_prediction(text):
    # prepare our text into tokenized sequence
    inputs = tokenizer(text, padding=True, truncation=True, max_length=max_length, return_tensors="pt")
    # perform inference to our model
    outputs = model(**inputs)
    # get output probabilities by doing softmax
    probs = outputs[0].softmax(1)
    # executing argmax function to get the candidate label
    return target_names[probs.argmax()]

# Example
# text = """
# This is amazing! I'm so happy.
# """
# print(get_prediction(text)) # expected: joy
