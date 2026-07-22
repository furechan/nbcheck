# Notebook format validation utility

This project is a simple utility wrapper around `nbformat` to check the validity of notebook files.
The utility will return a non zero return code if any of the notebooks has validations errors.
This may be useful in pre-commit scripts to detect problematic notebooks.

## Usage

```console
Usage: nbcheck [OPTIONS] [PATH]...

  Check notebooks for validation errors

Options:
  -r, --recurse   Recurse to sub directories
  -x, --executed  Fail notebooks with unexecuted code cells
  -v, --verbose   Print validation errors
  --help          Show this message and exit.
```

The `--executed` option additionally fails notebooks where any non-empty code cell has no execution count — catching notebooks committed with cleared or never-run outputs. Useful when committed outputs are the published artifact, e.g. notebooks rendered to a docs site without execution.

## Example

```console
> nbcheck extras
pass extras/valid-notebook.ipynb
fail extras/broken-notebook.ipynb
fail extras/nbformat-read.ipynb
```

## Installation

You can install the latest version of this module with `pip` or `pipx`

```console
pipx install git+ssh://git@github.com/furechan/nbcheck.git
```

## Related Resources
- [The Jupyter Notebook Format](https://nbformat.readthedocs.io/en/latest/)
- [nbfornat API](https://nbformat.readthedocs.io/en/latest/api.html)
