"""news-image-20261125 entry program (Python 3.13, standard library only).

The entry's image is the entry.png beside this file; the program copies it
to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png outside the grader).
The image is the front page for Wednesday 25 November 2026, drawn by
render.py (also in this repository) from news researched that day: 47
stories, 3 hero cards, a stat strip, a stylised world map and a DATE CHECK
box naming the stories deliberately left out because they happened on
another day.
"""

import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
shutil.copyfile(os.path.join(here, "entry.png"), os.path.join(out, "entry.png"))
