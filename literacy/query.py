from pyquery import (
    PyQuery, pyquery
)
from lxml import (
    etree,
)
from copy import (
    deepcopy,
)

class PyQueryUTF(PyQuery):
    """Patch output html to export a different encoding than pyquery."""
    @pyquery.with_camel_case_alias
    def outer_html(self):
        if not self:
            return None
        e0 = self[0]
        if e0.tail:
            e0 = deepcopy(e0)
            e0.tail = ''
        return etree.tostring(e0, method='html', encoding='utf-8').decode('utf-8')

    @pyquery.with_camel_case_alias
    def inner_html(self):
        if not self:
            return None
        tag = self[0]
        children = tag.getchildren()
        if not children:
            return tag.text
        html = tag.text or ''
        return html + "\n".join([etree.tostring(e, method='html', encoding='utf-8').decode('utf-8') for e in children])
