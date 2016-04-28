from .cell import (
    StaticCell,
)
from .interactive import (
    InteractiveCell,
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

@magics_class
class Literate(Magics):
    def __init__(self, namespace='library', *args, **kwargs):
        """Created and name a templating environment.  Initialize the magic."""
        self.files={}
        self.env=LiterateEnvironment(**kwargs)
        self.env.ip.user_ns[namespace] = self
        super(Literate,self).__init__(*args, **kwargs)
        self.env.ip.register_magics(self)
    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument( "name", default=None, nargs="?", help="""Name of local variable to set to parsed value""")
    @magic_arguments.argument("-f", "--filename", default="", help="""File name for the cell.""")
    @magic_arguments.argument("-n", "--nodisplay", default=False, action="store_true", help="""Show the tangled code.""")
    @magic_arguments.argument("-i", "--interact", default=False, action="store_true", help="""Interactive widgets for the cell.""")
    @magic_arguments.argument("-s", "--static", default=False, action="store_true", help="""Display interactive widget as static display""")
    @magic_arguments.argument("-a", "--auto", default=False, action="store_true", help="""Automatically update widgets.""")
    @magic_arguments.argument("-t", "--template", default='default', help="""Template for the tangled cell.""")
    @magic_arguments.argument("-c", "--classes", default='', help="""Template for the tangled cell.""")
    def literate(self, line, cell):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.literate, line)
        cell_type = InteractiveCell if args.interact else StaticCell
        cell=cell_type(cell, cell_args=args, env=self.env)
        if cell.filename:
            self.files[cell.filename]=cell
        if not args.nodisplay:
            if args.interact:
                if args.static:
                    pass
                else:
                    return cell.display
            return cell

    @property
    def this(self):
        return self.env.globals['this']
