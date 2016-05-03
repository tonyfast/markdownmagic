
# coding: utf-8

# # About `environment.py`
# 
# The jinja2 environment behind the literate magics.
from .macro import (
    Macros,
)
from jinja2 import (
    Template,
    Environment,
    DictLoader,
    FunctionLoader,
    PrefixLoader,
    PackageLoader,
    FileSystemLoader,
)
from mistune import (
    Markdown,
    Renderer,
)
# The `render` behavior will include the global contexts of the notebook and jinja2 environment.
class GlobalsTemplate(Template):
    def render(self, **data):
        """Attach globally variables to the render function.
        """
        env = self.environment
        data.update( env.globals )
        data.update( env.ip.user_ns  )
        return super().render(**data)
# `LiterateEnvironment` connects the cell contents with macros and template rending. 
class LiterateEnvironment( Environment ):
    from IPython import(
        get_ipython,
    )
    preprocessor = Markdown(renderer=Renderer(escape=False))
    def __init__(self, *args, **kwargs):
        super().__init__( loader = PrefixLoader({
                    'default': PackageLoader('literacy','/tmpl') ,
                    'macro': PackageLoader('literacy','/tmpl/macro') ,
                    'custom': DictLoader({}),
                }), *args, **kwargs)
        self.kernel_name = 'python'
# This template injects global variables into template.
        self.template_class = GlobalsTemplate
# 
        self.ip = get_ipython()
        
# Macros allow user defined behaviors and views of code including Markdown.
        self.macros = Macros(env=self)
        self.macro('python')
        self.macro('default')
        self.macro('markdown', html=self.preprocessor)
# This is how literate executes code.  The kernel exeucted before a template renders.
    @property
    def kernel(self):
        return self.ip.run_cell
# Conviently add a new macro.
    def macro(self, *args, **kwargs):
        return self.macros.macro(*args, **kwargs)
# A convenience function to render a list of blocks in a cell.
    def render_cell( self, cell ):
        cell.data = """"""
        for block in cell.blocks:
            cell.data += block.render()
        return cell