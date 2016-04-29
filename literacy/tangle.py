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
        self.data, self.blocks =["",[]]
        children = self.query.children()
        if len(children)==0 or self.query[0].tag in ['pre']:
            """One line cell case"""
            self.blocks.append(Block(PyQueryUTF(self.query),self.env))
        else:
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
        """Split FrontMatter"""
        if raw.startswith('---\n'):
            frontmatter, self.raw = self.raw.lstrip('---').strip().split('---',1)
            self.frontmatter.update(yaml.load(self.render(frontmatter)))
        self.query = PyQueryUTF(self.env.renderer(self.raw))
        super(Processor,self).__init__()
