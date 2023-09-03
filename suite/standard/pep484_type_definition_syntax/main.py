from typing import assert_type

# https://peps.python.org/pep-0484/#type-definition-syntax

def greeting(name: str) -> str:
    return 'Hello ' + name

assert_type(greeting('Monty'), str)

# > Expressions whose type is a subtype of a specific argument type are also accepted for that argument.
class StrSub(str): ...
assert_type(greeting(StrSub('Monty')), str)

# > Type hints may be built-in classes (including those defined in standard library or third-party
# > extension modules), abstract base classes, types available in the types module, and user-defined
# > classes (including those defined in the standard library or third-party modules).
import abc
import types

class UserDefinedClass: ...
class AbstractBaseClass(abc.ABC):
    @abc.abstractmethod
    def abstract_method(self): ...

def valid_type_hints(
    p1: int, p2: str, p3: bytes, p4: bytearray, p5: memoryview, p6: complex, p7: float, p8: bool,
    p9: object, p10: type, p11: types.ModuleType, p12: types.FunctionType,
    p13: types.BuiltinFunctionType, p14: UserDefinedClass, p15: AbstractBaseClass,
): ...

# > Annotations should be kept simple or static analysis tools may not be able to interpret the values.
def too_complex_type_hint(p: eval("".join(map(chr, [105, 110, 116])))): ...  # Error

# > In addition to the above, the following special constructs defined below may be used: None, Any,
# > Union, Tuple, Callable, all ABCs and stand-ins for concrete classes exported from typing (e.g.
# > Sequence and Dict), type variables, and type aliases.
import typing

def some_more_valid_type_hints(
    p1: None, p2: typing.Any, p3: typing.Union[int, str], p4: typing.Tuple[int, str],
    p5: typing.Tuple[int, ...], p6: typing.Callable[[int, str], None], p7: typing.Sequence[int],
    p8: typing.Dict[str, int], p9: typing.Type[int]
): ...

# https://peps.python.org/pep-0484/#using-none
# > When used in a type hint, the expression None is considered equivalent to type(None).

def takes_None(x: None) -> None: ...
assert_type(takes_None(None), None)

# https://peps.python.org/pep-0484/#type-aliases
# > Type aliases are defined by simple variable assignments:

Url = str

def retry(url: Url, retry_count: int) -> None: ...
assert_type(retry('https://example.com', 3), None)
retry(1, 2)  # Error

# > Type aliases may be as complex as type hints in annotations – anything that is acceptable as a
# > type hint is acceptable in a type alias:

from typing import TypeVar, Iterable, Tuple

T_ifc = TypeVar('T_ifc', int, float, complex)
Vector = Iterable[Tuple[T_ifc, T_ifc]]

def inproduct(v: Vector[T_ifc]) -> T_ifc:
    return sum(x*y for x, y in v)
def dilate(v: Vector[T_ifc], scale: T_ifc) -> Vector[T_ifc]:
    return ((x * scale, y * scale) for x, y in v)
vec: Vector[float] = []

def inproduct_noalias(v: Iterable[Tuple[T_ifc, T_ifc]]) -> T_ifc:
    return sum(x*y for x, y in v)
def dilate_noalias(v: Iterable[Tuple[T_ifc, T_ifc]], scale: T_ifc) -> Iterable[Tuple[T_ifc, T_ifc]]:
    return ((x * scale, y * scale) for x, y in v)
vec_noalias: Iterable[Tuple[float, float]] = []

inproduct(vec)
inproduct(vec_noalias)
inproduct_noalias(vec)
inproduct_noalias(vec_noalias)
dilate(vec, 2.0)
dilate(vec_noalias, 2.0)
dilate_noalias(vec, 2.0)
dilate_noalias(vec_noalias, 2.0)

# https://peps.python.org/pep-0484/#callable
from typing import Callable

def feeder(get_next_item: Callable[[], str]) -> None: ...

def async_query(on_success: Callable[[int], None],
                on_error: Callable[[int, Exception], None]) -> None: ...

def callable_return_str() -> str: ...
def callable_return_int() -> int: ...

feeder(callable_return_str)
feeder(callable_return_int)  # Error

# > It is possible to declare the return type of a callable without specifying the call signature by
# > substituting a literal ellipsis (three dots) for the list of arguments. [...] The arguments of
# > the callback are completely unconstrained in this case (and keyword arguments are acceptable).

def partial(func: Callable[..., str], *args) -> Callable[..., str]:
    func(1, "foo")
    func("bar", 3, b"az")
    func(arbitrary_kwarg=1)
    return func

