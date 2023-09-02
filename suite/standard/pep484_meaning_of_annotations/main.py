# https://peps.python.org/pep-0484/#the-meaning-of-annotations
# mypy is the reference implementation

# > Any function without annotations should be treated as having the most general type possible, or ignored, by any type checker.
# > Functions with the @no_type_check decorator should be treated as having no annotations.
from typing import Any, assert_type, reveal_type, no_type_check

def unannotated(x, y): ...

@no_type_check
def annotated_no_type_check(x: int, y: str) -> int: ...

# These should reveal the same thing
reveal_type(unannotated)
reveal_type(annotated_no_type_check)

# > For a checked function, the default annotation for arguments and for the return type is Any
def checked(annotated: int, x, y):
    assert_type(annotated, int)
    assert_type(x, Any)
    assert_type(y, Any)
    reveal_type(checked)
    assert_type(checked(annotated, x, y), Any)

# > An exception is the first argument of instance and class methods.
# > If it is not annotated, then it is assumed to have the type of the containing class for instance methods,
# > and a type object type corresponding to the containing class object for class methods.
class MethodFirstArg:
    def instance_method(self, x) -> None:
        assert_type(x, Any)
        self.instance_method(x)
        reveal_type(self)

    @classmethod
    def class_method(cls, x) -> None:
        assert_type(x, Any)
        cls.class_method(x)
        reveal_type(cls)

# > Type checkers are expected to attempt to infer as much information as necessary.
# > The minimum requirement is to handle the builtin decorators @property, @staticmethod and @classmethod.

class BuiltinDecorators:
    @property
    def prop(self) -> int:
        return 1

    @staticmethod
    def static() -> int:
        return 2

    @classmethod
    def cls(cls) -> int:
        cls.prop
        cls.static
        return 3


def test_builtin_decorators() -> None:
    reveal_type(BuiltinDecorators.prop)
    reveal_type(BuiltinDecorators.static)
    assert_type(BuiltinDecorators.static(), int)
    reveal_type(BuiltinDecorators.cls)
    assert_type(BuiltinDecorators.cls(), int)

    builtin_decorators = BuiltinDecorators()
    reveal_type(builtin_decorators.prop)
    assert_type(builtin_decorators.prop, int)
    reveal_type(builtin_decorators.static)
    assert_type(builtin_decorators.static(), int)
    reveal_type(builtin_decorators.cls)
    assert_type(builtin_decorators.cls(), int)
