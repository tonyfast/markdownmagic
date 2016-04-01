
# markdownmagic
> an [IPython](http://ipython.org/) [magic](https://ipython.org/ipython-doc/dev/interactive/tutorial.html) for authoring Interactive Data-Driven notebooks with basic [Markdown]().

## Install
From the command line (or with `!` in a notebook cell):
```bash
pip install markdownmagic
```

## Enable
### Ad-hoc
In the notebook, you can use the `%load_ext` or `%reload_ext` line magic.


```python
%reload_ext autoreload
%autoreload 2
```


```python
from markdownmagic import  environment
mdmagic = environment()
```

### Configuration
In your profile's `ipython_kernel_config.py`, you can add the following line to automatically load `markdownmagic` into all your running kernels:

```python
c.InteractiveShellApp.extensions = ['markdownmagic']
```

## Use
The `%%jade` cell magic will either act as simple parser:


```python
%%markdown
# This is markdown

Magic options for markdown:
    
# How is this different
```




# This is markdown

Magic options for markdown:
    
# How is this different



which can be accessed by the special last result variable `_`:


```python
_
```




# This is markdown



Or will update a named variable with the parsed document:

## Contribute
[Issues](https://github.com/tonyfast/markdownmagic/issues) and [pull requests](https://github.com/tonyfast/markdownmagic/pulls) welcome!

## License

`markdownmagic` is released as free software under the [BSD 3-Clause license](./LICENSE).

## Thank



```python

```
