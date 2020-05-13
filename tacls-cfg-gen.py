# tacls-cfg-gen: config generator for TAC Life Support
# Copyright (C) 2020 Al2Me6

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import argparse
import os
import sys
from contextlib import contextmanager
from typing import List

__version__ = "0.1.0"

# https://docs.google.com/spreadsheets/d/1DkWf210viRSNcV8tvDv30vZ_iACj6GeY1Lf_4JdZYds
# https://github.com/KSP-RO/TacLifeSupport/blob/master/Source/SettingsParams.cs#L175
DAILY_CONSUMPTION = {
    "Food": 0.365_625,
    "Water": 0.241_662_5,
    "Oxygen": 37.012_41,
    "CarbonDioxide": 31.979_78,
    "WasteWater": 0.307_75,
    "Waste": 0.033_25,
}
KERBIN_DAY_LENGTH = 6.0
CONSUMED = ("Food", "Water", "Oxygen")
INDENT = "    "


class IndentedTextBuilder:
    def __init__(self, indent: str) -> None:
        self._indent = indent
        self._indent_level = 0  # indent state
        self._text: List[str] = []  # each line is stored as a separate string
        self.newline()

    def newline(self) -> None:
        self._text.append("")

    def append(self, *snippet: str) -> None:
        # if the line is new, indent according to current indent state
        # cannot be done in newline() because indent state can change
        # between a call to newline() and the addition of actual text
        if self._text[-1] == "":
            self._text[-1] += self._indent * self._indent_level
        for snip in snippet:
            self._text[-1] += snip

    def append_line(self, *line: str) -> None:
        for ln in line:
            self.append(ln)
            self.newline()

    @contextmanager
    def indent(self):
        self._indent_level += 1
        yield
        self._indent_level -= 1

    @contextmanager
    def block(self):
        self.append_line("{")
        with self.indent():
            yield
        self.append_line("}")

    def build(self) -> str:
        return "\n".join(self._text)


def add_resource_definition(
        builder: IndentedTextBuilder,
        name: str,
        max_amount: float,
        fill: bool = True
) -> None:
    amount = max_amount if fill else 0
    builder.append_line(f"%RESOURCE[{name}]")
    with builder.block():
        builder.append_line(
            f"%amount = {amount:.4f}",
            f"%maxAmount = {max_amount:.4f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"TACLS config generator v{__version__}",
        allow_abbrev=False
    )
    parser.add_argument(
        "-p",
        required=True,
        metavar="PART",
        help="name of part to patch"
    )
    parser.add_argument(
        "-c",
        required=True,
        type=int,
        metavar="CREW",
        help="number of Kerbals to support"
    )
    parser.add_argument(
        "-d",
        required=True,
        type=float,
        metavar="DAYS",
        help=f"number of days ({KERBIN_DAY_LENGTH} hours by default) to supply"
    )
    parser.add_argument(
        "--partial",
        metavar="RESOURCE",
        nargs="+",  # at least 1
        choices=DAILY_CONSUMPTION.keys(),
        help="generate configs only for the specified resources; cannot use with -o"
    )
    parser.add_argument(
        "--day-length",
        type=float,
        default=KERBIN_DAY_LENGTH,
        metavar="HOURS",
        help="length of a day, in hours"
    )
    parser.add_argument(
        "--for",
        metavar="MOD",
        dest="for_mod",
        help="add a ModuleManager :FOR[] flag"
    )
    parser.add_argument(
        "-o",
        metavar="FILE",
        type=argparse.FileType("a"),
        help="output config to file in create-or-append mode, print to stdout if omitted"
    )
    args = parser.parse_args()
    if args.o and args.partial:
        print(
            f"{os.path.basename(sys.argv[0])} :error : -o cannot be used with --partial",
            file=sys.stderr
        )
        sys.exit(2)

    day_length_multiplier = args.day_length / KERBIN_DAY_LENGTH

    builder = IndentedTextBuilder(INDENT)  # TODO: customizable indent type
    builder.append(f"@PART[{args.p}]:NEEDS[TacLifeSupport]")
    if args.for_mod:
        builder.append(f":FOR[{args.for_mod}]")
    builder.newline()
    with builder.block():
        for resource in args.partial if args.partial else DAILY_CONSUMPTION:
            add_resource_definition(
                builder,
                name=resource,
                max_amount=DAILY_CONSUMPTION[resource] * args.c * args.d * day_length_multiplier,
                fill=resource in CONSUMED
            )
    if args.o:
        args.o.write(builder.build())
        args.o.close()
    else:
        print(builder.build())


if __name__ == "__main__":
    main()
