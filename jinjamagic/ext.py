from jinja2 import (
    Template,
)
from jinja2.ext import(
    Extension,
)
from IPython import (
    get_ipython,
)


class IPythonNS(Template):
    """Return templates as IPython display objects that use the current IPython
    namespace.
    """
    def render(self, apply_globals=True, **kwargs):
        if apply_globals:
            builtin = self.environment.ip.user_ns['__builtin__']

            kwargs = {
                **self.environment.ip.user_ns,
                **{
                    name: getattr(builtin, name)
                    for name in dir(builtin) if not name.startswith('_')
                },
                **kwargs,
            }
        return super(IPythonNS, self).render(**kwargs)


class IPythonKernel(Extension):
    """Attach the IPython context to the environment then
    """
    def __init__(self, environment):
        environment.ip = get_ipython()
        environment.template_class = IPythonNS
        self.environment = environment


class LiterateExtension(IPythonKernel):
    """Replace code fences with filter jinja filters tags before processing.
    """
    def preprocess(self, source, *args, **kwargs):
        if '\n```' in source:
            parsed = """"""
            for count, block in enumerate(source.split('\n```')):
                if (count % 2) == 0:
                    language = 'markdown'
                else:
                    if block:
                        language, block = block.split('\n', 1)
                        language = language.strip()
                    else:
                        language = ''
                    if language not in self.environment.filters:
                        language = 'source'
                if block:
                    parsed += "{% filter "+language+" %}" + \
                        block + "{% endfilter %}"
        else:
            parsed = source
        return parsed
