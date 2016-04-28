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
    current_block=PyQueryUTF("""<section></section>""")
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
        self.current_block.html("""""")
        for block in self.blocks:
            if block.is_code and self.current_block.html():
                html+=super().weave(Block(self.current_block('section'),self.env))
                self.current_block.html("""""")
            if block.is_code:
                html+=super().weave(block)
            else:
                self.current_block.append(block.query.outerHtml())
        if self.current_block and self.current_block.html():
            html+=super().weave(Block(self.current_block('section'),self.env))
        return html
