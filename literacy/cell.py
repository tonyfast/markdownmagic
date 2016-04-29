from IPython.display import (
    HTML,
)
from .tangle import (
    Processor,
)
from .environment import (
    LiterateEnvironment,
)
class Cell(Processor, HTML):
    """
    This class should not instantiated itself use staticCell or interactivecell
    Process the body of cell:
    Tangle the code into html and code blocks.
    Weave the code in either static or interactive mode.
    """
    def __init__(self, raw, args, env=LiterateEnvironment()):
        self.blocks = []
        self.env, self.name, self.filename, self.env.globals['this'] = [env, args.name, args.filename, self]
        # Assign cell args
        self.classes = args.classes
        # Define template for the cell
        if args.template in ['default'] and (args.classes or self.name):
            args.template = 'default_div'
        self._template = self.env.get_template(args.template)

        if args.name:
            self.env.globals[args.name]=self.env.ip.user_ns[args.name]=self
        super(Cell,self).__init__(raw)

    def save(self):
        if self.filename:
            with open(self.filename,'w') as f:
                f.write(self.data)

    def render(self,txt,render_template=False):
        if self.env.render_template or render_template:
            template = self.env.from_string(txt)
            context = {
                k:getattr(self.env.ip.user_ns['__builtin__'],k)
                for k in dir(self.env.ip.user_ns['__builtin__'])
                if not k.startswith('_')
            }
            context.update(self.env.ip.user_ns)
            context.update(self.frontmatter)
            return template.render(**context)
        return txt

class StaticCell(Cell):
    def __init__(self, *args, **kwargs):
        super(StaticCell,self).__init__(*args,**kwargs)
        self.tangle()
        self.data =self._template.render(cell=self).strip()
