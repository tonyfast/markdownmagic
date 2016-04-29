class CodeBlock(object):
    def __init__(self):
        """If the element starts with <pre><code> then it is code block.
        Block is updated with language, callbacks, and indents.
        In the future I hope to split make cells with the correct indent pattern
        """
        if self.is_code:
            lines=self.content.split('\n')
            self.indent = [len(line) - len(line.lstrip()) for line in lines]
        self.language = self.env.default_language
        if self.query('code').attr('class'):
            self.language = [c.lstrip(self.env.language_prefix)
                for c in self.query('code').attr('class').split()
                if c.startswith(self.env.language_prefix)
            ][0]
        self.handler = self.env.languages[self.language] if self.language in self.env.languages else None

class Block(CodeBlock):
    """
    A stream of non-code elements or a code element.
    """
    def __init__(self, query,env):
        self.query, self.env = [query, env]
        if self.query[0].tag=='div' and not(self.query.attr('class') or self.query.attr('id')):
            """Pyquery wraps a weird div around the rendered text."""
            self.query=self.query('div')
        self.tag = self.query[0].tag
        self.is_code = self.tag in ['pre']
        self.content = self.query.outerHtml()
        super(Block, self).__init__()
