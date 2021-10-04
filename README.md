# csvfix

Just a quick script to "fix"/normalise CSV files, such as actually making it
comma-separated (it's not called a CSV for nothing...), and converting the
decimal point to a `.`.

Might add more settings later.

```
usage: csvfix.py [-h] [-H] [-d DELIMITER] [-D DECIMAL] [-t THOUSANDS] file

positional arguments:
  file                  the input file

optional arguments:
  -h, --help            show this help message and exit
  -H, --headings        whether the input file has headings
  -d DELIMITER, --delimiter DELIMITER
                        the input file's delimiter character
  -D DECIMAL, --decimal DECIMAL
                        the input file's decimal delimiter
  -t THOUSANDS, --thousands THOUSANDS
                        the input file's thousands separator
```
