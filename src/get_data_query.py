"""
Raster Data Access
==================

Return raster(xarray.Dataset) at any range and of any resolution.
"""

import xarray as xr
import pandas as pd

RAW_RESOLUTION = 0.25  # 0.25 degree x 0.25 degree


def raster_data_access(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    spatial_resolution: float,  # e.g., 0.25, 0.5, 1.0, 2.5, 5.0
    spatial_agg_method: str,  # e.g., "mean", "max", "min"
    start_datetime: str,
    end_datetime: str,
    time_resolution: str,  # e.g., "hour", "day", "month", "year"
    time_agg_method: str,  # e.g., "mean", "max", "min"
) -> xr.Dataset:
    """
    "get data of a certain variable V over area A (at some spatial resolurion) and time period T (at some time resolution)"
    E.g., "get average temperature of Greenland (1 degree x 1 degree) over the last year (daily)."
    """
    return xr.Dataset()


def gen_file_name(variable: str, datetime: str) -> str:
    """
    Generate the file name for the given variable and datetime
    """
    datetime = datetime.split(" ")[0]  # transform datetime, e.g., "2023-01-01 00:00:00" -> "2023-01-01"
    return f"../data/ERA5/{variable}-{datetime}.nc"


def get_coarsen_factor(spatial_resolution: float) -> int:
    return int(spatial_resolution / RAW_RESOLUTION)


def st_resample(xa, spatial_resolution: float, spatial_agg_method: str, time_resolution: str, time_agg_method: str) -> xr.Dataset:
    """
    Resample the time dimension of the given xarray.Dataset
    """
    # spatial re-resolution
    coarsen_factor = get_coarsen_factor(spatial_resolution)
    xa = xa.coarsen(latitude=coarsen_factor, longitude=coarsen_factor, boundary="trim")
    if spatial_agg_method == "mean":
        xa = xa.mean()
    elif spatial_agg_method == "max":
        xa = xa.max()
    elif spatial_agg_method == "min":
        xa = xa.min()
    else:
        raise ValueError(f"Unknown spatial_agg_method: {spatial_agg_method}")

    # temporal re-resolution
    if time_resolution == "hour":
        return xa
    elif time_resolution == "day":
        xa = xa.resample(time="D")
    elif time_resolution == "month":
        xa = xa.resample(time="M")
    elif time_resolution == "year":
        xa = xa.resample(time="Y")
    else:
        raise ValueError(f"Invalid time resolution: {time_resolution}")

    if time_agg_method == "mean":
        xa = xa.mean()
    elif time_agg_method == "max":
        xa = xa.max()
    elif time_agg_method == "min":
        xa = xa.min()
    else:
        raise ValueError(f"Unknown time_agg_method: {time_agg_method}")
    return xa


def raster_data_access_single_file(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    spatial_resolution: float = 0.25,  # e.g., 0.25, 0.5, 1.0, 2.5, 5.0
    spatial_agg_method: str = "mean",  # e.g., "mean", "max", "min"
    time_resolution: str = "hour",  # e.g., "hour", "day", "month", "year"
    time_agg_method: str = "mean",  # e.g., "mean", "max", "min"
) -> xr.Dataset:
    file_name = gen_file_name(variable, start_datetime)
    xa = xr.open_dataset(file_name)
    xa = xa.sel(
        latitude=slice(max_lat, min_lat),
        longitude=slice(min_lon, max_lon),
        time=slice(start_datetime, end_datetime),
    )
    return st_resample(xa, spatial_resolution, spatial_agg_method, time_resolution, time_agg_method)


def raster_data_access_multiple_files(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    spatial_resolution: float = 0.25,  # e.g., 0.25, 0.5, 1.0, 2.5, 5.0
    spatial_agg_method: str = "mean",  # e.g., "mean", "max", "min"
    time_resolution: str = "hour",  # e.g., "hour", "day", "month", "year"
    time_agg_method: str = "mean",  # e.g., "mean", "max", "min"
) -> xr.Dataset:
    date_range = pd.date_range(start=start_datetime, end=end_datetime)
    xa_list = []
    for d in date_range:
        fname = gen_file_name(variable, str(d))
        xa = xr.open_dataset(fname)
        xa_list.append(xa)
    xa = xr.concat(xa_list, dim="time")
    xa = xa.sel(
        latitude=slice(max_lat, min_lat),
        longitude=slice(min_lon, max_lon),
        time=slice(start_datetime, end_datetime),
    )
    return st_resample(xa, spatial_resolution, spatial_agg_method, time_resolution, time_agg_method)
