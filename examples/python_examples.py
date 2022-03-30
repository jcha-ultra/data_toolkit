# function documentation example

# """Gets and prints the spreadsheet's header columns

# Parameters
# ----------
# file_loc : str
#     The file location of the spreadsheet
# print_cols : bool, optional
#     A flag used to print the columns to the console (default is False)

# Returns
# -------
# list
#     a list of strings representing the header columns
# """


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