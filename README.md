
<h1><code>Literacy</code></h1><p><code>Literacy</code> assists in creating static and interactive data-driven documents with Jupyter notebooks.</p>
<hr><pre><code class="lang-%%bash">pip install git+https://github.com/tonyfast/literacy --upgrade
</code></pre><hr><h2>Initialize <code>literate</code> magic</h2><p>Initialize the <code>literate</code> magic in a code cell in the Jupyter notebook.</p>
<hr><pre><code class="lang-python">library = Literate()
</code></pre><hr><p>The Literate <code>library</code> contains a <a href=""><code>jinja2</code></a> templating environment
that is used for all of the <code>%%literate</code> cells.  The templating environment allows <code>jinja2</code>
to access variables in your current notebook.</p>

<h1>Using <code>literate</code> magic</h1><p>Literate magics start with <code>%%literate</code>.  The body of the cell is markdown.  Markdown code fences 
are executed as code if the <code>library</code> corresponding to the language.</p>
<hr><pre><code class="lang-python">default_filters = [k.lstrip('execute_') for k in library.env.filters.keys() if k.startswith('execute_')]
num_filters = len(default_filters)
</code></pre><hr><h3>Default filters</h3><p>The 2 default filters are:</p><ul>

<li>javascript</li>

<li>python</li>

</ul>