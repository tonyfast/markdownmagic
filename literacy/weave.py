from .blocks import (
    Block,
)
from .query import (
    PyQueryUTF,
)
class Tokenize(object):
    def weave(self,block):
        """
        Weave executable, html, css, and javascript codes together.
        """
        tokens={'html':""""""}
        if block.is_code:
            code=self.render(block.code)
            if block.callback:
                tokens.update(block.callback(code))
            tokens.update({
                'html': self.env.get_template('weave_code').render(code=self.render(code))+tokens['html'],
            })
        else:
            tokens.update({
                'html': self.render(block.code)
            })
        return self.env.get_template('weave_template').render(**tokens)

class Weave(Tokenize):
    current_block=PyQueryUTF("""<section></section>""").parent().html("""""")
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
        html,_html=["",""]
        for block in self.blocks:
            if block.is_code and html:
                html+=super().weave(Block(PyQueryUTF(_html),self.env))
                _html=""""""
            if block.is_code:
                html+=super().weave(block)
            else:
                _html+=block.query.outer_html()
        else:
            if _html:
                html+=super().weave(Block(PyQueryUTF(_html),self.env))
        return html
