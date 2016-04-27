from .weave import (
    Weave,
)
from pyquery import (
    PyQuery,
)
import yaml

class TangleClient(Weave):
    """
    Tokenize the HTML representation of a template.
    """
    def tangle(self,code):
        return {
                'html': code,
            }
class TangleKernel(TangleClient):
    """
    Tokenize executable code and html representation.
    """
    def tangle(self,html="""""", element=None):
        tokens={'html':""""""}
        if element and element[0].tag in ['pre']:
            lang=self._get_lang(element)
            if lang and lang in self.env.globals['callback']:
                tokens.update(self.env.globals['callback'][lang](self.render(element.text())))
            tokens['html'] = self.env.get_template('weave_code').render(code=self.render(element.text()))+tokens['html']
        else:
            tokens=super(TangleKernel,self).tangle(self.render(html))
        return self.weave(**tokens)


class Tangle(TangleKernel):
    @property
    def query(self):
        """"""
        return PyQuery(self.env.renderer(self.raw))

    def tangle(self):
        data, block, self.templates = ["""""","""""",[]]
        for child in self.query.children().items() if self.query.children() else self.query.items():
            tagName=child[0].tag
            is_code = bool(tagName in ['pre'])
            if not is_code:
                block += child.outerHtml()
            if is_code and block:
                data += '\n' + super(Tangle,self).tangle(html=block)
                block = """"""
            if is_code:
                data+=super(Tangle,self).tangle(element=child)
        else:
            data += '\n' + super(Tangle,self).tangle(html=block) if block else """"""
        # Wrap an id around the output if there is an ID provided.  Tooltips get easier.``
        self.data=self.tangled.html(data).outerHtml()
        return self.data

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
    def _get_lang(self,child):
        """Get language of the current code block"""
        lang = self.env.globals['default_lang']
        if child('code').attr('class'):
            lang = [c.lstrip(self.env.globals['lang_prefix']) for c in child('code').attr('class').split() if c.startswith(self.env.globals['lang_prefix'])][0]
        return lang
