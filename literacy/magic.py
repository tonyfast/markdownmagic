"""
# About `magic.py`

Initialize `%%literate` magic.

## Syntax

### Basic

    from literate import Literacy
    Literacy()

## Examples


## Input Arguments

- `macros` -
- `templates` -

## See Also
"""
from .blocks import (
    ParentCell,
)
from .environment import (
    LiterateEnvironment,
)
from IPython.core import magic_arguments
from IPython.core.magic import (
    Magics,
    magics_class,
    cell_magic,
)
from traitlets import (
    Dict,
)
@magics_class
class Literate(Magics):
    files=Dict()
    languages=Dict()  #List of lanuages
    def __init__(self,
        namespace= 'library',
        macros={},
        templates={},
        filters = {},
        render_templates = True,
        *args,
        **kwargs
    ):
        """Created and name a templating environment.  Initialize the magic."""
        super(Literate,self).__init__(*args, **kwargs)
        self.env=LiterateEnvironment(**kwargs)
        self.env.macros.update(macros)
        self.env.loader.mapping['custom'].mapping.update(templates)
        self.env.filters.update(filters)
        self.namespace=namespace
        self.env.globals['render_templates'] = render_templates
        self._register_magic()

    def _register_magic(self):
        ip=self.env.ip
        ip.register_magics(self)

    def macro(self, name, aliases=[], template_name='macro/default.html', **kwargs):
        return self.env.macros.macro( name, aliases=[], template_name='macro/default.html', **kwargs)

    def template(self, name, template_string):
        self.env.loader.mapping['custom'].mapping[name] = template_string
        return 'custom/{}'.format(name)

    def filter(self, name, callback):
        self.env.filters[name] = callback
        return self.env.filters[name]

    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument( "name", default=None, nargs="?", help="""Name of local variable to set to parsed value""")
    @magic_arguments.argument("-f", "--filename", default="", help="""File name for the cell.""")
    @magic_arguments.argument("-n", "--nodisplay", default=False, action="store_true", help="""Show the tangled code.""")
    @magic_arguments.argument("-c", "--classes", default='', help="""Template for the tangled cell.""")
    def literate(self, line, cell):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.literate, line)
        literate_cell = ParentCell(self.env, cell)
        if literate_cell.filename:
            self.cells[literate_cell.filename]=literate_cell
        if args.name:
            self.env.ip.user_ns[args.name] = literate_cell
        if not args.nodisplay:
            return literate_cell

    @property
    def this(self):
        return self.env.globals['this']
