"""
# About `magic.py`

Initialize `%%jinjamagic` magic.

## Syntax

### Basic

    from jinjamagic import jinjamagic
    jinjamagic()

## Examples

"""
from .blocks import (
    CellBlock,
)
from .environment import (
    Env,
)
from IPython.core import (
    magic_arguments,
)
from IPython.core.magic import (
    Magics,
    magics_class,
    cell_magic,
)


@magics_class
class jinjamagic(Magics):
    def __init__(
        self,
        namespace='default',
        templates={},
        filters={},
        render_templates=True,
        *args,
        **kwargs
    ):
        """Created and name a templating environment.  Initialize the magic."""
        super(jinjamagic, self).__init__(*args, **kwargs)
        self.env = Env(templates, filters)
        self.env.globals['render_templates'] = render_templates
        self.env.ip.register_magics(self)

    @property
    def render_templates(self):
        return self.env.globals['render_templates']

    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "var_name", default=None, nargs="?",
        help="""Name of local variable to set to parsed value""")
    @magic_arguments.argument(
        "-h", "--hide", default=False,
        action="store_true",
        help="""Don't display output.""")
    @magic_arguments.argument(
        "-c", "--classes", default='',
        help="""Template for the tangled cell.""")
    @magic_arguments.argument(
        "-n", "--namespace", default=None,
        help="""Template for the tangled cell.""")
    def jinja(self, line, cell):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.jinja, line)
        cell = CellBlock(self.env, cell, var_name=args.var_name)
        cell.render()
        if not args.hide:
            return cell

    @property
    def this(self):
        return self.env.globals['this']
