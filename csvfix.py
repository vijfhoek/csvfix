import csv
import fileinput
import argparse
import re
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the input file")
    parser.add_argument(
        "--headings",
        action="store_true",
        default=False,
        help="whether the file has headings",
    )
    parser.add_argument("--delimiter", default=",", help="the delimiter character")
    parser.add_argument("--decimal", default=".", help="the decimal delimiter")
    parser.add_argument("--thousands", default=None, help="the thousands separator")
    args = parser.parse_args()

    if args.thousands is None:
        if args.decimal == ",":
            args.thousands = "."
        elif args.decimal == ".":
            args.thousands = ","

    # First pass: Detect decimal columns
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

    # Second pass: Convert decimal columns
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


if __name__ == "__main__":
    main()
