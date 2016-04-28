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
    def __init__(self,default_lang='python',lang_prefix='lang-', render_template=True,*args,**kwargs):
        super(LiterateEnvironment,self).__init__(loader=DictLoader({}))
        self.globals.update({
            "default_lang": default_lang,
            "render_template": render_template,
            "lang_prefix": lang_prefix,
            "callback": {
                'python': lambda code: {
                    'python': self.ip.run_cell(code),
                },
                'html': lambda code: {
                    'html': code,
                },
                'js': lambda code: {
                    'js': code,
                },
                'css': lambda code: {
                    'css': code,
                },
            }})
