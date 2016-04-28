class CodeBlock(object):
    def __init__(self):
        """If the element starts with <pre><code> then it is code block.
        Block is updated with language, callbacks, and indents.
        In the future I hope to split make cells with the correct indent pattern
        """
        if self.is_code:
            lines=self.code.split('\n')
            self.offset = [len(line) - len(line.lstrip()) for line in lines]
    @property
    def callback(self):
        """The callback for the language if it exists"""
        callbacks=self.env.globals['callback']
        if self.language in callbacks:
            return callbacks[self.language]
        return None
    @property
    def language(self):
        """Get language of the current code block"""
        lang = self.env.globals['default_lang']
        if self.query('code').attr('class'):
            lang = [c.lstrip(self.env.globals['lang_prefix']) for c in self.query('code').attr('class').split() if c.startswith(self.env.globals['lang_prefix'])][0]
        return lang

class Block(CodeBlock):
    """
    A stream of non-code elements or a code element.
    """
    def __init__(self, query,env):
        self.env,self.query=[env,query]
    @property
    def code(self):
        if self.is_code:
            return self.query('code').html()
        return self.query.outerHtml()
    @property
    def tag(self):
        return self.query[0].tag
    @property
    def is_code(self):
        return self.tag in ['pre']
