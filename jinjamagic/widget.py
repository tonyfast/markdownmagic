from ipywidgets import (
    HTML,
)


class JinjaWidget(HTML):
    def __init__(self, cell):
        self.template = cell.template
        super(JinjaWidget, self).__init__(cell.data)

    def attach(self, widget, attr='value'):
        widget.observe(names=attr, handler=self._update_state)
        return self

    def _on_change_value(self, change):
        self.value = self.template.render().data
