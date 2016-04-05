from __future__ import print_function

from IPython import get_ipython

import IPython

from IPython.core import magic_arguments

from IPython.core.magic import (
    Magics,
    magics_class,
    cell_magic,
)

from jinja2 import (
    Environment,
    DictLoader,
)

import mistune
from mistune import (
    Renderer,
)

import yaml

class LiterateMarkdown(mistune.Markdown):
    _filter_prefix = 'execute_'
    def render( self, m, data={}):
        self.template = self.env.from_string(m)
        return self.template.render({**self.frontmatter, **self.ip.user_ns, **data})
    def _execute_python( self, code ):
        self.ip.run_cell(code)
        return """"""
    def __init__( self, *args, **kwargs ):
        self.env = jinja2.Environment()
        self.env.filters['execute_python'] = self._execute_python
        self.env.filters['execute_javascript'] = lambda s: s
        self.ip = IPython.get_ipython()
        super().__init__( *args, **kwargs )   
    
    def __call__(self, text, data={}):
        if text.startswith('---'):
            frontmatter, text = text.lstrip('---').split('---', 1)
            self.frontmatter = yaml.load(
                self.render(frontmatter)
            )
        else:
            self.frontmatter = {}
        text = self.render(text, data )
        return self.parse(text), self.template
                          
    def output_code(self):
        src = """"""
        lang = self.token['lang'] if self.token['lang'] else ''
        output = """<hr>%s<hr>"""%super().output_code()
        
        filter_name = self._filter_prefix+lang
        if filter_name in self.env.filters:
            src = self.env.filters[filter_name](self.token['text'])
        if isinstance(src, str) and src:
            """If the filter outputs a script then stick it in a script tag."""
            output += """<script>%s</script>"""%src
        return  output 

class DisplayTemplate(IPython.display.HTML):
    def __init__( self,  *args, renderer=mistune.markdown, **kwargs ):
        self.renderer = renderer
        super().__init__(*args, **kwargs )
    def _repr_html_(self):
        data, self.template = self.renderer( self.data )
        return data
    
@magics_class
class environment(Magics):
    """
    Literate Python in using Markdown.
    Example:
        %%markdown
        # This is a title with {{data}}
    """
    def _execute_python( self, code ):
        self.ip.run_cell(code)
        return """"""

    ip = get_ipython()
    def __init__(self, env=Environment(loader=DictLoader({}))):
        self.env = env
        self.env.filters['execute_python'] = lambda s: self._execute_python(s)
        self.env.filters['execute_javascript'] = lambda s: s
        self.renderer = LiterateMarkdown(env=self.env,renderer=Renderer(escape=False) )
        self.display = DisplayTemplate
        super().__init__()
        self.ip.register_magics(self)

    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "name",
        default=None,
        nargs="?",
        help="""Name of local variable to set to parsed value"""
    )
    @magic_arguments.argument(
        "-n", "--nodisplay",
        default=False,
        action="store_true",
        help="""set variable in window._yaml"""
    )
    def markdown(self, line, cell):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.markdown, line)
        try:
            # Literate python execution
            display = self.display( cell,renderer=self.renderer)
        except Exception as err:
            print(err)
            return
        if args.name:
            self.ip.user_ns[args.name] = display
        if not args.nodisplay:
            return display
