"""
# `literacy` is a magical magic

`%%literate` Jupyter notebook cells are:

* Markdown / HTML
* Code
* Templates (_you can put data in your document_.)

## Example

        %%literate cell_name
        # Three things you need to know.

        ## First - Everything is Markdown, use `<html>` to escape out of it.

        ## Second - Indented code blocks are executed as normal code

            print("This will print to STDOUT")

        ## Third - GFM codes fences are macros

        The snippet below injects javascript into the template.

        ```javascript
        console.log("Literacy placed me here.")
        ```
# Why literacy

Literacy was designed to put real data in a document.

## What can you do

## What can't you do


"""

from .magic import (
    Literate,
)
