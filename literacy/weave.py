from .blocks import (
    Block,
)
from .query import (
    PyQueryUTF,
)
class Tokenizer(object):
    def weave(self,block):
        """
        Weave executable, html, css, and javascript codes together.
        """
        tokens={'html':""""""}
        if block.is_code:
            content=self.render(block.content)
            if block.callback:
                for language, caller in block.callback.items():
                    tokens[language] = caller(content)
            tokens.update({
                'html': self.env.get_template('weave_code').render(code=self.render(content))+tokens['html'],
            })
        else:
            tokens.update({
                'html': self.render(block.content)
            })
        return self.env.get_template('weave_template').render(**tokens)

class Weave(Tokenizer):
    def __init__(self):
        self.env.loader.mapping.update({
            'weave_code': """<br><pre><code>{{code|e}}</code></pre><br>""",
            'weave_template': """
            {% if css %}<style>{{css}}</style>{% endif %}
            {% if html %}{{html}}{% endif %}
            {% if js %}<script>{{js}}</script>{% endif %}
            """,
        })

    def weave(self,html=""""""):
        """Weave separate blocks of html and code together."""
        self.data,_html=["",""]
        for block in self.blocks:
            if block.is_code and _html:
                self.data+=super(Weave,self).weave(Block(PyQueryUTF(_html),self.env)).strip()
                _html=""""""
            if block.is_code:
                self.data+=super(Weave,self).weave(block).strip()
            else:
                _html+=block.query.outer_html()
        if _html:
            self.data+=super(Weave,self).weave(Block(PyQueryUTF(_html),self.env)).strip()
        return self.data
