"""
Query Functions
===============

All queries should return result as xarray.Dataset.
"""

import xarray as xr


def gen_file_name(variable: str, datetime: str) -> str:
    """
    Generate the file name for the given variable and datetime
    """
    datetime = datetime.split(" ")[0]  # transform datetime, e.g., "2023-01-01 00:00:00" -> "2023-01-01"
    return f"data/ERA5/{variable}-{datetime}.nc"


def single_value_aggregation_query(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    aggregation_method: str,  # e.g., "mean", "max", "min"
) -> xr.Dataset:
    """
    "have a single value of a certain variable V over area A and time period T"
    E.g., "find the average temperature of Greenland over the last year."
    """
    file_name = gen_file_name(variable, start_datetime)
    xa = xr.open_dataset(file_name)
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
    time_resolution: str,  # e.g., "hour", "day", "month", "year"
    aggregation_method: str,  # e.g., "mean", "max", "min"
) -> xr.Dataset:
    """
    "have a time series of a certain variable V over area A and time period T"
    E.g., "draw the average temperature heatmap of Greenland over the last year."
    """
    file_name = gen_file_name(variable, start_datetime)
    xa = xr.open_dataset(file_name)
    xa = xa.sel(
        latitude=slice(max_lat, min_lat),
        longitude=slice(min_lon, max_lon),
        time=slice(start_datetime, end_datetime),
    )

    def resample_time_resolution(xa, time_resolution):
        """
        Resample xa to the given time resolution
        Equivalent to SQL's GROUP BY time
        """
        if time_resolution == "day":
            xa = xa.resample(time="D")
        elif time_resolution == "month":
            xa = xa.resample(time="M")
        elif time_resolution == "year":
            xa = xa.resample(time="Y")
        else:
            raise ValueError(f"Invalid time resolution: {time_resolution}")
        return xa

    if aggregation_method == "mean":
        result = xa.mean(dim=["latitude", "longitude"])
    elif aggregation_method == "max":
        result = xa.max(dim=["latitude", "longitude"])
    elif aggregation_method == "min":
        result = xa.min(dim=["latitude", "longitude"])
    else:
        raise ValueError(f"Invalid aggregation method: {aggregation_method}")

    if time_resolution != "hour":
        result = resample_time_resolution(result, time_resolution)
        if aggregation_method == "mean":
            result = result.mean()
        elif aggregation_method == "max":
            result = result.max()
        elif aggregation_method == "min":
            result = result.min()

    return result


def heat_map_query(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    aggregation_method: str,  # e.g., "mean", "max", "min"
) -> xr.Dataset:
    """
    "have the heatmap of a certain variable V over a certain area A and certain time period T"
    E.g., "draw the average temperature heatmap of Green- land over the last year."
    """
    # TODO: Implement this function
    return xr.Dataset()


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
) -> xr.Dataset:
    """
    "retrieve records based on a certain variable criteria"
    E.g., "find all data records in the world over the last year where the temperature has exceeded 240."
    """
    # TODO: Implement this function
    return xr.Dataset()


def arbitrary_shape_query(
    variable: str,
    shape: str,  # e.g., "greenland", "iceland", "tri", "rec"
    start_datetime: str,
    end_datetime: str,
) -> xr.Dataset:
    """
    "retrieve records within an arbitrary shape"
    E.g., "find all data records in Greenland over the last year."
    """
    # TODO: Implement this function
    return xr.Dataset()
