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
from traitlets import (
    Dict,
    import_item,
)
@magics_class
class Literate(Magics):
    files=Dict()
    languages=Dict()
    def __init__(self, namespace='library', languages={}, templates={}, *args, **kwargs):
        """Created and name a templating environment.  Initialize the magic."""
        super(Literate,self).__init__(*args, **kwargs)
        self.env=LiterateEnvironment()
        self.languages.update(languages)
        self.templates.update(templates)
        self.namespace=namespace
        self._register_magic()

    def _register_magic(self):
        ip=self.env.ip
        ip.user_ns[self.namespace] = self
        ip.register_magics(self)

    def template(self,template_name, template_string):
        self.templates[template_name] = template_string

    def language(self, names, **languages):
        """Register a GFM-style language to be executed when rendering.

        Provide keyword arguments for `languages` as:

            <web-renderable format>: callback(code)

        example:

            whitespace = Literate()

            whitespace.language("coffee", js=coffeetools.coffee.compile)

            whitespace.language("jade", html=pyjade.process)

            def stylus(code):
                return check_output(["stylus"], stdin=PIPE)
            whitespace.language("stylus", css=stylus)

            whitespace.language("yaml", json=yaml.safe_load)
        """
        if isinstance(names, str):
            names=[names]
        for name in names:
            self.languages[name] = languages

    @property
    def templates(self):
        return self.env.loader.mapping
    @property
    def languages(self):
        return self.env.languages

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
        literate_cell=cell_type(cell, args=args, env=self.env)
        if literate_cell.filename:
            self.cells[literate_cell.filename]=literate_cell
        if not args.nodisplay:
            if args.interact and not args.static:
                return literate_cell.display()
            return literate_cell

    @property
    def this(self):
        return self.env.globals['this']
