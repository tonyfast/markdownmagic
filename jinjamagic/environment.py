from .blocks import (
    NormalBlock,
    FenceBlock,
    IndentBlock,
    CellBlock,
)
from jinja2 import (
    FileSystemLoader,
    PackageLoader,
    DictLoader,
    ChoiceLoader,
)
from jinja2 import (
    Environment,
    Template,
    TemplateNotFound,
)
from mistune import (
    Markdown,
    Renderer,
)
from IPython import (
    get_ipython,
)
from IPython.display import (
    HTML,
)


class GlobalsTemplate(Template):
    def render(self, **data):
        """Attach globally variables to the render function.
        """
        env = self.environment
        data.update(env.globals)
        data.update(env.ip.user_ns)
        return super(GlobalsTemplate, self).render(**data)


class Env(Environment):
    preprocessor = Markdown(renderer=Renderer(escape=False))
    loaders = {
            'custom': DictLoader({}),
            'local': FileSystemLoader('tmpl'),
            'builtin': PackageLoader('jinjamagic', 'tmpl'),
        }

    def __init__(self, templates={}, filters={}):
        super(Env, self).__init__(
            loader=ChoiceLoader(list(self.loaders.values()))
        )
        self.template_class = GlobalsTemplate
        self.filters.update({
                'default': lambda code: {
                    'html': code,
                },
                'javascript': lambda code: {
                    'script': code,
                },
                'css': lambda code: {
                    'style': code,
                },
            })
        self.filters.update(filters)
        self.loaders['custom'].mapping.update(templates)
        self.ip = get_ipython()

    def init(self, template_name='init'):
        has_template = True
        try:
            template = self.get_template(template_name)
        except TemplateNotFound:
            has_template = False
        if has_template:
            return HTML(template.render())

    @property
    def kernel(self):
        return self.ip.run_cell

    @property
    def this(self):
        return self.env.globals['this']

    def add_template(self, template_name, template):
        self.env.loaders['custom'].mapping[template_name] = template
        return self.env.get_template(template_name)

    def render_literate(self, code):
        cell = CellBlock(self, code)
        for ct, fence in enumerate(code.split('\n```')):
            if (ct % 2) == 1:
                """ct=0 is false"""
                cell.blocks.append(FenceBlock(cell, "```{}```".format(fence)))
            else:
                rendered_markdown = self.preprocessor(fence)
                """Discover basic idented code blocks"""
                indent_blocks = rendered_markdown.replace(
                    '</code></pre>', '<pre><code>'
                ).split('<pre><code>')
                for ct_md, block in enumerate(indent_blocks):
                    cell.blocks.append(
                        IndentBlock(cell, block)
                        if (ct_md % 2) == 1
                        else NormalBlock(cell, block)
                    )
        cell.data = self.get_template('cell.html').render(cell=cell)
        return cell
