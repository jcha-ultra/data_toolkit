# setting attribute to function
def generate_counter():
    def add_one():
        add_one.x += 1
        return add_one.x
    add_one.x = 0
    return add_one
