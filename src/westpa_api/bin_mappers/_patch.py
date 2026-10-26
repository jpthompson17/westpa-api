import warnings

import numpy as np

from westpa.core.binning.assign import BinMapper, coord_dtype, index_dtype


@warnings.deprecated("westpa.core.binning.assign.BinMapper is deprecated. Use BinMapperBase instead.")
def __call__(self, segments, coord_index=-1):
    coord_ndim = segments[0].pcoord.shape[1]
    coords = np.empty((len(segments), coord_ndim), coord_dtype)
    for i, segment in enumerate(segments):
        coords[i] = segment.pcoord[coord_index]

    output = np.empty(len(segments), dtype=index_dtype)
    self.assign(coords, mask=None, output=output)

    return output


BinMapper.__call__ = __call__  # noqa
