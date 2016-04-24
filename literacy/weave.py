class Weave(object):
    def weave(self,**kwargs):
        tokens={
            'html':'',
            'js':'',
            'css':''
        }
        tokens.update(kwargs)
        return self.env.get_template('weave_template').render(tokens)

def __init__():
    pass
