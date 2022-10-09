# add the current working directory when a script is executed to the system path. Allows Python to detect packages defined at this path.
import sys
sys.path.append('')

# programmatically import modules
import importlib
importlib.import_module('module_name')
