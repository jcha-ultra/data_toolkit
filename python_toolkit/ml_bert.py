
"""
Functions for using BERT models.
"""

# %%

import torch
from typing import Tuple, List, Union
from transformers import Trainer, TrainingArguments, BertTokenizerFast, BertForSequenceClassification
from pandas import read_csv
from sklearn.model_selection import train_test_split
# from os.path import join

is_gpu = torch.cuda.is_available()

# %%

def mk_bert_pt_regressor(model_name: str, is_gpu) -> BertForSequenceClassification:
    """Creates a BERT model for regression.

    Parameters
    ----------
    model_name : str
        The name of the BERT model to use.

    Returns
    -------
    BertForSequenceClassification
        An untrained model.
    """
    cpu_model = BertForSequenceClassification.from_pretrained(model_name, num_labels=1)
    return cpu_model.to("cuda") if is_gpu else cpu_model
# test_mk_bert_pt_regressor = mk_bert_pt_regressor('bert-base-uncased')

def make_training_args(config: dict) -> TrainingArguments:
    """Creates training arguments for Huggingface interface.
    
    Parameters
    ----------
    config : dict
        A dictionary of configuration parameters.
    
    Returns
    -------
    TrainingArguments
        A training arguments object.
    """
    return TrainingArguments(
        output_dir='./results',          # output directory
        num_train_epochs=3,              # total number of training epochs
        per_device_train_batch_size=8,  # batch size per device during training
        per_device_eval_batch_size=20,   # batch size for evaluation
        warmup_steps=500,                # number of warmup steps for learning rate scheduler
        weight_decay=0.01,               # strength of weight decay
        logging_dir='./logs',            # directory for storing logs
        load_best_model_at_end=True,     # load the best model when finished training (default metric is loss)
                                        # but you can specify `metric_for_best_model` argument to change to accuracy or other metric
        logging_steps=100,               # log & save weights each logging_steps
        save_steps=100,
        # logging_steps=400,               # log & save weights each logging_steps
        # save_steps=400,
        evaluation_strategy="steps",     # evaluate each `logging_steps`
    )
# test_make_training_args = make_training_args({})

# %%

class BertDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx: int) -> dict:
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor([self.labels[idx]])
        return item

    def __len__(self) -> int:
        return len(self.labels)

# %%

def make_training_datasets(texts: List[str], labels: Union[List[float], List[int]], tokenizer: BertTokenizerFast, config: dict) -> Tuple[BertDataset, BertDataset]:
    """Creates training datasets for BERT.

    Parameters
    ----------
    texts : list[str]
        A list of strings.
    labels : list[float] | list[int]
        A list of floats or ints that correspond to the labels.
    tokenizer : BertTokenizerFast
        A tokenizer for the BERT model.

    Returns
    -------
    Tuple[BertDataset, BertDataset]
        A tuple of training and evaluation datasets.
    """
    truncation, padding, max_length = config['truncation'], config['padding'], config['max_length']
    train_texts, valid_texts, train_labels, valid_labels = train_test_split(texts, labels, test_size=0.3, shuffle=False)
    train_encodings = tokenizer(train_texts, truncation=truncation, padding=padding, max_length=max_length)
    valid_encodings = tokenizer(valid_texts, truncation=truncation, padding=padding, max_length=max_length)
    train_dataset = BertDataset(train_encodings, train_labels)
    valid_dataset = BertDataset(valid_encodings, valid_labels)
    return train_dataset, valid_dataset
# test_tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased', do_lower_case=True)
# test_make_training_datasets = make_training_datasets(['sample text 1', 'sample text 2', 'sample text 3', 'sample text 4'], [0.0, 1.0, 2.0, 3.0], test_tokenizer, {'truncation': True, 'padding': True, 'max_length': 512})

# %%

def train_bert_regression_model(model_name: str, texts: List[str], labels: Union[List[int], List[float]], config: dict) -> BertForSequenceClassification:
    """Trains a BERT model for regression.

    Parameters
    ----------
    model_name : str
        The name of the BERT model to use.
    config : dict
        A dictionary of configuration parameters.

    Returns
    -------
    BertForSequenceClassification
        A trained model.
    """
    tokenizer = BertTokenizerFast.from_pretrained(model_name, do_lower_case=True)
    model = mk_bert_pt_regressor(model_name, is_gpu)
    train_dataset, valid_dataset = make_training_datasets(texts, labels, tokenizer, config)
    training_args = make_training_args(config)
    trainer = Trainer(
        model=model,                         # the instantiated Transformers model to be trained
        args=training_args,                  # training arguments, defined above
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,          # evaluation dataset
        tokenizer=tokenizer,
        # compute_metrics=compute_metrics,     # the callback that computes metrics of interest
    )
    trainer.train()
    return model

# %%


# (test) <- (test_data -> collab) <- (test_data) <- ()
# ....


# >>>

# %%
# test_data = read_csv('../datasets/roots.csv')
test_train_bert_regression_model = train_bert_regression_model(
    'bert-base-uncased', 
    test_data['k'].astype(str).to_list(),
    test_data['root_k'].to_list(),
    {'truncation': True, 'padding': True, 'max_length': 512})

# %%

def get_model_outputs(model, tokenizer: BertTokenizerFast, text: str, config: dict) -> torch.Tensor:
    """Retrieves outputs from a model given a tokenizer."""
    inputs = tokenizer(text, padding=config['padding'], truncation=config['truncation'], max_length=config['max_length'], return_tensors="pt")
    outputs = model(**inputs)
    return outputs
test_get_model_outputs = get_model_outputs(
    test_train_bert_regression_model, 
    BertTokenizerFast.from_pretrained('bert-base-uncased', do_lower_case=True),
    '49',
    {'truncation': True, 'padding': True, 'max_length': 512})







# (train_vagueness_model) <- (cloud_prototype) <- (model_train -> model_retrieval) <- (model_train) <- () # see beginning of this doc # see save_model from https://github.com/GoogleCloudPlatform/ai-platform-samples/blob/main/ai-platform/tutorials/unofficial/pytorch-on-google-cloud/sentiment_classification/python_package/trainer/utils.py
# ....
# %%
