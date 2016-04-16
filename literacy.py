import jinja2, IPython, mistune, haikunator
from pyquery import PyQuery
get_ipython = IPython.get_ipython

class LiterateEnvironment( jinja2.Environment ):
    """A Jinja Environment that can """
    ip = get_ipython()
    def _execute_python( self, code ):
        self.ip.run_cell(code)
        return """"""
    def __init__(self,default_lang='',lang_prefix='lang-', filter_prefix='execute_'):
        super().__init__(loader = jinja2.DictLoader({}))
        self.globals = {**self.globals,"default_lang": default_lang, "lang_prefix": lang_prefix, "filter_prefix": filter_prefix}
        self.filters[self.globals['filter_prefix']+'python'] = self._execute_python
        self.filters[self.globals['filter_prefix']+'javascript'] = lambda s: (s, None)
        
class Compiler:
    def execute(self, child, data={}, filter_name=""""""):
        lang = self.env.globals['default_lang']
        if child('code').attr('class'):
            lang = [c.lstrip(self.env.globals['lang_prefix']) for c in child('code').attr('class').split() if c.startswith(self.env.globals['lang_prefix'])][0]
        filter_name = self.env.globals['filter_prefix']+lang
        rendered = self.render(self._append_template(child.outerHtml()),data)
        if filter_name in self.env.filters:
            src = self.env.filters[filter_name](PyQuery(rendered).text())
            rendered += """<script>%s</script>"""%src if src else """"""
        return rendered
    
class Templates(Compiler):
    templates=[]
    @property
    def _current_template(self):
        return self.env.globals[self.env.globals['_current_name']]
    
    def _append_template(self, txt, data={}):
        template = self.env.from_string(txt)
        if '_current_name' in self.env.globals:
            self._current_template.templates.append(template)
        return self.render(template, data)
    
    def render(self,template, data={}):
        return self._current_template.templates[-1].render({
            **{k:getattr(self.env.ip.user_ns['__builtin__'],k) for k in dir(self.env.ip.user_ns['__builtin__']) if not k.startswith('_')},
            **self.env.ip.user_ns, **data,
        })

class Selection(IPython.display.HTML, Templates):
    def __init__(self,data):
        super().__init__( data ) 
        self.raw, self.query = [self.data, PyQuery(self.renderer(self.data))]
        self.data = self.parse(self.query)
    def parse( self, query=None, data={} ):
        query = self.query if not query else query
        html, block, self.templates = ["""""","""""",[]]
        for i, child in enumerate(query.children().items()):
            is_code = bool(child[0].tag in ['pre'])
            if not is_code:
                block += child.outerHtml()
            if is_code and block:
                html += '\n' + self._append_template(block, data)
                block = """"""
            if is_code:
                block += """<hr>%s<hr>"""%self.execute(child,data)
        if block:
            html += '\n' + self._append_template(block, data)
        return html
    
class Cell( Selection ):   
    renderer = mistune.Markdown( renderer=mistune.Renderer(escape=False))
    def __init__(self, data, name=haikunator.haikunate(), env=LiterateEnvironment()):
        self.env = env
        self.name = name
        self.env.globals[self.name] = self
        super().__init__(data)        

@IPython.core.magic.magics_class
class Literate(IPython.core.magic.Magics):
    def flush( self ):
        [self.env.globals.pop(k,None) for k in self.cells.keys()]
        self.cells = {}

    def __init__(self, **kwargs):
        self.env, self.cells = [LiterateEnvironment(**kwargs), {}]
        super().__init__()
        self.env.ip.register_magics(self)

    @IPython.core.magic.cell_magic 
    @IPython.core.magic_arguments.magic_arguments()
    @IPython.core.magic_arguments.argument( "name", default=None, nargs="?", help="""Name of local variable to set to parsed value""")
    @IPython.core.magic_arguments.argument("-n", "--nodisplay", default=False, action="store_true", help="""Show the output""")
    def literate(self, line, cell):
        line = line.strip()
        args = IPython.core.magic_arguments.parse_argstring(self.literate, line)
        define_global = True
        if not args.name:
            define_global = False
            args.name = haikunator.haikunate(delimiter='_',tokenlength=0)
        self.env.globals['_current_name'] = args.name
        display = Cell( cell, args.name, self.env )
        self.cells[args.name] = display
        if define_global:
            self.env.ip.user_ns[args.name] = display
        if not args.nodisplay:
            return display
