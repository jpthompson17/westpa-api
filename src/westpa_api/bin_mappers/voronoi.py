import westpa.core.binning
from .base import BinMapperBase


class VoronoiBinMapper(BinMapperBase):
    """Maps coordinates to cells in a Voronoi diagram.

    Parameters
    ----------
    centers : 2-D array-like
        Voronoi sites.
    dfunc : callable
        Distance function. It must accept arguments
        ``(coord, centers, *dfargs, **dfkwargs)`` and return a 1-D array
        containing the distance of ``coord`` from each point in ``centers``.
    dfargs : tuple, optional
        Extra positional arguments to pass to `dfunc`.
    dfkwargs : Mapping[str, Any], optional
        Extra keyword arguments to pass to `dfunc`.
    **kwargs
        Keyword arguments to pass to the :class:`BinMapperBase` class.

    Attributes
    ----------
    labels : list of str
        Bin labels.
    nbins : int
        Number of bins (sites) mapped to.
    ndim : int
        Coordinate space dimension.
    centers : 2-D numpy.ndarray
        Voronoi sites.
    dfunc : callable
        Distance function.
    dfargs : tuple
        Extra positional arguments to pass to the distance function.
    dfkwargs : Mapping[str, Any]
        Extra keyword arguments to pass to the distance function.

    """

    def __init__(self, centers, dfunc, dfargs=None, dfkwargs=None, **kwargs):
        super().__init__(**kwargs)
        self._mapper = westpa.core.binning.VoronoiBinMapper(
            dfunc=dfunc,
            centers=centers,
            dfargs=dfargs,
            dfkwargs=dfkwargs,
        )

    @property
    def labels(self):
        return iter(self._mapper.labels)

    def assign(self, coords, weights, output):
        return self._mapper.assign(coords, mask=None, output=output)
