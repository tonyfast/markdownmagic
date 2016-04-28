from .tangle import (
    Processor,
)
from .environment import (
    LiterateEnvironment,
)
from IPython.display import (
    HTML,
)
from .query import (
    PyQueryUTF,
)
class Cell(Processor, HTML):
    """
    Process the body of cell:
    Tangle the code into html and code blocks.
    Weave the code in either static or interactive mode.
    """
    def __init__(self, raw, cell_args, env=LiterateEnvironment(), *args, **kwargs):
        self.blocks=[]
        self.env, self.name, self.env.globals['this'] = [env, cell_args.name, self]
        self.classes=cell_args.classes
        if cell_args.template in ['default'] and (cell_args.classes or self.name):
            cell_args.template='default_div'
        self._template=self.env.get_template(cell_args.template)
        self.filename=cell_args.filename
        if cell_args.name:
            self.env.globals[cell_args.name]=self.env.ip.user_ns[cell_args.name]=self
        super(Cell,self).__init__(raw)

    def save(self,template=None):
        with open(self.filename,'w') as f:
            f.write(self.data)

    def render(self,txt,render_template=False):
        if self.env.globals['render_template'] or render_template:
            template=self.env.from_string(txt)
            data={k:getattr(self.env.ip.user_ns['__builtin__'],k) for k in dir(self.env.ip.user_ns['__builtin__']) if not k.startswith('_')}
            data.update(self.env.ip.user_ns)
            data.update(self.frontmatter)
            return template.render(**data)
        return txt

    @property
    def query(self):
        """"""
        return PyQueryUTF(self.env.renderer(self.raw))

class StaticCell(Cell):
    def __init__(self,*args,**kwargs):
        super(StaticCell,self).__init__(*args,**kwargs)
        self.data=self.tangle()
        self.data=self._template.render(cell=self)
