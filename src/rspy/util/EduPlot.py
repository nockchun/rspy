import numpy as np
from matplotlib import pyplot, ticker, get_backend, rc
from functools import wraps

class EduPlotConf(object):
    def __init__(
        self, font='serif', fontSize=5, dpi=160, figScale=1, linewidth=1, markersize=4,
        gridParams = {'linewidth': 0.2, 'alpha': 0.5},
        quiverParams = {'angles': 'xy', 'scale_units': 'xy', 'scale': 1, 'width': 0.005, "headwidth":5, "headaxislength":3}
    ):
        self.font = font
        self.fontSize = fontSize
        self.dpi = dpi
        self.figSize = np.array([3,3]) * figScale
        self.linewidth = linewidth
        self.markersize = markersize
        self.gridParams = gridParams
        self.quiverParams = quiverParams
        
    def set(self):
        rc('font', family=self.font, size=self.fontSize)
        rc('figure', dpi=self.dpi)
        rc('lines', linewidth=self.linewidth, markersize=self.markersize)


class EduPlot2D(object):
    def __init__(self, conf=EduPlotConf()):
        self._vectors   = {}
        self._functions = {}
        self._markers   = {}
        self._conf      = conf
        conf.set()
        
    def genSpace(self, xLim, yLim=None, title=None):
        # input check
        if isinstance(xLim, int): xLim = [-xLim, xLim]
        else: assert len(xLim) == 2, "xLim should have 2 elements list. [-2, 4]"
        if yLim is None: yLim = xLim
        else:
            if isinstance(yLim, int): yLim = [-yLim, yLim]
            else: assert len(yLim) == 2, "xLim should have 2 elements list. [-2, 4]"
        assert xLim[0] <= 0 <= xLim[1], "xLim range should contain 0 elements"
        assert yLim[0] <= 0 <= yLim[1], "yLim range should contain 0 elements"
            
        # create panal with limit
        self._figure, self._axis = pyplot.subplots(figsize=self._conf.figSize)
        if title is not None: self._figure.suptitle(title);
        self._axis.set_xlim(xLim)
        self._axis.set_ylim(yLim)
        self._axis.set_aspect('equal')

        xticks = self._axis.get_xticks()
        yticks = self._axis.get_yticks()
        dx = xticks[1] - xticks[0]
        dy = yticks[1] - yticks[0]
        base = max(int(min(dx, dy)), 1)   # grid interval is always an integer
        loc = ticker.MultipleLocator(base=base)
        self._axis.xaxis.set_major_locator(loc)
        self._axis.yaxis.set_major_locator(loc)
        self._axis.grid(True, **self._conf.gridParams)

        # show x-y axis in the center, hide frames
        self._axis.spines['left'].set_position(('data', 0))
        self._axis.spines['bottom'].set_position(('data', 0))
        self._axis.spines['right'].set_color('none')
        self._axis.spines['top'].set_color('none')
        
        # draw plot
        for name in self._vectors:
            self._axis.quiver(self._vectors[name]["origins"][:,0], self._vectors[name]["origins"][:,1],
                              self._vectors[name]["vectors"][:,0], self._vectors[name]["vectors"][:,1],
                              color=self._vectors[name]["color"], **self._conf.quiverParams)
            
        for name in self._functions:
            x = np.linspace(xLim[0], xLim[1], self._functions[name]["linespace"])
            y = eval(self._functions[name]["expression"])
            pyplot.plot(x, y, self._functions[name]["color"])
            
        for name in self._markers:
            pyplot.plot(self._markers[name]["positions"][:,0], self._markers[name]["positions"][:,1], marker=".",
                        linewidth=0, color=self._markers[name]["color"])
            
    def addVector(self, vectors, origins=None, name="vector", color="#0000FF"):
        vectors = np.array(vectors)
        assert vectors.shape[1] == 2, "Each vector should have 2 elements."  
        if origins is not None:
            origins = np.array(origins)
            assert origins.shape[1] == 2, "Each tail should have 2 elements."
        else:
            origins = np.zeros_like(vectors)
        
        nvectors = vectors.shape[0]
        norigins = origins.shape[0]
        if nvectors == 1 and norigins > 1:
            vectors = np.tile(vectors, (norigins, 1))
        elif norigins == 1 and nvectors > 1:
            origins = np.tile(origins, (nvectors, 1))
        else:
            assert origins.shape == vectors.shape, "vectors and tail must have a same shape"
            
        self._vectors[name] = {"vectors":vectors, "origins":origins, "color":color}
    
    def addFunction(self, expX_ForY="x**2", linespace=100, name="function", color="#FF0000"):
        self._functions[name] = {"expression":expX_ForY, "linespace":linespace, "color":color}
        
    def addMarker(self, positions, mark=".", name="marker", color="#00FF00"):
        self._markers[name] = {"positions":np.array(positions), "mark":mark, "color":color}
        
    def setConf(self, conf):
        self._conf = conf
        conf.set()
    
    def getConf(self):
        return self._conf
