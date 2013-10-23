# galene

**γαλήνη (galene)** is a very simple text editor for Linux and GTK. It clears away all distractions and makes you focus on the writing itself. It can have only one file open and displays it full screen. There are no buttons or user interface. Just you and your text.

<a href="https://raw.github.com/ze-phyr-us/galene/master/screenshot.png">
	<img alt="Screenshot of γαλήνη." width="500"
	src="https://raw.github.com/ze-phyr-us/galene/master/screenshot.png" />
</a>

Γαλήνη, or Galene, was a personification of calm sea in the ancient Greek mythology. That's how I like the blank sheet before me: calm, empty, waiting for words that will give it meaning.

Syntax highlighting is supported as well as a few keyboard shortcuts. There is a very limited configuration available at the top of `galene.py`. You may want to change your font there (a beautiful LaTeX serif is set by default).


## Keyboard Shortcuts

**Ctrl+O**: open a file; **Ctrl+S**: save the current file; **Shift+Ctrl+S**: save as...

I use the editor primarily for HTML, which is why it supports the following shortcuts:
**Ctrl+Alt+e**: wrap the current selection by the `<em>` tag; *Ctrl+Alt+g*: wrap the current selection by the `<strong>` tag; **Ctrl+Alt+p**: wrap the current selection by the `<p>` tag; **Ctrl+Alt+c**: comment out the current selection; **Ctrl+space**: insert a non-breakable space (`&nbsp;`).


## Requirements

* 2.5 &le; Python &lt; 3.0
* 2.10 &le; PyGTK
* pygtksourceview

Read more about γαλήνη at [ze.phyr.us/focus-on-writing](http://ze.phyr.us/focus-on-writing).
