from pyquery import (
    PyQuery,
)
from lxml import (
    etree,
)
class PyQueryUTF(PyQuery):
    """Patch output html to export a different encoding than pyquery."""
    def outer_html(self):
        if not self:
            return None
        e0 = self[0]
        if e0.tail:
            e0 = deepcopy(e0)
            e0.tail = ''
        return etree.tostring(e0, method='html', encoding='utf-8')
