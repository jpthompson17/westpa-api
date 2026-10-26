import numpy as np
from westpa.core.binning import index_dtype


class NOPBinMapper:
    """Put everything into one bin."""

    @property
    def labels(self):
        return ['nop']

    @property
    def nbins(self):
        return 1

    def __call__(self, segments, coord_index=-1):
        return np.zeros(len(segments), dtype=index_dtype)
