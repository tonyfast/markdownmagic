from __future__ import print_function

from IPython import get_ipython

import IPython

from IPython.core import magic_arguments

from IPython.core.magic import (
    Magics,
    magics_class,
    cell_magic,
)

from jinja2 import (
    Environment,
    DictLoader,
)

import mistune
from mistune import (
    Renderer,
)

import yaml

__version_info__ = (0, 1, 0)
__version__ = '.'.join(map(str, __version_info__))


class LiterateRenderer(Renderer):
    """Executes code for on Markdown code fences for the language ``python``"""
    def __init__(self, ip, *args, **kwargs):
        self.ip = ip
        super().__init__(*args, **kwargs)

    def block_code(self, text, lang):
        if lang in ['python']:
            self.ip.run_code(text)
        return super().block_code(text, lang)


class MarkdownerTemplate(IPython.core.display.Markdown):
    def __init__(
        self,
        env=Environment(),
        ip=get_ipython(),
        frontmatter="""""",
        *args,
        **kwargs
    ):
        self.env = env
        self.ip = ip
        self.frontmatter = frontmatter
        super().__init__(*args, **kwargs)
        if self.frontmatter:
            self.frontmatter = yaml.load(
                self.env.from_string(
                    self.frontmatter
                ).render(self.ip.user_ns)
            )
        else:
            self.frontmatter = {}
        self.template = self.env.from_string(self.data)

    def __add__(self, payload):
        if payload in ['*']:
            payload = self.ip.user_ns
        return self.template.render(**payload)

    def __mul__(self, payload):
        return '\n'.join([self.template.render(**load) for load in payload])

    def _repr_markdown_(self):
        self.env.filters['mistune_renderer'](self.data)
        return self + {**self.frontmatter, **self.ip.user_ns}


@magics_class
class environment(Magics):
    """
    Literate Python in using Markdown.

    Example:

        %%markdown
        # This is a title with {{data}}
    """
    ip = get_ipython()

    def __init__(self, env=Environment(loader=DictLoader({}))):
        self.env = env
        self.env.filters['mistune_renderer'] = mistune.Markdown(
            renderer=LiterateRenderer(ip=self.ip, escape=False)
        )
        super().__init__()
        self.ip.register_magics(self)

    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "name",
        default=None,
        nargs="?",
        help="""Name of local variable to set to parsed value"""
    )
    def markdown(self, line, cell):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.markdown, line)
        if cell.startswith('---'):
            frontmatter, cell = cell.lstrip('---').split('---', 1)
        else:
            frontmatter = {}
        try:
            # Literate python execution
            display = MarkdownerTemplate(
                self.env,
                self.ip,
                frontmatter,
                data=cell
            )
        except Exception as err:
            print(err)
            return

        if args.name:
            self.ip.user_ns[args.name] = display
        return display
