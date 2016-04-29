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
        tokens, comment = [{},""]
        if block.is_code:
            code=self.render(block.query('code').html())
            if block.handler:
                for language, caller in block.handler.items():
                    tokens[language] = caller(code) if caller else None
                    if tokens[language]:
                        comment="""<!--executed: {}-->""".format(code)
            if not 'html' in tokens:
                tokens['html'] = block.query.text(code).outer_html()
        else:
            tokens.update({
                'html': self.render(block.content)
            })
        if comment:
            tokens['html']+="""<!--execute: {}-->""".format(tokens['html'])
        return self.env.get_template('weave_template').render(**tokens)

class Weave(Tokenizer):
    def __init__(self):
        self.env.loader.mapping.update({
            'weave_template': """
            {% if css %}<style>{{css}}</style>{% endif %}
            {% if html %}{{html}}{% endif %}
            {% if js %}<script>{{js}}</script>{% endif %}
            """,
        })

    def weave(self, _html=""):
        """Weave separate blocks of html and code together."""
        for block in self.blocks:
            if block.is_code and _html:
                self.data+=super(Weave,self).weave(Block(PyQueryUTF(_html),self.env)).strip()
                _html=""""""
            if block.is_code:
                self.data+=super(Weave,self).weave(block).strip()
            else:
                _html+=block.query.outer_html().strip()
        if _html:
            self.data+=super(Weave,self).weave(Block(PyQueryUTF(_html),self.env)).strip()
        return self.data
