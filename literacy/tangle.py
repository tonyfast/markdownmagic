import yaml
from .blocks import (
    Block,
)
from .weave import (
    Weave,
)
from .query import (
    PyQueryUTF,
)
class Tangle(Weave):
    def tangle(self):
        """Tangle non-code and code blocks."""
        children=self.query.children()
        children = self.query if len(children)==1 else children
        for child in children.items():
            self.blocks.append(Block(child,self.env))
        return self.weave()
class Processor(Tangle):
    """
    Slice front matter, tangle templates, and weave the code.
    """
    templates=[]
    def __init__(self, raw):
        self.raw, self.frontmatter = [raw, {}]
        self.query = PyQueryUTF(self.env.renderer(self.raw))
        """Split FrontMatter"""
        if raw.startswith('---\n'):
            frontmatter, content = self.raw.lstrip('---').strip().split('---',1)
            if hasattr( self, 'widgets'):
                self.raw=content
            self.frontmatter=yaml.load(self.render(frontmatter))
        super(Processor,self).__init__()
