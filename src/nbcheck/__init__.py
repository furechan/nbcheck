""" Notebook Validation Check Utility """

import sys
import click
import nbformat

from pathlib import Path


def collect_files(paths, *, recurse=False):
    """ collect file paths with optional recursion """

    files = []

    for path in paths:
        path = Path(path)
        if path.is_dir():
            if recurse:
                files.extend(path.rglob("*.ipynb"))
            else:
                files.extend(path.glob("*.ipynb"))
        elif path.exists():
            files.append(path)
        else:
            raise FileNotFoundError(str(path))

    return files


def unexecuted_cells(nb):
    """ indices of non-empty code cells that have not been executed """

    return [
        i for i, cell in enumerate(nb.cells)
        if cell.cell_type == "code"
        and cell.source.strip()
        and cell.get("execution_count") is None
    ]


def check_notebook(file, verbose=False, executed=False):
    """ check for validation errors """

    error_dict = dict()
    try:
        with open(file, "r") as f:
            nb = nbformat.read(f,
                               as_version=nbformat.NO_CONVERT,
                               capture_validation_error=error_dict)
    except Exception as exc:
        print("fail", file)
        if verbose:
            print(exc, file=sys.stderr)
        return False

    error = error_dict.get('ValidationError')
    if error:
        print("fail", file)
        if verbose:
            print(error, file=sys.stderr)
        return False

    if executed:
        stale = unexecuted_cells(nb)
        if stale:
            print("fail", file)
            if verbose:
                cells = ", ".join(str(i) for i in stale)
                print(f"{file}: unexecuted code cells: {cells}", file=sys.stderr)
            return False

    print("pass", file)
    return True


@click.command
@click.argument("path", nargs=-1)
@click.option("-r", "--recurse", is_flag=True,
              help="Recurse to sub directories")
@click.option("-x", "--executed", is_flag=True,
              help="Fail notebooks with unexecuted code cells")
@click.option("-v", "--verbose", is_flag=True,
              help="Print validation errors")
def main(path=(), recurse=False, executed=False, verbose=False):
    """ Check notebooks for validation errors """

    files = collect_files(path, recurse=recurse)

    error_count = 0

    for file in files:
        if not check_notebook(file, verbose=verbose, executed=executed):
            error_count += 1

    if error_count > 0:
        exit(1)


if __name__ == "__main__":
    main()
