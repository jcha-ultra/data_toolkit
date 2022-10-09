# call the constructor of a parent class
class Foo:
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)
