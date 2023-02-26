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


def demo():
    """Demo the function drafting process using ."""
    from langchain.llms import OpenAI

    # Set up the OpenAI API key in the environment, if needed
    # os.environ["OPENAI_API_KEY"] = "<your key>"

    # If the key is not set, the code will raise an error
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("Please set the OpenAI API key as an environment variable.")

    function_name = "prime"
    functionality = "Generate the nth prime number. This function is efficient for large values of n."

    # name = "fibonacci"
    # functionality = "generates the nth fibonacci number"

    # name = "get_python_architecture_structure"
    # functionality = "Given a directory of Python packages and modules, create a dictionary that describes the structure of the packages, modules, classes, and functions within the directory."

    model_name = "text-davinci-003"
    text_llm = OpenAI(temperature=0, model_name=model_name, max_tokens=-1)
    assistant = BasicOpenAIAssistant(text_llm)
    results = draft_function(
        name=function_name, functionality=functionality, assistant=assistant
    )
    func_draft = results.code
    print(func_draft)


if __name__ == "__main__":
    demo()
