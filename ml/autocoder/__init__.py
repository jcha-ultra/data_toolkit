"""Autocode a function from a name and functionality description."""

from dataclasses import dataclass
import os
from typing import Protocol

from assistants import BasicAssistant


class Assistant(Protocol):
    """
    A natural language assistant that can answer questions and provide explanations.
    Typically powered by a large language model.
    """

    def post_request(self, request: str) -> str:  # type: ignore
        """Post a request to the language model."""


def generate_docs_request(name, functionality) -> str:
    """Generate request for a docstring for the function."""
    request = f"Generate the docstring for a Python function with the name and description below. Include parameter and return types. Do not include the function signature or the function itself. Do not post any other output besides the documentation. Do not include any examples in the docstring.\n\nName:\n`{name}`\n\nFunctionality:\n{functionality}."
    return request


def generate_signature_request(name, documentation) -> str:
    """Generate a request for the function signature for the function."""
    request = f'Generate the function signature for a Python function called `{name}` that has the docstring below. Do not include the function body, or the docstring. Do not post any other output besides the function signature.\n\nDocstring:\n"""\n{documentation}\n"""\n'
    return request


def generate_examples_request(documentation) -> str:
    """Generate examples for the documentation."""
    request = f'Generate an Examples section for the Python docstring below. The examples should be in a format parsable by doctests. Include at least 3 examples, preferably those showing diverse use cases, including negative tests. Do not include the function signature or the function itself. Do not post any other output besides the examples.\n\nDocstring:\n"""\n{documentation}\n"""\n'
    return request


def generate_body_request(header: str) -> str:
    """Generate code for the function."""
    request = f"Generate a Python function that starts with the signature and docstring below. Use functionality from external packages (including 3rd-party ones) whenever possible, and include any import statements needed. Prefer concision, simplicity, and performance. \n\nSignature and docstring:\n\n{header}"
    return request


@dataclass(frozen=True)
class DraftOutputs:
    """Outputs from drafting a function."""

    docs: str
    """The parameters and returns for the drafted function. Does not include examples."""
    signature: str
    """The signature for the function."""
    examples: str
    """The examples for the drafted function."""
    full_docstring: str
    """The full docstring for the drafted function."""
    code: str
    """The code for the function."""


def draft_function(name: str, functionality: str, assistant: Assistant) -> DraftOutputs:
    """
    Draft a function with the given name and functionality, using a language
    model to generate the docstring, signature, and examples.
    """
    docs = assistant.post_request(generate_docs_request(name, functionality))
    docs = docs.strip("\n").strip('"').strip("\n")
    print("...docs generated")
    # print(docs)

    signature = assistant.post_request(
        generate_signature_request(name=name, documentation=docs)
    )
    signature = signature.strip()
    print("...signature generated")
    # print(signature)

    examples = assistant.post_request(generate_examples_request(documentation=docs))
    examples = examples.strip("\n")
    print("...examples generated")
    # print(examples)

    full_docstring = f'''    """\n{docs}\n\n{examples}\n"""'''.replace("\n", "\n    ")
    header = f"""{signature}
    {full_docstring}"""
    print("...header generated")
    # print(header)

    code = assistant.post_request(generate_body_request(header=header))
    code = code.strip()
    print("...code generated")
    # print(code)

    return DraftOutputs(
        docs=docs,
        signature=signature,
        examples=examples,
        full_docstring=full_docstring,
        code=code,
    )


# TBD:
# - test code
# - debug/test loop


# %%

# PrimeFunc = Callable[[int], int]

# def make_function(code: str) -> PrimeFunc:
#     """Make the function from the code given."""
#     exec(code)
#     return locals()[NAME]

# prime = make_function(code=code)

# # %%
# def generate_tests(documentation, context) -> Sequence[Callable[[Callable], Literal[True]]]:
#     """Generate a set of tests for the function."""

#     def test_1(func: PrimeFunc):
#         assert func(1) == 2
#         return True
#     def test_5(func: PrimeFunc):
#         assert func(5) == 11
#         return True
#     def test_10(func: PrimeFunc):
#         assert func(10) == 29
#         return True

