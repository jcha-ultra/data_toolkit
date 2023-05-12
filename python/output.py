# writing to a file
with open("hello.txt", mode="w") as file:
    file.write("Hello, World!")

# printing to a file:
with open('output_path', 'w') as f:
    print('text 1', 'text 2', file=f)

# adding custom handlers to logger
import logging
parent_logger = logging.getLogger('parent_module')
handler_1 = logging.StreamHandler()
parent_logger.addHandler(handler_1)
handler_2 = logging.FileHandler(filename='example_path')
parent_logger.addHandler(handler_2)
parent_logger.warn('test parent warning')
child_logger = logging.getLogger('parent_module.child_module')
child_logger.warn('test child warning')
