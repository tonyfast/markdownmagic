"""# About `environment.py`

The jinja2 environment behind the literate magics.
"""

from .macro import (
    Macros,
)
from jinja2 import (
    Template,
    Environment,
    DictLoader,
    ChoiceLoader,
    PackageLoader,
    FileSystemLoader,
)
from mistune import (
    Markdown,
    Renderer,
)
class GlobalsTemplate(Template):
    def render(self, **data):
        """Attach globally variables to the render function.
        """
        env = self.environment
        data.update( env.globals )
        data.update( env.ip.user_ns  )
        return super(GlobalsTemplate, self).render(**data)

class LiterateEnvironment( Environment ):
    from IPython import(
        get_ipython,
    )
    preprocessor = Markdown(renderer=Renderer(escape=False))
    filters_directory = '_filters'
    macros_directory = '_macros'
    templates_directory = '_includes' # because jekyll
    def __init__(self, *args, **kwargs):
        super(LiterateEnvironment, self).__init__( loader = ChoiceLoader([
                    DictLoader({}),
                    FileSystemLoader(self.templates_directory),
                    PackageLoader('literacy', 'tmpl'),
                ]), *args, **kwargs)
        self.kernel_name = 'python'
        self.template_class = GlobalsTemplate
        self.ip = get_ipython()
        self.macros = Macros(env=self)
        self.macro('python')
        self.macro('default')
        self.macro('markdown', html=self.preprocessor)

    @property
    def kernel(self):
        return self.ip.run_cell

    def macro(self, *args, **kwargs):
        return self.macros.macro(*args, **kwargs)

    def render_cell( self, cell ):
        cell.data = """"""
        for block in cell.blocks:
            cell.data += block.render()
        return cell
