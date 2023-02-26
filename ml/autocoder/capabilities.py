"""Maintenance of autocoding capabilities."""

import inspect
import os
from pathlib import Path
import sys
from typing import Any, Callable, Union
from langchain.llms import OpenAI

sys.path.append("")
from ml.assistants import BasicAssistant
from ml.autocoder.drafting import Assistant, draft_function


def add_capability(
    name: str, functionality: str, outdir: str, assistant: Assistant, override=False
) -> None:
    """Add a capability to the capabilities directory."""
    capability_file = Path(outdir) / f"{name}.py"
    if capability_file.exists() and not override:
        raise ValueError(f"Capability file already exists: {capability_file}")

    # If the key is not set, the code will raise an error
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError(
            "Please set the OpenAI API key as an environment variable called `OPENAI_API_KEY`."
        )
    results = draft_function(
        name=name, functionality=functionality, assistant=assistant
    )
    func_draft = results.code

    with open(capability_file, "w", encoding="utf-8") as f:
        f.write(func_draft)


def run_capability(name: str, capabilities_dir: str, *args, **kwargs) -> Any:
    """Run a capability."""
    capability_file = Path(capabilities_dir) / f"{name}.py"
    if not capability_file.exists():
        raise ValueError(f"Capability file does not exist: {capability_file}")
    with open(capability_file, "r", encoding="utf-8") as f:
        code = f.read()
    exec(code)
    func = locals()[name]
    return func(*args, **kwargs)


# def find_capability(description: str, capabilities_dir: str) -> str:
#     """Given a description of a capability, figure out which capability from a directory best matches the description."""
#     breakpoint()


TEST_ASSISTANT = BasicAssistant(
    OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=-1)
)

from importlib import import_module


def summarize_code(code: str, assistant: Assistant) -> str:
    """Use an ML model to summarize a code snippet."""
    raise NotImplementedError


def summarize_docs(func: Callable, assistant: Union[Assistant, None] = None) -> str:
    """Use the first sentence of a docstring as a summary. If no docstring, use a provided assistant to summarize the code."""
    docstring = inspect.getdoc(func)
    if docstring is None and assistant is not None:
        code = inspect.getsource(func)
        return summarize_code(code, assistant)
    if docstring is None:
        return ""
    docstring_summary = docstring.split(".", maxsplit=1)[0]
    return docstring_summary


def make_summaries(module_functions: dict):
    """Make a dictionary of function summaries."""
    func_summaries = {}
    for func_name, func in module_functions.items():
        docstring_summary = summarize_docs(func)
        func_summaries[func_name] = docstring_summary
    return func_summaries


def get_package_functions(file_path: str):
    """Get all functions in modules within a package. Does not include functions in top-level __init__.py files."""
    module_list = []
    for root, _, files in os.walk(file_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                module_list.append(
                    os.path.join(root, file).replace("/", ".").replace(".py", "")
                )
    package_functions = {}
    for module_name in module_list:
        module = import_module(module_name)
        package_functions = {
            **package_functions,
            **{
                (module_name, obj_name): obj
                for obj_name, obj in inspect.getmembers(module)
                if inspect.isfunction(obj)
            },
        }
    return package_functions


def test_find_capability():
    """Test finding a capability."""

    file_path = "ml/autocoder/_capabilities"
    module_functions = get_package_functions(file_path)
    capabilities_summary = make_summaries(module_functions)

    desired_capability = "get all the classes in a module"
    breakpoint()


test_find_capability()


def test_add_capability():
    """Add a demo capability to the capabilities directory."""
    # os.environ["OPENAI_API_KEY"] = "<FILL IN>"

    outdir = "ml/autocoder/_capabilities"
    name = "get_class_list"
    functionality = "Given a file path to a Python module, return a list of classes in the package."

    add_capability(name, functionality, outdir, TEST_ASSISTANT)

    assert (Path(outdir) / f"{name}.py").exists()


if __name__ == "__main__":
    test_add_capability()
