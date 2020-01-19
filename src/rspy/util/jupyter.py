import math, re
import ipywidgets as ipw
from matplotlib import font_manager

def showMulti(*args, colSize=None, width="100%", margin="3px"):
    """Display multiple output data lines and columns as desired.
    Args:
      args: multiple datas.
      colSize: column size.
      width: css style width parameter. default is 100%. you can use "px" unint.
      margin: css style margin parameter. default is 3px.
    Returns:
      None
    Example:
      >>> showMulti("a", "b", "c", colSize=2)
      a      b
      c
    """

    # calculate column and row counts.
    lenArgs = len(args)
    if (colSize is not None) and (colSize > 0) and (lenArgs - colSize > 0):
        lenRow = math.ceil(lenArgs/colSize)
        lenCol = colSize
    else:
        lenRow = 1
        lenCol = lenArgs

    # create Output() of ipywidgets and to display the args to it.
    layout = ipw.Layout(width=width, grid_gap=margin)
    grid = ipw.GridspecLayout(lenRow, lenCol, layout=layout)
    outs = [ipw.Output() for _ in range(len(args))]
    for idx, out in enumerate(outs):
        with out:
            display(args[idx])

    # allocate Output() to grid
    idxOuts = 0
    for row in range(lenRow):
        for col in range(lenCol):
            grid[row, col] = outs[idxOuts] if idxOuts < lenArgs else ipw.Output()
            idxOuts += 1
    display(grid)

def getSystemFonts(self, hintRegex=""):
    regex = re.compile(hintRegex, re.IGNORECASE)
    return [{f.name: f.fname} for f in font_manager.fontManager.ttflist if regex.search(f.fname)]