"""rio_tiler_fs.reader: Custom COGReader."""

import typing
import warnings

import attr
import fsspec
import rasterio
from rasterio.io import DatasetReader

from rio_tiler.errors import NoOverviewWarning
from rio_tiler.io import cogeo


@attr.s
class COGReader(cogeo.COGReader):
    """Custom COGReader using fsspec."""

    fs: typing.Optional[fsspec.AbstractFileSystem] = attr.ib(default=None)
    storage_options: typing.Dict = attr.ib(factory=dict)

    fs_obj: fsspec.core.OpenFile = attr.ib(init=False)
    dataset: DatasetReader = attr.ib(init=False)

    def __attrs_post_init__(self):
        """Define _kwargs, open dataset and get info."""
        if self.nodata is not None:
            self._kwargs["nodata"] = self.nodata
        if self.unscale is not None:
            self._kwargs["unscale"] = self.unscale
        if self.resampling_method is not None:
            self._kwargs["resampling_method"] = self.resampling_method
        if self.vrt_options is not None:
            self._kwargs["vrt_options"] = self.vrt_options
        if self.post_process is not None:
            self._kwargs["post_process"] = self.post_process

        if self.fs is None:
            self.fs, self.input = fsspec.core.url_to_fs(
                self.input, **self.storage_options
            )

        self.fs_obj = self._ctx_stack.enter_context(self.fs.open(self.input))
        self.dataset = self._ctx_stack.enter_context(rasterio.open(self.fs_obj))

        self.bounds = tuple(self.dataset.bounds)
        self.crs = self.dataset.crs

        self.nodata = self.nodata if self.nodata is not None else self.dataset.nodata

        if self.minzoom is None or self.maxzoom is None:
            self._set_zooms()

        if self.colormap is None:
            self._get_colormap()

        if min(
            self.dataset.width, self.dataset.height
        ) > 512 and not self.dataset.overviews(1):
            warnings.warn(
                "The dataset has no Overviews. rio-tiler performances might be impacted.",
                NoOverviewWarning,
            )
