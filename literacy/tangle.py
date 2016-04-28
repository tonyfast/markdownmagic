from .blocks import (
    Block,
)
from .weave import (
    Weave,
)
import yaml

class Tangle(Weave):
    def tangle(self):
        """Tangle non-code and code blocks."""
        self.blocks=[]
        for child in self.query.children().items() if self.query.children() else self.query.items():
            self.blocks.append(Block(child,self.env))
        return self.weave()
class Processor(Tangle):
    """
    Slice front matter, tangle templates, and weave the code.
    """
    templates=[]
    def __init__(self, raw):
        self.raw, self.frontmatter = [raw, {}]
        """Split FrontMatter"""
        if raw.startswith('---\n'):
            frontmatter, content = self.raw.lstrip('---').strip().split('---',1)
            if hasattr( self, 'widgets'):
                self.raw=content
            self.frontmatter=yaml.load(self.render(frontmatter))
        super(Processor,self).__init__()
