from .ext import (
    LiterateExtension,
)
from .language import (
    Language,
)
# from .widget import (
#     JinjaWidget,
# )
from jinja2 import (
    Environment,
    ChoiceLoader,
    PackageLoader,
)
from IPython.display import (
    HTML,
)
from IPython.core import (
    magic_arguments,
)
from IPython.core.magic import (
    Magics,
    magics_class,
    cell_magic,
)
from mistune import (
    Markdown,
    Renderer,
)


@magics_class
class jinjamagic(Magics):
    def __init__(
        self,
        loaders=[],
        *args,
        **kwargs
    ):
        """Created and name a templating environment.  Initialize the magic."""
        super(jinjamagic, self).__init__(*args, **kwargs)
        self.environment = Environment(
            loader=ChoiceLoader([
                *loaders,
                PackageLoader('jinjamagic', 'tmpl'),
            ]))
        self.environment.default_language = 'markdown'
        # self.environment.add_extension('pyjade.ext.jinja.PyJadeExtension')
        self.environment.add_extension(LiterateExtension)
        self.add_language('source')
        self.add_language(
            'markdown',
            html=Markdown(renderer=Renderer(escape=False)),
            show_source=False
        )
        self.add_language(
            'html',
            html=lambda source: source,
        )
        self.add_language(
            'javascript',
            script=lambda source: source,
        )
        self.add_language(
            'css',
            style=lambda source: source,
        )
        self.environment.ip.register_magics(self)

    def add_language(
        self, language, show_source=True,
        handler=lambda source: {},
        **tokens
    ):
        self.environment.filters[language] = Language(
            self.environment, language,
            show_source=show_source, handler=handler, **tokens
        )

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
        "-i", "--interact", default=False,
        action="store_true",
        help="""Interactive widget view.""")
    def jinja(self, line, raw):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.jinja, line)
        if '```' not in raw:
            raw += '\n```\n```'
        template = self.environment.from_string(raw)
        cell = HTML(template.render())
        cell.template = template
        cell.raw = raw
        # if args.interact:
        #     cell = JinjaWidget(cell)
        if args.var_name:
            self.environment.ip.user_ns[args.var_name] = cell
            self.environment.ip.user_ns[args.var_name] = cell
        if not args.hide:
            return cell
