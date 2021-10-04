import csv
import argparse
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the input file")
    parser.add_argument(
        "-H",
        "--headings",
        action="store_true",
        default=False,
        help="whether the input file has headings",
    )
    parser.add_argument(
        "-d", "--delimiter", default=",", help="the input file's delimiter character"
    )
    parser.add_argument(
        "-D", "--decimal", default=".", help="the input file's decimal delimiter"
    )
    parser.add_argument(
        "-t", "--thousands", default=None, help="the input file's thousands separator"
    )
    args = parser.parse_args()

    if args.thousands is None:
        if args.decimal == ",":
            args.thousands = "."
        elif args.decimal == ".":
            args.thousands = ","

    return args


def first_pass(args: argparse.Namespace) -> set[int]:
    """First pass: Detect decimal columns"""
    decimal_re = re.compile(
        "^[+-]?([0-9{1}]+([{0}][0-9{1}]*)?|[{0}][0-9{1}]+)$".format(
            re.escape(args.decimal), re.escape(args.thousands)
        )
    )

    not_decimal_columns = set()
    with open(args.file) as csvfile:
        reader = csv.reader(csvfile, delimiter=args.delimiter)
        if args.headings:
            next(reader)
        for row in reader:
            for i, column in enumerate(row):
                if not decimal_re.match(column):
                    not_decimal_columns.add(i)

    return not_decimal_columns


def second_pass(args: argparse.Namespace, not_decimal_columns: set[int]) -> None:
    """Second pass: Convert decimal columns"""
    with open(args.file) as csvfile:
        reader = csv.reader(csvfile, delimiter=args.delimiter)
        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)
        if args.headings:
            writer.writerow(next(reader))
        for row in reader:
            columns = []
            for i, column in enumerate(row):
                if i not in not_decimal_columns:
                    value = (
                        column.replace(args.thousands, "").replace(args.decimal, ".")
                    )
                else:
                    value = column
                columns.append(value)
            writer.writerow(columns)


def main() -> None:
    args = parse_args()
    not_decimal_columns = first_pass(args)
    second_pass(args, not_decimal_columns)


if __name__ == "__main__":
    main()
