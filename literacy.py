from .cell import (
    InteractiveCell,
    StaticCell,
)
from .env import (
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
    def __init__(self, namespace='library', **kwargs):
        self.env, self.cells = [LiterateEnvironment(**kwargs), {}]
        self.env.ip.user_ns[namespace] = self
        super().__init__()
        self.env.ip.register_magics(self)
    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument( "name", default=None, nargs="?", help="""Name of local variable to set to parsed value""")
    @magic_arguments.argument("-n", "--nodisplay", default=False, action="store_true", help="""Show the tangled code.""")
    @magic_arguments.argument("-i", "--interact", default=False, action="store_true", help="""Interactive widgets for the cell.""")
    @magic_arguments.argument("-s", "--static", default=False, action="store_true", help="""Display interactive widget as static display""")
    @magic_arguments.argument("-a", "--auto", default=False, action="store_true", help="""Automatically update widgets.""")
    def literate(self, line, cell):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.literate, line)
        if args.interact:
            cell = InteractiveCell( cell, args.name, self.env, auto=args.auto )
        else:
            cell = StaticCell(cell, args.name, self.env)
        if args.name:
            self.env.ip.user_ns[args.name] = cell
        if not args.nodisplay:
            if args.interact:
                if args.static:
                    pass
                else:
                    return cell.display
            return cell

if __name__ == '__main__':
    Literate()
