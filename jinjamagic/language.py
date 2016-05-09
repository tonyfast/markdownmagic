class Language():
    def __init__(
        self, environment, name, handler=lambda s: {},
        transpile=True, show_source=True, template_name='block.html', **tokens
    ):
        self.environment = environment
        self.template = self.environment.get_template(template_name)
        self.name = name
        self.handler = handler
        self.tokens = tokens
        self.show_source = show_source

    def __call__(self, source, show_source=None):
        """"""
        tokens = {}
        source = self.environment.from_string(
            source
        ).render(
            apply_globals=False
        )
        tokens.update({'source': source})
        tokens.update(
            {
                key: _handler(source)
                for key, _handler in self.tokens.items()
            }
        )
        tokens.update(self.handler(source))
        if isinstance(show_source, type(None)):
            show_source = self.show_source
        return self.template.render(show_source=show_source, **tokens)
