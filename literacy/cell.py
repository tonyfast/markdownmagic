from .tangle import (
    Tangle,
)
from .environment import (
    LiterateEnvironment,
)
import IPython, ipywidgets

class Cell(Tangle, IPython.display.HTML):
    def __init__(self, raw, name="""_current_cell""", env=LiterateEnvironment()):
        self.env, self.name = [env, name]
        if name:
            self.env.ip.user_ns[name] = self
        super(Cell,self).__init__(raw)
        self.env.globals[self.name] = self

class StaticCell(Cell):
    def __init__(self,*args,**kwargs):
        super(StaticCell,self).__init__(*args,**kwargs)
        self.tangle()

class InteractiveCell(Cell):
    """A cell that can support interactive widgets"""
    auto=False
    def __init__(self, *args, **kwargs):
        self.widgets={}
        if 'auto' in kwargs:
            self.auto=kwargs['auto']
            del kwargs['auto']
        super(InteractiveCell,self).__init__(*args, **kwargs)
        if not 'html' in self.widgets:
            self.widgets['html']=ipywidgets.HTML(self.data)
        if not 'trigger' in self.widgets:
            self.widgets['trigger']=ipywidgets.Button(description="""Update cell""")
            self.widgets['trigger'].on_click(callback=self.update_html)
        self.widgetize()
        self.update_html()

    def update_html(self,*args,**kwargs):
        """tangle the code and up the html"""
        self.widgets['html'].value = self.tangle()
    def update_frontmatter(self,change,*args,**kwargs):
        """Update frontmatter when when the variable changes"""
        self.frontmatter[change['owner'].description]=change['new']
        if self.auto:
            self.update_html()
    def attach_widget( self, name, widget=None, abbrev=None, *args, **kwargs ):
        if not name in self.widgets:
            if abbrev:
                widget=ipywidgets.interaction._widget_from_abbrev(abbrev)
            else:
                widget=widget(*args,**kwargs)
            widget.description=name
            widget.observe(names='value', handler=self.update_frontmatter)
            self.widgets[name]=widget
    def widgetize(self):
        for k, v in self.frontmatter.items():
            if not k in self.widgets:
                self.attach_widget(k,abbrev=v)
        for k, v in self.widgets.items():
            if not k in ['html'] and hasattr( v, 'value'):
                self.frontmatter[k]=v.value
    @property
    def display(self):
        """Show the widgets"""
        widgets=[self.widgets['html']]
        widgets.extend([v for k,v in self.widgets.items() if k not in ['html','trigger']])
        if not self.auto:
            widgets.append(self.widgets['trigger'])
        return ipywidgets.Box(children=widgets)
