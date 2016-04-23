import jinja2, IPython, mistune
from pyquery import PyQuery
import yaml
get_ipython = IPython.get_ipython

class LiterateEnvironment( jinja2.Environment ):
    """A Jinja Environment that can """
    ip = get_ipython()
    def __init__(self,default_lang='python',lang_prefix='lang-', render_data=True):
        super().__init__(loader = jinja2.DictLoader({}))
        self.globals = {
            **self.globals,
            "default_lang": default_lang, "lang_prefix": lang_prefix, 'render_data':render_data
        }
        self.globals['callback']={
            'python': lambda code: {
                'python': self.ip.run_cell(code),
            },
            'html': lambda code: {'html': code}, 'js': lambda code: {'js': code}, 'css': lambda code: {'css': code},
        }
class Weave():
    def __init__(self):
        if not 'weave_template' in self.env.loader.mapping:
            self.env.loader.mapping['weave_template'] = """{% if css %}<style>{{css}}</style>{% endif %}{% if html %}{{html}}<hr>{% endif %}{% if js %}<script>{{js}}</script>{% endif %}"""
    def weave(self,**kwargs):
        return self.env.get_template('weave_template').render(
            {**{'html':'','js':'','css':''},**kwargs}
        )
class TangleClient(Weave):
    def tangle(self,code):
        return {
                'html': code,
            }
class TangleKernel(TangleClient):
    def tangle(self,html="""""", child=None,lang=None,output={}):
        if lang and lang in self.env.globals['callback']:
            html=self.render(child.outerHtml())
            output = self.env.globals['callback'][lang](self.render(child.text()))
        else:
            html=self.render(html)
        return self.weave(**{**output,**super().tangle(html)})
class Tangle( TangleKernel):
    templates=[]
    def __init__(self, raw):
        self.raw, self.frontmatter = [raw, {}]
        if raw.startswith('---\n'):
            tmp, self.raw = self.raw.lstrip('---').strip().split('---',1)
            self.frontmatter=yaml.load(self.render(tmp))
        super().__init__()
    @property
    def query(self):
        return PyQuery(self.renderer(self.raw))
    def _get_lang(self,child):
        lang = self.env.globals['default_lang']
        if child('code').attr('class'):
            lang = [c.lstrip(self.env.globals['lang_prefix']) for c in child('code').attr('class').split() if c.startswith(self.env.globals['lang_prefix'])][0]
        return lang
    def tangle(self):
        html, block, self.templates = ["""""","""""",[]]
        for child in self.query.children().items():
            is_code = bool(child[0].tag in ['pre'])
            if not is_code:
                block += child.outerHtml()
            if is_code and block:
                html += '\n' + super().tangle(block)
                block = """"""
            if is_code:
                html+=super().tangle(child.text(),child=child,lang=self._get_lang(child))
        else:
            html += '\n' + super().tangle(block) if block else """"""
        return html
    def render(self,txt, data={},render_data=False):
        template = self.env.from_string(txt)
        self.templates.append(template)
        if self.env.globals['render_data'] or render_data:
            return template.render({
                **{k:getattr(self.env.ip.user_ns['__builtin__'],k) for k in dir(self.env.ip.user_ns['__builtin__']) if not k.startswith('_')},
                **self.env.ip.user_ns, **data, **self.frontmatter,
            })
        return txt
class Cell(Tangle):
    renderer=mistune.Markdown(renderer=mistune.Renderer(escape=False))
    def __init__(self, raw, name="""_current_cell""", env=LiterateEnvironment()):
        self.env, self.name = [env, name]
        self.env.globals[self.name] = self
        super().__init__(raw)

class StaticCell(Cell, IPython.display.HTML):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.data=self.tangle()
    def display(self):
        return self

def widgetize( cell, auto=False ):
    if not hasattr(cell,'widgets'):
        cell.widgets={}
    if not 'html' in cell.widgets:
        cell.widgets['html']=ipywidgets.HTML(cell.data)
    def update_html(*args,**kwargs):
        cell.widgets['html'].value = cell.tangle()
    if not 'trigger' in cell.widgets:
        cell.widgets['trigger']=ipywidgets.Button(description="""Update cell""")
        cell.widgets['trigger'].on_click(callback=update_html)
    def update_frontmatter(change,*args,**kwargs):
        cell.frontmatter[change['owner'].description]=change['new']
        if auto:
            update_html()
    for k, v in cell.frontmatter.items():
        cell.widgets[k]=ipywidgets.interaction._widget_from_abbrev(v)
        cell.widgets[k].description=k
        cell.widgets[k].observe(names='value', handler=update_frontmatter)        
    trigger = [] if auto else [cell.widgets['trigger']]
    return ipywidgets.Box(children=[*[v for k,v in cell.widgets.items() if k in cell.frontmatter],*trigger,cell.widgets['html']])

@IPython.core.magic.magics_class
class Literate(IPython.core.magic.Magics):
    def __init__(self, namespace='library', **kwargs):
        self.env, self.cells = [LiterateEnvironment(**kwargs), {}]
        self.env.ip.user_ns[namespace] = self
        super().__init__()
        self.env.ip.register_magics(self)
    @IPython.core.magic.cell_magic
    @IPython.core.magic_arguments.magic_arguments()
    @IPython.core.magic_arguments.argument( "name", default=None, nargs="?", help="""Name of local variable to set to parsed value""")
    @IPython.core.magic_arguments.argument("-n", "--nodisplay", default=False, action="store_true", help="""Show the output""")
    @IPython.core.magic_arguments.argument("-i", "--interact", default=False, action="store_true", help="""Show the output""")
    @IPython.core.magic_arguments.argument("-a", "--auto", default=False, action="store_true", help="""Show the output""")
    def literate(self, line, cell):
        line = line.strip()
        args = IPython.core.magic_arguments.parse_argstring(self.literate, line)
        cell = StaticCell( cell, args.name, self.env )
        if args.name:
            self.env.ip.user_ns[args.name] = cell
        if not args.nodisplay:
            if args.interact:
                return widgetize(cell,auto=args.auto)
            return cell
