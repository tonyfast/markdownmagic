from .weave import (
    Weave,
)
from pyquery import (
    PyQuery,
)
import yaml

class TangleClient(Weave):
    def tangle(self,code):
        return {
                'html': code,
            }
class TangleKernel(TangleClient):
    def tangle(self,html="""""", child=None,lang=None,output={}):
        if lang and lang in self.env.globals['callback']:
            output = self.env.globals['callback'][lang](self.render(child.text()))
        else:
            output=super().tangle(self.render(html))
        return self.weave(**output)

class Tangle(TangleKernel):
    templates=[]
    def __init__(self, raw):
        self.raw, self.frontmatter = [raw, {}]
        """Split FrontMatter"""
        if raw.startswith('---\n'):
            tmp, self.raw = self.raw.lstrip('---').strip().split('---',1)
            self.frontmatter=yaml.load(self.render(tmp))
        super().__init__()

    @property
    def query(self):
        return PyQuery(self.env.renderer(self.raw))

    def tangle(self):
        self.data, block, self.templates = ["""""","""""",[]]
        for child in self.query.children().items():
            is_code = bool(child[0].tag in ['pre'])
            if not is_code:
                block += child.outerHtml()
            if is_code and block:
                self.data += '\n' + super().tangle(block)
                block = """"""
            if is_code:
                self.data+=super().tangle(child.text(),child=child,lang=self._get_lang(child))
        else:
            self.data += '\n' + super().tangle(block) if block else """"""
            return self.data

    def render(self,txt, data={},render_template=False):
        self.templates.append(self.env.from_string(txt))
        if self.env.globals['render_template'] or render_template:
            return self.templates[-1].render({
                # Add builtins to the template namespace
                **{k:getattr(self.env.ip.user_ns['__builtin__'],k) for k in dir(self.env.ip.user_ns['__builtin__']) if not k.startswith('_')},
                # Add variables from the global namespace,
                **self.env.ip.user_ns,
                # Add front matter as private data, access globals through user_ns or globals.
                **self.frontmatter,
                # Any other data.
                **data,

            })
        return txt
    def _get_lang(self,child):
        """Get language of the current code block"""
        lang = self.env.globals['default_lang']
        if child('code').attr('class'):
            lang = [c.lstrip(self.env.globals['lang_prefix']) for c in child('code').attr('class').split() if c.startswith(self.env.globals['lang_prefix'])][0]
            return lang
