import jinja2, IPython, mistune, haikunator, yaml
from pyquery import PyQuery

class LiterateEnvironment( jinja2.Environment ):
    ip = get_ipython()
    _filter_prefix = 'execute_'
    def _execute_python( self, code ):
        self.ip.run_cell(code)
        return """""", {}

    def __init__(self, *args, **kwargs):
        self.loader = jinja2.DictLoader({})
        super().__init__(*args, **kwargs)
        self.filters[self._filter_prefix+'python'] = self._execute_python
        self.filters[self._filter_prefix+'javascript'] = lambda s: (s, None)


class LiterateDisplay( IPython.display.HTML):

    renderer = mistune.Markdown( renderer=mistune.Renderer(escape=False))
    default_lang = 'python'
    templates = []
    def __init__(self, data, name=haikunator.haikunate(), env=LiterateEnvironment(), *args, **kwargs):
        self.env = env
        super().__init__(data, *args, **kwargs)
        self.name = name
        self.env.globals[self.name] = self
        self.raw = self.data
        self.query = PyQuery(self.renderer(self.raw))
        self.parse()

    @property
    def current_object(self):
        return self.env.globals[self.env.globals['_current_name']]

    def append_template( self, txt):
        template = self.env.from_string(txt)
        if '_current_name' in self.env.globals:
            self.current_object.templates.append(template)
        return self.render(template)

    def render(self,template ):
        return self.current_object.templates[-1].render(**self.env.ip.user_ns)

    def execute(self,child):
        lang = self.default_lang if self.default_lang else """"""
        if child('code').attr('class'):
            lang = [c.lstrip('lang-') for c in child('code').attr('class').split() if c.startswith('lang-')][0]
        filter_name = self.env._filter_prefix+lang
        rendered = self.render(self.append_template(child.outerHtml()))
        if filter_name in self.env.filters:
            src, data = self.env.filters[filter_name](child.text())
            if src:
                rendered += """<script>%s</script>"""%src
            if data:
                for key, value in data.items():
                    setattr(self.current_object, key, value )
        return rendered

    def parse( self ):
        html, block = ["""""",""""""]
        children=self.query.children()
        for i, child in enumerate(children.items()):
            is_code = bool(child[0].tag in ['pre'])
            if not is_code:
                block += child.outerHtml()
            if is_code and block:
                html += '\n' + self.append_template(block)
                block = """"""
            if is_code:
                block += """<hr>%s<hr>"""%self.execute(child)
        if block:
            html += '\n' + self.append_template(block)
        self.data = html


@IPython.core.magic.magics_class
class Literate(IPython.core.magic.Magics):
    def flush( self ):
        for k in self.templates.keys():
            del self.env.globals[k]
        self.templates = {}

    def __init__(self):
        env = self.env = LiterateEnvironment()
        self.templates = {}
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
        display = LiterateDisplay( cell, args.name, self.env )
        self.templates[args.name] = display

        if define_global:
            self.env.ip.user_ns[args.name] = display
        if not args.nodisplay:
            return display
