"""
A meta type checker.
Not to be confused with Meta's type checker, which is better known as pyre.
"""
from __future__ import annotations
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import tomli
import tomlkit

ROOT = Path(__file__).resolve().parent.parent


def default_command_for(type_checker: str) -> str:
    if type_checker == "mypy":
        return "mypy main.py"
    elif type_checker == "pyright":
        return "pyright main.py"
    raise ValueError(f"Unknown type checker: {type_checker}")


@dataclass
class Case:
    case: Path
    type_checker: str

    def run(self) -> CaseResult:
        result = self.case / "results" / f"{self.type_checker}.toml"

        try:
            with open(result, "rb") as f:
                result_data = tomli.load(f)
        except FileNotFoundError:
            result_data = {}

        command = result_data.get("command") or default_command_for(self.type_checker)
        proc = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            text=True,
            shell=True,
            env={"MYPY_CACHE_DIR": str(ROOT / ".mypy_cache"), **os.environ},
            cwd=self.case,
        )
        return CaseResult(
            case=self.case,
            type_checker=self.type_checker,
            output=proc.stdout,
        )


@dataclass
class CaseResult:
    case: Path
    type_checker: str
    output: str

    def write(self):
        result = self.case / "results" / f"{self.type_checker}.toml"
        try:
            with open(result, "r") as f:
                existing_result = tomlkit.load(f)
        except FileNotFoundError:
            existing_result = {}
            result.parent.mkdir(parents=True, exist_ok=True)

        output = self.output.strip()
        if output:
            assert self.case.is_absolute()
            output = re.sub(re.escape(str(self.case)), "", output)
            output = re.sub(re.escape(str(self.case.relative_to(ROOT))), "", output)
            output = f"\n{output}\n"

        existing_result["output"] = tomlkit.string(output, multiline=True)
        with open(result, "w") as f:
            tomlkit.dump(existing_result, f)


def main():
    assert sys.version_info >= (3, 11)

    assert (ROOT / "meta").is_dir()
    assert (ROOT / "suite").is_dir()

    cases = [p.parent for p in Path(ROOT / "suite").rglob("main.py")]

    # TODO: concurrency, pytype, pyre
    for case in cases:
        for type_checker in ["mypy", "pyright"]:
            case_result = Case(case=case, type_checker=type_checker).run()
            case_result.write()
