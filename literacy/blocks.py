
# coding: utf-8

# Literacy uses cell magics.
# 
# Each cell is a core `IPython` display object.
from IPython.display import (
    HTML,
)
# 
class Cell(HTML):
    """Cell is the base class for each cell display.

    ## Input Arguments

    * `cell` - An existing `Cell` object.
    * `source` - The source code of the cell.
    """
    id = """"""
    classes = """"""
    def __init__(self, cell, source):
        self.env = cell.env
        self.raw = source
        self.macro = self.env.macros['default']
        if self.macro_name in self.env.macros:
            self.macro = self.env.macros[self.macro_name]
        super().__init__(source)
        self.render()
# 
class Block(Cell):
    """A Block is either indented or fenced code or html/markdown.
    """
    fenced = False
    macro_name = 'default'
    def __init__(self, cell, source):
        self.parent = cell
        self.raw = source
        super().__init__(cell, source)

    def compile(self, source=None):
        """This function is called by `render`.  Template the source code of the block.

        If the macro is the kernel language then it is executed.
        """
        source = self.raw if not source else source
        self.source = self.env.from_string(source).render(**self.parent.frontmatter)
        if self.macro_name in [self.env.kernel_name]:
            self.env.kernel(self.source)

    def render(self, **data):
        """Assign the `data` attribute inherited by the `IPython.display.HTML` object.
        """
        self.compile()
        self.data = self.macro.render(block=self, **data)
        return self.data
# 
class NormalBlock(Block):
    """A markdown cell that injects data through jinja.  Markdown can be escaped
    using `<html>` tags.
    """
    macro_name = 'markdown'
    pass
# 
class FenceBlock(Block):
    """A gfm styled code fence.

    ### Example

        ```macro_name
        This is some code.
        ```
    """
    fenced = True
    def __init__(self, cell, source = ''):
        self.macro_name = source.split('\n',1)[0].lstrip('```').strip()
        super().__init__(cell, source)

    def compile(self):
        super().compile('\n'.join(self.raw.strip().split('\n')[1:-1]))
# 
class IndentBlock( Block ):
    """An indented code block.  These code blocks are executed by the kernel.
    """
    def __init__(self, cell, source =''):
        self.macro_name = cell.env.kernel_name
        super().__init__(cell, source)
# 
class ParentCell(Block):
    """The main cell.
    """
    indent = 8
    filename = ""
    frontmatter = {}
    def __init__(self, env, source):
        self.env = env
        self.env.globals['this'] = self
        self.blocks = []
        self.raw = source
        if source.startswith('---'):
            tmp, self.raw = self.raw.lstrip('---').split('---',1)
            self.frontmatter  = yaml.load(tmp)
        self.render()

    def render(self):
        self.data = ""
        for ct, fence in enumerate(self.raw.split('```')):
            if (ct % 2) == 1:
                """ct=0 is false"""
                self.blocks.append(FenceBlock(self,"```{}```".format(fence)))
                self.data += self.blocks[-1].data
            else:
                rendered_markdown = self.env.preprocessor(fence)
                """Discover basic idented code blocks"""
                indent_blocks = rendered_markdown.replace('</code></pre>','<pre><code>').split('<pre><code>')
                for ct_md, block in enumerate(indent_blocks):
                    if (ct_md % 2) == 1:
                        self.blocks.append(IndentBlock(self,block))
                    else:
                        self.blocks.append(NormalBlock(self,block))
                    self.data += self.blocks[-1].data
        return self.data