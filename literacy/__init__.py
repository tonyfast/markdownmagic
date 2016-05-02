"""
# `literacy`

Literate creates a the magic `%%literate` thats allows cells to written in
literate markdown.

## Quickstart

Literacy exposes `%%literate` as a cell magic in the IPython notebook.

    from literacy import Literate
    Literate()

## Usage

    %%literate
    # This is markdown

        foo = {'bar': 'baz'}
        print("\""This indented code block will be
        executed as Python and define define a variable `foo`"\"")

    # `literate` cells are templates

    Templates allow data to be directly placed into markdown, html, or code. The
    value of `bar` in `foo` is {{foo.bar}}.

        # Templates can be used in code
        b = "{{foo.bar}}"*5

    This is a longer version of `foo.bar` is `{{b}}` without effecting {{foo}}.

"""

from .magic import (
    Literate,
)
