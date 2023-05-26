from importlib import import_module
import inspect
import os

def get_class_list(file_path):
    """Returns a list of class names from a given file path."""
    class_list = []
    try:
        module = __import__(file_path)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                class_list.append(name)
    except ImportError:
        pass
    return class_list

def get_module_list(file_path: str) -> list:
    """Returns a list of module names from a given file path."""
    module_list = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith('.py'):
                module_list.append(os.path.join(root, file).replace('/', '.').replace('.py', ''))
    return module_list

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

