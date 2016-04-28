from jinja2 import (
    Environment,
    DictLoader,
)
from IPython import (
    get_ipython,
)
from mistune import (
    Markdown,
    Renderer,
)

class LiterateEnvironment( Environment ):
    """A Jinja Environment and the current notebook state."""
    ip = get_ipython()
    renderer=Markdown(renderer=Renderer(escape=False))
    def __init__(self,default_language='python',language_prefix='lang-', render_template=True):
        super(LiterateEnvironment,self).__init__(
            loader=DictLoader({
                'default': """{{cell.data}}""",
                'default_div': """
                    <div id="{{cell.name}}" class='{{cell.classes.strip('"').strip("'")}}'>
                    {{cell.data}}
                    </div>""",
            }),
        )
        self.default_language, self.render_template, self.language_prefix = [
            default_language, render_template, language_prefix,
        ]
        self.languages = {
            'python': {
                'python': self.ip.run_cell,
            },
            'html': {
                'html': lambda s: s,
            },
            'js': {
                'js': lambda s: s,
            },
            'css': {
                'css': lambda s: s,
            },
        }
