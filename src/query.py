"""
Query Functions
===============

All queries should return result as xarray.Dataset.
"""

import xarray


def single_value_aggregation_query(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    aggregation_method: str,  # e.g., "mean", "max", "min"
) -> xarray.Dataset:
    """
    "have a single value of a certain variable V over area A and time period T"
    E.g., "find the average temperature of Greenland over the last year."
    """
    xa = xarray.open_dataset("data/ERA5/2m_temperature-2023-01-01.nc")  # TODO: Load the correct dataset
    xa = xa.sel(
        latitude=slice(max_lat, min_lat),
        longitude=slice(min_lon, max_lon),
        time=slice(start_datetime, end_datetime),
    )
    if aggregation_method == "mean":
        result = xa.mean()
    elif aggregation_method == "max":
        result = xa.max()
    elif aggregation_method == "min":
        result = xa.min()
    else:
        raise ValueError(f"Invalid aggregation method: {aggregation_method}")
    return result


def time_series_query(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    time_resolution: str,
    aggregation_method: str,  # e.g., "mean", "max", "min"
) -> xarray.Dataset:
    """
    "have a time series of a certain variable V over area A and time period T"
    E.g., "draw the average temperature heatmap of Greenland over the last year."
    """
    # TODO: Implement this function
    return xarray.Dataset()


def heat_map_query(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    aggregation_method: str,  # e.g., "mean", "max", "min"
) -> xarray.Dataset:
    """
    "have the heatmap of a certain variable V over a certain area A and certain time period T"
    E.g., "draw the average temperature heatmap of Green- land over the last year."
    """
    # TODO: Implement this function
    return xarray.Dataset()


def value_predicate_query(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    predicate_verb: str,  # e.g., "=", ">", "<", ">=", "<=", "!="
    predicate_value: float,
) -> xarray.Dataset:
    """
    "retrieve records based on a certain variable criteria"
    E.g., "find all data records in the world over the last year where the temperature has exceeded 240."
    """
    # TODO: Implement this function
    return xarray.Dataset()


def arbitrary_shape_query(
    variable: str,
    shape: str,  # e.g., "greenland", "iceland", "tri", "rec"
    start_datetime: str,
    end_datetime: str,
) -> xarray.Dataset:
    """
    "retrieve records within an arbitrary shape"
    E.g., "find all data records in Greenland over the last year."
    """
    # TODO: Implement this function
    return xarray.Dataset()
