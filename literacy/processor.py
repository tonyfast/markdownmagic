from .tangle import (
    Tangle,
)
from .query import (
    PyQueryUTF,
)
import yaml
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

    def render(self,txt, data={},template=None,render_template=False):
        if not template:
            self.templates.append(self.env.from_string(txt))
        if self.env.globals['render_template'] or render_template:
            data={k:getattr(self.env.ip.user_ns['__builtin__'],k) for k in dir(self.env.ip.user_ns['__builtin__']) if not k.startswith('_')}
            data.update(self.env.ip.user_ns)
            data.update(self.frontmatter)
            data.update(data)
            return self.templates[-1].render(**data)
        return txt

    @property
    def query(self):
        """"""
        return PyQueryUTF(self.env.renderer(self.raw))