#     return [
#         test_1,
#         test_5,
#         test_10,
#     ]

# tests = generate_tests(documentation=docs, context=CONTEXT)

# # %%
# def test_code(func, tests) -> "dict[str, bool]":
#     """Test the function."""
#     results = {}
#     for test in tests:
#         try:
#             test(func)
#         except AssertionError as e:
#             results[test.__name__] = False
#             print(f"Test `{test.__name__}` failed: {e}")
#         else:
#             results[test.__name__] = True
#             print(f"Test `{test.__name__}` passed")
#     return results

# test_code(prime, tests)


def demo():
    """Demo the function drafting process."""
    from langchain.llms import OpenAI

    # Set up the OpenAI API key in the environment, if needed
    # os.environ["OPENAI_API_KEY"] = "<your key>"

    # If the key is not set, the code will raise an error
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("Please set the OpenAI API key as an environment variable.")

    function_name = "reconstruct_relational_tables"
    functionality = "given a list of json objects, each representing a row in a table, with a nested field representing a table, and a join key for that table, reconstruct the relational tables, i.e. un-nest the nested values, and return the two un-nested tables."

    # name = "fibonacci"
    # functionality = "generates the nth fibonacci number"

    # name = "get_python_architecture_structure"
    # functionality = "Given a directory of Python packages and modules, create a dictionary that describes the structure of the packages, modules, classes, and functions within the directory."

    model_name = "text-davinci-003"
    text_llm = OpenAI(temperature=0, model_name=model_name, max_tokens=-1)
    assistant = BasicAssistant(text_llm)
    results = draft_function(
        name=function_name, functionality=functionality, assistant=assistant
    )
    func_draft = results.code
    print(func_draft)


os.environ["OPENAI_API_KEY"] = "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"

if __name__ == "__main__":
    demo()



# from dataclasses import dataclass
# import os
# from typing import Any, Callable, Literal, Sequence, Union

# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate

# openai_api_key = "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"
# os.environ["OPENAI_API_KEY"] = openai_api_key
# text_llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=512)

# _ASSISTANT_TEMPLATE = """You are an assistant to a human, powered by a large language model trained by OpenAI.

# You are designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, you are able to generate human-like text based on the input you receive, allowing you to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand. You are able to update your responses based on feedback from the user, allowing you to improve your responses over a conversation.

# You are constantly learning and improving, and your capabilities are constantly evolving. You are able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. You have access to some personalized information provided by the human in the Context section below. Additionally, you are able to generate your own text based on the input you receive, allowing you to engage in discussions and provide explanations and descriptions on a wide range of topics.

# Overall, you are a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether the human needs help with a specific question or just wants to have a conversation about a particular topic, you are here to assist.

# User: {input}
# Assistant:"""

# # %%

# def create_context(resource: Union[str, None]=None) -> Union[str, None]:
#     """Construct a context from a resource."""

#     return None

# # %%

# # name = "fibonacci"
# # functionality = "generates the nth fibonacci number"

# NAME = "prime"
# FUNCTIONALITY = "generates the nth prime number"
# CONTEXT = create_context()

# # %%
# def generate_docs(name, functionality, context) -> str:
#     """Generate a docstring for the function."""
#     prompt = PromptTemplate(
#         input_variables=["input"], template=_ASSISTANT_TEMPLATE
#     ).format(input=f"Generate the docstring (in numpy format) for a Python function with the name and description below. Do not include the function signature or the function itself. Do not post any other output besides the documentation. Do not include any examples in the docstring.\n\nName:\n`{name}`\n\nFunctionality:\n{functionality}.")
#     return text_llm(prompt)


# def generate_signature(name, documentation, context) -> str:
#     """Generate a function signature for the function."""

#     request = f'Generate the function signature for a Python function called `{name}` that has the following docstring. Do not include the function body, or the docstring. Do not post any other output besides the function signature.\n\nDocstring:\n"""\n{documentation}\n"""\n'
#     prompt = PromptTemplate(
#         input_variables=["input"], template=_ASSISTANT_TEMPLATE
#     ).format(input=request)
#     return text_llm(prompt)


