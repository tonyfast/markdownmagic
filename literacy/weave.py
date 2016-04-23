class Weave():
    def weave(self,**kwargs):
        return self.env.get_template('weave_template').render(
            {**{
                'html':'',
                'js':'',
                'css':''
            },
            **kwargs
            }
        )
