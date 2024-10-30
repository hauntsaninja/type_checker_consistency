## Update

This work evolved into [PEP 729](https://peps.python.org/pep-0729/) for Typing Governance
and the [typing spec conformance test suite](https://github.com/python/typing/tree/main/conformance).

# type_checker_consistency

## Motivation

As the Python type system has gotten more complex, and the number of type checkers has grown, it's
become harder to have a source of truth for what expected behaviour should be.

While in theory behaviour is standardised via PEPs, in practice PEPs have several shortcomings:
- PEPs have many audiences. Most typing PEPs do not sufficiently describe expected behaviour,
  especially as the combinatorial complexity of the type system has grown.
- Many facets of the Python type system have been left unstandardised, both intentionally and
  unintentionally. Some standardised behaviour is not documented in PEPs and is only in the official
  Python documentation.
- Increasingly, people view PEPs as historical documents, which make it hard to add even simple
  clarifications, let alone things that could be seen as standardising new behaviour. Newer PEPs
  sometimes supersede older PEPs.

I hope that this project improves accessibility of the typing ecosystem, in two different ways.

The first is by making it easier to write new type checkers! The less would-be implementers have to
trawl through typing-sig and python/typing and PEPs and docs and type checker issue trackers to
figure why things work the way they do, the better.

The second is by improving the chances of success for new additions to the new type system features.
I feel implementation and specification need to be closely in dialogue with each other to create
successful and consistent products. Historically, the type system has primarily been developed by a
handful of type checker maintainers who are able to have this dialogue within their own heads.
However, as more people suggest additions to the type system, it feels important to create more
bandwidth for constructive, detailed dialogue.

### More thoughts on PEP process

I'd like the typing community to explicitly define some recommended guidelines before submitting
PEPs to the Steering Council. For example:

- Typing PEPs should come with associated test cases. The level of detail here should be higher than
  what we've historically seen in the body text of PEPs.
- There is an implementation in at least one major type checker that passes these test cases.
- Maintainers of at least two of the major type checkers have reviewed the PEP and test cases, and
  broadly approve (if this can't be done, it's a strong indication it shouldn't be standard).

Some process notes:
- "major" type checker would be interpreted by Jelle and Guido in a commonsense way.
- The only process that is mandatory would be PEP 1. While the above would be recommended, the PEP
  sponsor could always choose to submit the PEP regardless.

## What this project contains

This project contains test cases for various behaviours of Python type checkers. Test cases can
be found in the following directories:
- `standard`. Behaviour for the test case is prescribed by a PEP, the official Python documentation
  or on typing.readthedocs.io (and hasn't been superseded by a newer prescription).
- `draft_standard`. Behaviour is prescribed by a draft standard.
- `unstandardised`. Behaviour is not prescribed by any standard.

For each test case, we also record the behaviour of the four major type checkers:
mypy, pytype, pyre, and pyright. The output is automatically generated, but can come with
associated commentary. In particular, watch out for the following phrases:

- `standard`. The behaviour matches a standard.
- `intentionally nonstandard`. The behaviour intentionally differs from a standard. Should be
  accompanied by a link to type checker documentation or issue tracker comment.
- `defacto standard`. The behaviour has not been prescribed by a standard, but is either consistent
  across all major type checkers whose behaviour is intentional or there is broad consensus that
  some behaviour is correct (e.g. evidenced by typing-sig discussion).
- `subject to change`. The behaviour unintentionally differs from the standard or defacto standard
  or will change in the future.
- `unknown`. Catch-all that should be explained in commentary.

## Contributing

Please contribute! Some notes:

Test cases are meant to be human readable. Please quote from standards documents, liberally link to
discussions and issue trackers, etc. Do not bulk import test cases from type checker test suites.

Double coverage across tests is fine. Test cases for a particular feature should be relatively
standalone.

The focus of this repository is currently the static type system, not general Python semantics.
In particular, for now, err on the side of avoiding test cases where the correct behaviour can be
easily determined from the interpreter.
