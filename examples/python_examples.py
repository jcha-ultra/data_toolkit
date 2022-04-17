# function documentation example

"""Gets and prints the spreadsheet's header columns

Parameters
----------
file_loc : str
    The file location of the spreadsheet
print_cols : bool, optional
    A flag used to print the columns to the console (default is False)

Returns
-------
list
    a list of strings representing the header columns
"""

########################################################################################################################

# class documentation example; source: https://realpython.com/documenting-python-code/

"""A class used to represent an Animal

Attributes
----------
says_str : str
    a formatted string to print out what the animal says
name : str
    the name of the animal
sound : str
    the sound that the animal makes
num_legs : int
    the number of legs the animal has (default 4)

Methods
-------
says(sound=None)
    Prints the animals name and what sound it makes
"""

########################################################################################################################

# Extracts features from text using BERT, to be used for fine tuning. Adapted from https://huggingface.co/bert-base-uncased
def get_text_features(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained("bert-base-uncased")
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    return output
get_text_features("Replace me by any text you'd like.")


# Unmasks a token from a sentence using BERT. Copied from https://huggingface.co/bert-base-uncased
from transformers import pipeline
unmasker = pipeline('fill-mask', model='bert-base-uncased')
unmasker("The man worked as a [MASK].")