# > Because typing.Callable does double-duty as a replacement for collections.abc.Callable,
# > isinstance(x, typing.Callable) is implemented by deferring to isinstance(x,
# > collections.abc.Callable). However, isinstance(x, typing.Callable[...]) is not supported.

def narrow_callable_via_isinstance(o: object):
    if isinstance(o, Callable):
        reveal_type(o)
    if isinstance(o, Callable[[int], str]):  # Error
        reveal_type(o)

# https://peps.python.org/pep-0484/#generics

from typing import Mapping, Set

class Employee: ...
def notify_by_email(employees: Set[Employee], overrides: Mapping[str, str]) -> None: ...

# Generic function

from typing import Sequence, TypeVar

T = TypeVar('T')      # Declare type variable

def first(l: Sequence[T]) -> T:   # Generic function
    return l[0]

# > A TypeVar() expression must always directly be assigned to a variable (it should not be used as
# > part of a larger expression). The argument to TypeVar() must be a string equal to the variable
# > name to which it is assigned. Type variables must not be redefined.

def typevar_must_be_assigned(x: TypeVar("T")): ...  # Error
DoesNotMatch = TypeVar("Match")  # Error
Redefined = TypeVar("Redefined")
Redefined = TypeVar("Redefined", covariant=True)  # Error

# > TypeVar supports constraining parametric types to a fixed set of possible types

AnyStr = TypeVar('AnyStr', str, bytes)

def concat(x: AnyStr, y: AnyStr) -> AnyStr:
    return x + y

concat('foo', 'bar')
concat(b'foo', b'bar')
concat('foo', b'bar')  # Error
concat(b'foo', 'bar')  # Error

# > There should be at least two constraints, if any; specifying a single constraint is disallowed.

OneConstraint = TypeVar('OneConstraint', int)  # Error

# > Subtypes of types constrained by a type variable should be treated as their respective
# > explicitly listed base types in the context of the type variable.

class MyStr(str): ...
assert_type(concat(MyStr('apple'), MyStr('pie')), str)

# > Additionally, Any is a valid value for every type variable. [...] This is equivalent to omitting
# > the generic notation

from typing import List, Any

def count_truthy(elements: List[Any]) -> int:
    return sum(1 for elem in elements if elem)

def count_truthy_omitted(elements: List) -> int:
    return sum(1 for elem in elements if elem)

count_truthy([1, 2, 3])
count_truthy_omitted([1, 2, 3])
count_truthy([1, 2, 3, ''])
count_truthy_omitted([1, 2, 3, ''])

# https://peps.python.org/pep-0484/#user-defined-generic-types

from typing import TypeVar, Generic
from logging import Logger

class LoggedVar(Generic[T]):
    def __init__(self, value: T, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
        self.value = value

    def set(self, new: T) -> None:
        self.log('Set ' + repr(self.value))
        self.value = new

    def get(self) -> T:
        self.log('Get ' + repr(self.value))
        return self.value

    def log(self, message: str) -> None:
        self.logger.info('{}: {}'.format(self.name, message))

# > LoggedVar[T] is valid as a type

from typing import Iterable

def zero_all_vars(vars: Iterable[LoggedVar[int]]) -> None:
    for var in vars:
        var.set(0)

# > A generic type can have any number of type variables, and type variables may be constrained.

S = TypeVar('S')
class Pair(Generic[T, S]): ...
class PairConstrained(Generic[T, T_ifc]): ...

# > Each type variable argument to Generic must be distinct.

class PairInvalid(Generic[T, T]): ...  # Error

# > The Generic[T] base class is redundant in simple cases where you subclass some other generic
# > class and specify type variables for its parameters:

from typing import Iterator

class MyIter1(Iterator[T]): ...
class MyIter2(Iterator[T], Generic[T]): ...

def takes_iter(mi1: MyIter1[int], mi2: MyIter2[int]) -> None:
    for i in mi1:
        assert_type(i, int)
    for i in mi2:
        assert_type(i, int)

# > You can use multiple inheritance with Generic:

from typing import TypeVar, Generic, Sized, Iterable, Container, Tuple

T = TypeVar('T')

class LinkedList(Sized, Generic[T]):
    ...

K = TypeVar('K')
V = TypeVar('V')

class MyMapping(Iterable[Tuple[K, V]],
                Container[Tuple[K, V]],
                Generic[K, V]):
    ...

# > Subclassing a generic class without specifying type parameters assumes Any for each position.

class MyIterableAny(Iterable): ...

def unparametrised_generic(mia: MyIterableAny) -> None:
    assert_type(iter(mia), Iterator[Any])
    assert_type(next(iter(mia)), Any)

# TODO:
# https://peps.python.org/pep-0484/#scoping-rules-for-type-variables and onwards
