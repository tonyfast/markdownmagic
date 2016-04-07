from jinja2 import (Environment, DictLoader, Template,)
import IPython, mistune

class ParserUtils():
        
    def _split_txt(self, txt,delimiter):
        output = []
        body = [];
        for line in txt.splitlines():
            if line.lstrip().startswith(delimiter*3):
                output.append('\n'.join(body))
                body = []
                output.append( line )
            else:
                body.append(line)
        if body:
            output.append('\n'.join(body))
        return output

    def _tokenize_code(self, section):
        delimiter=self.code_delimiter
        output = []
        blocks = self._split_txt(section['body'],delimiter)
        for i, (divider, block) in enumerate(zip([delimiter,*blocks[1::2]],blocks[0::2])):
            output.append({
                    'type': 'md' if (i % 2) == 0 else 'code',
                    'body': block if (i % 2) == 0 else divider +'\n'+ block + delimiter*3,
                    'level': divider.find(delimiter)
                })
        return output

    def _tokenize_md(self, txt):
        delimiter = self.section_delimiter
        sections = self._split_txt(txt,delimiter)
        output = []
        if delimiter*3 in sections[0] and len(sections[0].split('\n'))==1:
            dividers = sections[::2]        
            start_index = 1
        else:
            dividers = [ delimiter*3, *sections[1::2] ]
            start_index = 0
        for i, (divider, section) in enumerate(zip(dividers,sections[start_index::2])):
            output.append({
                    'type':'md',
                    'body': delimiter*3 + '\n' + section,
                    'level': divider.find(delimiter)
                })

        if txt.lstrip('\n').startswith(delimiter):
            if not sections[0]:
                output.pop(0)
            output[0]['type'] = 'yaml'
            output[0]['body'] = output[0]['body'].lstrip('---')
        return output

    def _split_md_code( self, txt ):
        output=[]
        sections = self._tokenize_md(txt)
        for section in sections:
            if '```' in section['body']:
                output.extend( self._tokenize_code(section))
            else:
                output.append(section)
        return output
    
class LiterateParser(ParserUtils ):
    import yaml, mistune
    code_delimiter = '`'
    section_delimiter = '-'
    def __init__(self,env,renderer):
        self.env = env
        self.literate_renderer = renderer
        super(ParserUtils, self).__init__()
        
    def tokenize(self, txt):
        self.tokens = self._split_md_code( txt )
    
    def parse(self, txt):
        self.tokenize(txt)
        parsed = """"""
        for token in self.tokens:
            if token['type'] in ['yaml']:
                self.env.globals[self.env.globals['_current_name']].frontmatter = self.yaml.load(
                    self.env.from_string( token['body'] ).render(**self.env.ip.user_ns)
                )
            else:
                parsed += self.literate_renderer(token['body'])
        return parsed

import jinja2

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

from haikunator import haikunate

class TemplateMath(jinja2.Template):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    def __add__(self, payload):
        if payload in ['*']:
            payload = self.ip.user_ns
        return self.render(**payload)
    def __mul__(self, payload):
        return '\n'.join([self + load for load in payload])
    
class LiterateEnvironment( jinja2.Environment ):
    ip = get_ipython()
    _filter_prefix = 'execute_'
    def _execute_python( self, code ):
        self.ip.run_cell(code)
        return """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters[self._filter_prefix+'python'] = self._execute_python
        self.filters[self._filter_prefix+'javascript'] = lambda s: s
        self.globals['frontmatter'] = {}
        self.template_class = TemplateMath
        
class LiterateBlockLexer(mistune.BlockLexer):
    def _render( self, m ):
        name = self.env.globals['_current_name']
        current = self.env.globals[name]
        template = self.env.from_string(m)
        current.templates.append( template )
        return template + {**current.frontmatter, **self.env.ip.user_ns} 

    def __init__( self, env = LiterateEnvironment(loader=DictLoader({})), *args, **kwargs ):
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
                if lang.startswith('%%'):   
                    token['text'] = lang + '\n' + token['text']
                    lang = lang.lstrip('%%')
                    filter_name = self.env._filter_prefix+'python'
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
                if 'text' in token and token['text']:
                    token['text'] = self._render(token['text'])
                    updated_tokens.append(token)
        tokens=updated_tokens
        return tokens

class LiterateMarkdown( mistune.Markdown ):
    def __init__( self, env=LiterateEnvironment(), *args, **kwargs ):
        self.env = env        
        super().__init__( block=LiterateBlockLexer(env=self.env), *args, **kwargs )       
        
@magics_class
class Literacy(Magics):
    """
    Literate Python in using Markdown.
    Example:
        %%markdown
        # This is a title with {{data}}
    """
    def flush( self ):
        for k in self.templates.keys():
            del self.env.globals[k]
        self.templates = {}

    def __init__(self):
        env = self.env = LiterateEnvironment(loader=DictLoader({}))
        self.renderer = LiterateMarkdown(env=env,renderer=Renderer(escape=False))
        self.parser = LiterateParser(env,self.renderer)
        self.templates = {}
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
    def literate(self, line, cell):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.literate, line)
        display = IPython.display.HTML( cell )
        if args.name:
            self.env.ip.user_ns[args.name] = display
        else:
            args.name = haikunate(delimiter='_',tokenlength=0)
        self.env.globals['_current_name'] = args.name
        self.templates[args.name] = self.env.globals[args.name] = display
        display.name = args.name
        display.frontmatter = {}
        display.templates = []
        display.raw = display.data
        display.data = self.parser.parse(display.raw)
        try:
            pass
        except Exception as err:
            print(1,err)
            return
        if not args.nodisplay:
            return display
