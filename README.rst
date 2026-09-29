ASCII Trees
===========

[![Run on Repl.it](https://repl.it/badge/github/mbr/asciitree)](https://repl.it/github/mbr/asciitree)

.. code:: console

  asciitree
   +-- sometimes
   |   +-- you
   +-- just
   |   +-- want
   |       +-- to
   |       +-- draw
   +-- trees
   +-- in
       +-- your
           +-- terminal


.. code:: python

  from asciitree import LeftAligned
  from collections import OrderedDict as OD

  tree = {
      'asciitree': OD([
          ('sometimes',
              {'you': {}}),
          ('just',
              {'want': OD([
                  ('to', {}),
                  ('draw', {}),
              ])}),
          ('trees', {}),
          ('in', {
              'your': {
                  'terminal': {}
              }
          })
      ])
  }

  tr = LeftAligned()
  print(tr(tree))


Custom layout spaces
--------------------

``BoxStyle.space`` controls the character used for indentation and padding.
It defaults to an ordinary space. For example, use a non-breaking space when
embedding a tree in text that may wrap:

.. code:: python

  from asciitree import LeftAligned
  from asciitree.drawing import BoxStyle

  tree = {'root': {'child': {}}}
  tr = LeftAligned(draw=BoxStyle(space=u'\u00a0'))
  print(tr(tree))

Label text and the characters in ``BoxStyle.gfx`` are left unchanged.
On Python 2, use Unicode labels when selecting Unicode layout characters;
encoded byte labels are not automatically decoded.

Read the documentation at http://pythonhosted.org/asciitree
