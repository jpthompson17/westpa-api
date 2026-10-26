from westpa.core.binning import RectilinearBinMapper as _RectilinearBinMapper, index_dtype

from .base import BinMapperBase


class RectilinearBinMapper(BinMapperBase):
    """Maps coordinates to cells in a rectilinear grid.

    Parameters
    ----------
    boundaries : iterable of 1-D array-like
        Bin boundaries along each coordinate axis. The values in each array
        must be monotonically increasing.
    **kwargs
        Keyword arguments to pass to the :class:`BinMapperBase` class.

    Attributes
    ----------
    labels : list of str
        Bin labels.
    nbins : int
        Number of bins mapped to.
    ndim : int
        Coordinate space dimension.
    boundaries : iterable of 1-D array-like
        Bin boundaries along each coordinate axis.

    Examples
    --------
    >>> import westpa
    >>> bin_mapper = westpa.RectilinearBinMapper([[0., 1., 2., 3., 4., 5.]])
    >>> bin_mapper.nbins
    5
    >>> bin_mapper.ndim
    1

    """

    def __init__(self, boundaries, **kwargs):
        super().__init__(**kwargs)
        self._mapper = _RectilinearBinMapper(boundaries)

    @property
    def labels(self):
        return iter(self._mapper.labels)

    def assign(self, coords, weights, output):
        return self._mapper.assign(coords, None, output.astype(index_dtype))
