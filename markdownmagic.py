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

from pyquery import PyQuery


import yaml

__version_info__ = (0, 1, 0)
__version__ = '.'.join(map(str, __version_info__))


class LiterateMarkdown(mistune.Markdown):
    _filter_prefix = 'execute_'
    def __init__( self, env=Environment(), *args, **kwargs ):
        self.env = env
        super().__init__( *args, **kwargs )
    def output_code(self):
        txt, lang = [
            self.token['text'], 
            self.token['lang']
        ]
        lang = lang if lang else ''
        output = """<hr>%s<hr>"""%super().output_code()
        src = """"""
        filter_name = self._filter_prefix+lang
        if filter_name in self.env.filters:
            src = self.env.filters[filter_name](txt)
        if isinstance(src, str) and src:
            output += """<script>%s</script>"""%src
        return  output 

class MarkdownerTemplate(IPython.core.display.HTML):
    def __init__(
        self,
        cell,
        frontmatter="""""",
        *args,
        **kwargs
    ):
        self.cell = cell
        self.env = self.cell.env
        self.ip = self.cell.ip
        self.src = """"""
        self.renderer = LiterateMarkdown(env=self.env,renderer=Renderer(escape=False) )
        self.frontmatter = frontmatter
        super().__init__(*args, **kwargs)
        if self.frontmatter:
            self.frontmatter = yaml.load(
                self.env.from_string(
                    self.frontmatter
                ).render(self.ip.user_ns)
            )
            self.frontmatter = self.frontmatter if self.frontmatter else {}
        else:
            self.frontmatter = {}
        self.template = self.env.from_string(self.data)

    def __add__(self, payload):
        if payload in ['*']:
            payload = self.ip.user_ns
        return self.template.render(**payload)

    def __mul__(self, payload):
        return '\n'.join([self.template.render(**load) for load in payload])

    def _repr_html_(self):
        return self.renderer( self + {**self.frontmatter, **self.ip.user_ns} )
        
@magics_class
class environment(Magics):
    """
    Literate Python in using Markdown.

    Example:

        %%markdown
        # This is a title with {{data}}
    """
    ip = get_ipython()

    def __init__(self, env=Environment(loader=DictLoader({}))):
        self.env = env
        ip = self.ip
        self.env.filters['execute_python'] = lambda s: ip.run_cell(s)
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
    def markdown(self, line, cell):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.markdown, line)
        if cell.startswith('---'):
            frontmatter, cell = cell.lstrip('---').split('---', 1)
        else:
            frontmatter = {}
        try:
            # Literate python execution
            display = MarkdownerTemplate(
                self,
                frontmatter=frontmatter,
                data=cell
            )
        except Exception as err:
            print(err)
            return

        if args.name:
            self.ip.user_ns[args.name] = display
        return display
