from .tangle import (
    Tangle,
)
from .env import (
    LiterateEnvironment,
)
import IPython, ipywidgets

class Cell(Tangle):
    def __init__(self, raw, name="""_current_cell""", env=LiterateEnvironment()):
        self.env, self.name = [env, name]
        self.env.globals[self.name] = self
        super().__init__(raw)

class StaticCell(Cell, IPython.display.HTML):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.tangle()

class InteractiveCell(StaticCell):
    def __init__(self, *args, auto=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto=auto
        if not hasattr(self,'widgets'):
            self.widgets={}
        if not 'html' in self.widgets:
            self.widgets['html']=ipywidgets.HTML(self.data)
        if not 'trigger' in self.widgets:
            self.widgets['trigger']=ipywidgets.Button(description="""Update cell""")
            self.widgets['trigger'].on_click(callback=self.update_html)
        self.widgetize()
        self.update_html()

    def update_html(self,*args,**kwargs):
        self.widgets['html'].value = self.tangle()
    def update_frontmatter(self,change,*args,**kwargs):
        self.frontmatter[change['owner'].description]=change['new']
        if self.auto:
            self.update_html()
    def widgetize(self):
        for k, v in self.frontmatter.items():
            if isinstance( v,(str,list,dict,int,float)):
                self.widgets[k]=ipywidgets.interaction._widget_from_abbrev(v)
                self.frontmatter[k]=self.widgets[k].value
                self.widgets[k].description=k
                self.widgets[k].observe(names='value', handler=self.update_frontmatter)
    @property
    def display(self):
        trigger = [] if self.auto else [self.widgets['trigger']]
        return ipywidgets.Box(
            children=[
                self.widgets['html'],
                *[v for k,v in self.widgets.items() if k in self.frontmatter],
                *trigger
            ])
