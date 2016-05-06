"""Literacy uses cell magics.

Each cell is a core `IPython` display object.
"""

from IPython.display import (
    HTML,
)
import yaml


class Cell(HTML):
    """Cell is the base class for each cell display.

    ## Input Arguments

    * `cell` - An existing `Cell` object.
    * `source` - The source code of the cell.
    """
    id = """"""
    classes = """"""


class Block(Cell):
    """A Block is either indented or fenced code or html/markdown.
    """
    fenced = False
    filter_name = 'default'
    template_name = 'block.html'
    show_html = False

    def __init__(self, cell, source):
        self.parent = cell
        self.env = cell.env
        self.raw = source
        super(Block, self).__init__(source)

    @property
    def filter(self):
        if self.filter_name and self.filter_name in self.env.filters:
            return self.env.filters[self.filter_name]
        return lambda x: x

    def compile_source(self, source=None):
        """This function is called by `render`.  Template the source code of the block.

        If the macro is the kernel language then it is executed.
        """
        self.source = self.raw if not source else source
        if self.env.globals['render_templates']:
            self.source = self.env.from_string(
                self.source,
            ).render(
                **self.parent.frontmatter
            )

    def render(self, **data):
        """Assign the `data` attribute inherited by the `IPython.display.HTML` object.
        """
        self.compile_source()
        self.compiled = self.filter(
            self.source,
        )
        self.data = self.env.get_template(
            self.template_name
        ).render(
            block=self, **data
        )
        return self.data


class NormalBlock(Block):
    """A markdown cell that injects data through jinja.  Markdown can be escaped
    using `<html>` tags.
    """
    show_source = False
    show_html = True


class FenceBlock(Block):
    """A gfm styled code fence.

    ### Example

        ```macro_name
        This is some code.
        ```
    """
    fenced = True
    show_source = True

    def __init__(self, cell, source=''):
        self.filter_name = source.split('\n', 1)[0].lstrip('```').strip()
        source = '\n'.join(source.strip('```').split('\n')[1:]).strip()
        super(FenceBlock, self).__init__(cell, source)

    def compile_source(self):
        super(FenceBlock, self).compile_source(
            '\n'.join(self.raw.strip().split('\n')[1:-1])
        )


class IndentBlock(Block):
    """An indented code block.  These code blocks are executed by the kernel.
    """
    show_source = True

    def compile_source(self):
        super(IndentBlock, self).compile_source()
        self.env.kernel(self.source)


class CellBlock(Block):
    """The main cell.
    """
    indent = 8
    filename = ""
    frontmatter = {}
    template_name = 'cell.html'

    def __init__(self, env, source, var_name=""):
        self.env = env
        self.blocks = []
        self.raw = source
        if var_name:
          self.env.ip.user_ns[var_name] = self
        if source.startswith('---'):
            tmp, self.raw = self.raw.lstrip('---').split('---', 1)
            self.frontmatter = yaml.load(tmp)
        self.render()

    def render(self, **data):
        self.env.globals['this'] = {
            'cell': self,
            'block': None,
        }
        self.data = ""
        self.blocks = []
        """Split code from non-code blocks."""
        for ct, fence in enumerate(self.raw.split('\n```')):
            if (ct % 2) == 1:
                """ct=0 is false"""
                self.env.globals['this']['block'] = FenceBlock(
                  self, "```{}```".format(fence)
                )
                self.blocks.append(self.env.globals['this']['block'])
            else:
                rendered_markdown = self.env.preprocessor(fence)
                """Discover basic idented code blocks"""
                indent_blocks = rendered_markdown.replace(
                    '</code></pre>', '<pre><code>'
                ).split('<pre><code>')
                for ct_md, block in enumerate(indent_blocks):
                    if (ct_md % 2) == 1:
                        self.env.globals['this']['block'] = IndentBlock(
                            self, block
                        )
                    else:
                        self.env.globals['this']['block'] = NormalBlock(
                            self, block
                        )
                    self.blocks.append(self.env.globals['this']['block'])
        """Render the whole cell"""
        self.data = self.env.get_template(self.template_name).render(
            cell=self,  **data,
        )
        return self.data
