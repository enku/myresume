# myresume

This is a program to convert a résumé definition in YAML to HTML or PDF.

This is not **my** résumé (though that is available upon request).

## Features

  - Output to HTML or PDF
  - Pluggable theme interface
  - Ability to filter out or summarize older entries
  - Ability to produce resumes to be made public


## Installation

**myresume** is a Python package which can be installev via `pip`.

```sh
pip install git+https://github.com/enku/myresume
```

## Usage

```
usage: myresume [-h] [--since SINCE] [--format {html,pdf}] [--theme {default}]
                [--public] [--page-size PAGESIZE]
                input output

convert resume to html

positional arguments:
  input
  output

optional arguments:
  -h, --help            show this help message and exit
  --since SINCE         Filter out entries before this year
  --format {html,pdf}   Output format (default: html)
  --theme {default}
  --public              Make for public consumption by excluding address and
                        phone
  --page-size PAGESIZE  Page size (e.g. for PDF)
```

Typical usage:

```sh
myresume resume.yaml resume.html
myresume --format pdf resume.yaml resume.pdf
myresume --public resume.yaml public_resume.html
```
