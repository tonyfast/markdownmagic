from .tangle import (
    Tangle,
)

class PreProcessor(Tangle):
    """
    Slice front matter, tangle templates, and weave the code.
    """
    def __init__(self, raw):
        self.raw, self.frontmatter = [raw, {}]
        """Split FrontMatter"""
        if raw.startswith('---\n'):
            frontmatter, content = self.raw.lstrip('---').strip().split('---',1)
            if hasattr( self, 'widgets'):
                self.raw=content
            self.frontmatter=yaml.load(self.render(frontmatter))
        super(PreProcessor,self).__init__()
