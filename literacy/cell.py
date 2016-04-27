from .preprocessor import (
    PreProcessor,
)
from .environment import (
    LiterateEnvironment,
)
from IPython.display import (
    HTML,
)
from pyquery import (
    PyQuery,
)
class Cell(PreProcessor, HTML):
    def __init__(self, raw, filename=None, name="""_current_cell""", env=LiterateEnvironment()):
        self.tangled= PyQuery("""<div></div>""").addClass('literate')
        self.env, self.name = [env, name]
        self.env.globals['this'] = self
        if name:
            self.tangled.attr('id', name)
            self.env.globals[name] = self
            self.env.ip.user_ns[name] = self
        super(Cell,self).__init__(raw)
        if filename:
            self.filename=filename

    def save(self,template=None):
        with open(self.filename,'w') as f:
            f.write(self.data)

class StaticCell(Cell):
    def __init__(self,*args,**kwargs):
        super(StaticCell,self).__init__(*args,**kwargs)
        self.tangle()
