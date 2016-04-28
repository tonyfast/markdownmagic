from .cell import (
    Cell,
)
from ipywidgets import (
    interaction,
    Button,
    HTML,
    Box,
)
class InteractiveCell(Cell):
    """A cell that can support interactive widgets"""
    auto=False
    def __init__(self, *args, **kwargs):
        self.widgets={}
        self.auto=kwargs['args'].auto
        super(InteractiveCell,self).__init__(*args, **kwargs)
        self.data=""""""
        if not 'html' in self.widgets:
            self.widgets['html']=HTML(self.data)
        if not 'trigger' in self.widgets:
            self.widgets['trigger']=Button(description="""Update cell""")
            self.widgets['trigger'].on_click(callback=self.update_html)
        self.widgetize()
        self.update_html()

    def update_html(self,*args,**kwargs):
        """tangle the code and update static and dynamic html widget"""
        self.tangle()
        self.widgets['html'].value = self._template.render(cell=self)

    def update_frontmatter(self,change,*args,**kwargs):
        """Update frontmatter when when the variable changes"""
        self.frontmatter[change['owner'].description]=change['new']
        if self.auto:
            self.update_html()

    def attach_widget( self, name, widget=None, abbrev=None, *args, **kwargs ):
        """Utitily function to attach any widget to a cell."""
        if not name in self.widgets:
            try:
                if abbrev:
                    widget=interaction._widget_from_abbrev(abbrev)
                else:
                    widget=widget(*args,**kwargs)
                widget.description=name
                widget.observe(names='value', handler=self.update_frontmatter)
                self.widgets[name]=widget
            except:
                self.widgets[name]=None

    def widgetize(self):
        """Create widgets from shorthand and update the front matter"""
        for k, v in self.frontmatter.items():
            if not k in self.widgets:
                self.attach_widget(k,abbrev=v)
        for k, v in self.widgets.items():
            if not k in ['html'] and hasattr( v, 'value'):
                self.frontmatter[k]=v.value

    def display(self):
        """Show the widgets"""
        widgets=[self.widgets['html']]
        widgets.extend([v for k,v in self.widgets.items() if k not in ['html','trigger']])
        if not self.auto:
            widgets.append(self.widgets['trigger'])
        return Box(children=widgets)
