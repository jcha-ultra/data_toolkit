
# call the constructor of a parent class
class Foo:
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)

# destructuring dataclasses
from dataclasses import astuple, dataclass
@dataclass
class Foo:
    bar: str
    baz: int
foo = Foo('bar', 42)
bar, baz = astuple(foo)