# def generate_examples(documentation, context) -> str:
#     """Generate a function signature for the function."""

#     request = f'Generate an Examples section for the following Python docstring, in NumPy format. Include at least 3 examples, preferably showing diverse use cases, including negative tests. Do not include the function signature or the function itself. Do not post any other output besides the examples.\n\nDocstring:\n"""\n{documentation}\n"""\n'
#     print(request)
#     prompt = PromptTemplate(
#         input_variables=["input"], template=_ASSISTANT_TEMPLATE
#     ).format(input=request)
#     return text_llm(prompt)


# def generate_body(header: str) -> str:
#     """Generate code for the function."""
#     request = f"Generate the code for a Python function with the following signature and docstring. Include the docstring in the output. \n\nSignature and docstring:\n\n{header}"
#     prompt = PromptTemplate(
#         input_variables=["input"], template=_ASSISTANT_TEMPLATE
#     ).format(input=request)
#     return text_llm(prompt)


# @dataclass(frozen=True)
# class DraftOutputs:
#     """Outputs from drafting a function."""
#     docs: str
#     """The parameters and returns for the drafted function. Does not include examples."""
#     signature: str
#     """The signature for the function."""
#     examples: str
#     """The examples for the drafted function."""
#     full_docstring: str
#     """The full docstring for the drafted function."""
#     code: str
#     """The code for the function."""


# def draft_function(name: str, functionality: str, context: Any) -> DraftOutputs:
#     """
#     Draft a function with the given name and functionality, using a language
#     model to generate the docstring, signature, and examples.
#     """
#     docs = generate_docs(name, functionality, context)
#     docs = docs.strip('\n').strip('"').strip('\n')
#     print("docs generated")
#     # print(docs)

#     signature = generate_signature(name=name, documentation=docs, context=context)
#     signature = signature.strip()
#     print("signature generated")
#     # print(signature)

#     examples = generate_examples(documentation=docs, context=context)
#     examples = examples.strip("\n")
#     print("examples generated")
#     # print(examples)

#     full_docstring = f'''    """\n{docs}\n\n{examples}"""'''.replace('\n', '\n    ')
#     header = f'''{signature}
#     {full_docstring}'''
#     print("header generated")
#     # print(header)

#     code = generate_body(header=header)
#     code = code.strip()
#     print("code generated")
#     # print(code)

#     return DraftOutputs(docs=docs, signature=signature, examples=examples, full_docstring=full_docstring, code=code)

# func_draft = draft_function(name=NAME, functionality=FUNCTIONALITY, context=CONTEXT).code
# print(func_draft)
# # %%

# PrimeFunc = Callable[[int], int]

# def make_function(code: str) -> PrimeFunc:
#     """Make the function from the code given."""
#     exec(code)
#     return locals()[NAME]

# prime = make_function(code=code)

# # %%
# def generate_tests(documentation, context) -> Sequence[Callable[[Callable], Literal[True]]]:
#     """Generate a set of tests for the function."""
    
#     def test_1(func: PrimeFunc):
#         assert func(1) == 2
#         return True
#     def test_5(func: PrimeFunc):
#         assert func(5) == 11
#         return True
#     def test_10(func: PrimeFunc):
#         assert func(10) == 29
#         return True

#     return [
#         test_1,
#         test_5,
#         test_10,
#     ]

# tests = generate_tests(documentation=docs, context=CONTEXT)

# # %%
# def test_code(func, tests) -> "dict[str, bool]":
#     """Test the function."""
#     results = {}
#     for test in tests:
#         try:
#             test(func)
#         except AssertionError as e:
#             results[test.__name__] = False
#             print(f"Test `{test.__name__}` failed: {e}")
#         else:
#             results[test.__name__] = True
#             print(f"Test `{test.__name__}` passed")
#     return results

# test_code(prime, tests)

# body = generate_body(header=header)
# body = "    " + body.strip("\n").replace("\n", "\n    ")
# code = f"{header}\n{body}"
# print(code)
