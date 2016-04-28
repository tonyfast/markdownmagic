from .processor import (
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
    def __init__(self, raw, filename=None, name="""_current_cell""", env=LiterateEnvironment()):
        self.blocks=[]
        self.tangled=PyQueryUTF("""<div></div>""")
        self.env, self.name, self.env.globals['this'] = [env, name, self]
        if name:
            self.tangled.attr('id', name)
            self.env.globals[name], self.env.ip.user_ns[name] = [self, self]
        if filename:
            self.filename=filename
        super(Cell,self).__init__(raw)
    def save(self,template=None):
        with open(self.filename,'w') as f:
            f.write(self.data)

class StaticCell(Cell):
    def __init__(self,*args,**kwargs):
        super(StaticCell,self).__init__(*args,**kwargs)
        self.data=self.tangle()
