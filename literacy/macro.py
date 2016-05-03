class Macro():
    def __init__(self, env, template_name = 'macro/default.html', **kwargs):
        self.methods = {
            'source': lambda s: s,
        }
        self.env = env
        self.methods.update(kwargs)
        self.template_name = template_name

    def render(self, block, **data):
        payload = {}
        for key, macro_function in self.methods.items():
            if not key in [self.env.kernel]:
                payload[key] = macro_function(block.source) if macro_function else ""
        payload.update(data)
        return self.template.render(block=block, **payload)


    @property
    def template(self):
        return self.env.get_template(self.template_name)

class Macros(dict):
    def __init__(self, env):
        self.env = env
        self.macro('javascript',aliases=['js'], script=lambda s: s)
        self.macro('css', style=lambda s: s)

    def macro(self, macro_name, aliases=[], *args, **kwargs):
        self[macro_name] = Macro(self.env, *args, **kwargs)
        self[macro_name].name = macro_name
        self[macro_name].aliases = aliases
        for alias in aliases:
            self[alias] = self[macro_name]
