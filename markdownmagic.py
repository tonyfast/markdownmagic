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
    Template,
)

import mistune
from mistune import (
    Renderer,
)

import yaml

class TemplateMath(Template):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    def __add__(self, payload):
        if payload in ['*']:
            payload = self.ip.user_ns
        return self.render(**payload)
    def __mul__(self, payload):
        return '\n'.join([self + load for load in payload])
    
class LiterateEnvironment( Environment ):
    ip = get_ipython()
    _filter_prefix = 'execute_'
    def _execute_python( self, code ):
        self.ip.run_cell(code)
        return """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters[self._filter_prefix+'python'] = self._execute_python
        self.filters[self._filter_prefix+'javascript'] = lambda s: s
        self.template_class = TemplateMath
        
class LiterateBlockLexer(mistune.BlockLexer):
    def _render( self, m, data={},frontmatter={}):
        template = self.env.from_string(m, template_class=TemplateMath)
        return template + {**frontmatter, **self.env.ip.user_ns, **data} 

    def __init__( self, env = LiterateEnvironment(), *args, **kwargs ):
        self.env = env        
        super().__init__( *args, **kwargs )   

    def parse(self, text, *args, **kwargs):
        self.tokens = []
        tokens = super().parse(text, *args, **kwargs)
        updated_tokens= []
        for token in tokens:
            if token['type'] in ['code']:
                src = """"""
                lang = token['lang'] if token['lang'] else ''
                filter_name = self.env._filter_prefix+lang
                updated_tokens.extend([{'type': 'hrule'}, token, {'type': 'hrule'}])
                if filter_name in self.env.filters:
                    token['text'] = self._render(token['text'])
                    src = self.env.filters[filter_name](token['text'])
                    updated_tokens.append({
                            'type': 'open_html', 
                            'tag': 'script', 
                            'extra': " type='text\/javascript'", 
                            'text': src
                        })
            else:
                token['text'] = self._render(token['text'])
                updated_tokens.append(token)
        tokens=updated_tokens
        return tokens

class LiterateMarkdown( mistune.Markdown ):
    def __init__( self, env=LiterateEnvironment(), *args, **kwargs ):
        self.env = env
        super().__init__( block=LiterateBlockLexer(env=self.env), *args, **kwargs )        

@magics_class
class environment(Magics):
    """
    Literate Python in using Markdown.
    Example:
        %%markdown
        # This is a title with {{data}}
    """
    def __init__(self, env=LiterateEnvironment(loader=DictLoader({}))):
        self.env = env
        self.renderer = LiterateMarkdown(env=env,renderer=Renderer(escape=False))
        super().__init__()
        self.env.ip.register_magics(self)

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
        help="""Show the output"""
    )
    def markdown(self, line, cell):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.markdown, line)
        try:
            # Literate python execution
            display = IPython.display.HTML( self.renderer( cell ))
        except Exception as err:
            print(err)
            return
        if args.name:
            self.ip.user_ns[args.name] = display
        if not args.nodisplay:
            return display
