import math
import ipywidgets as ipw

def showMulti(*args, colSize=None):
    """Display multiple output data lines and columns as desired.

    Args:
      args: multiple datas.
      colSize: column size.

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
    grid = ipw.GridspecLayout(lenRow, lenCol)
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
