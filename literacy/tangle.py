from .blocks import (
    Block,
)
from .weave import (
    Weave,
)
class Tangle(Weave):
    def tangle(self):
        """Tangle non-code and code blocks."""
        self.data, self.blocks, self.templates = ["""""",[],[]]
        for child in self.query.children().items() if self.query.children() else self.query.items():
            self.blocks.append(Block(child,self.env))
        self.tangled.html(self.weave())
        return self.tangled.outer_html().decode('utf-8')
