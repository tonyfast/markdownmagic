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
        self.env=LiterateEnvironment(**kwargs)
        self.env.ip.user_ns[namespace] = self
        super(Literate,self).__init__(*args, **kwargs)
        self.env.ip.register_magics(self)
    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument( "name", default=None, nargs="?", help="""Name of local variable to set to parsed value""")
    @magic_arguments.argument("-f", "--filename", default=None, help="""File name for the cell.""")
    @magic_arguments.argument("-n", "--nodisplay", default=False, action="store_true", help="""Show the tangled code.""")
    @magic_arguments.argument("-i", "--interact", default=False, action="store_true", help="""Interactive widgets for the cell.""")
    @magic_arguments.argument("-s", "--static", default=False, action="store_true", help="""Display interactive widget as static display""")
    @magic_arguments.argument("-a", "--auto", default=False, action="store_true", help="""Automatically update widgets.""")
    def literate(self, line, cell):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.literate, line)
        if args.interact:
            cell = InteractiveCell( cell, name=args.name, filename=args.filename, env=self.env, auto=args.auto )
        else:
            cell = StaticCell(cell, name=args.name, filename=args.filename, env=self.env)
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
