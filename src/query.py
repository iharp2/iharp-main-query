"""
Query Functions
===============

All queries should return result as xarray.Dataset.
"""

import xarray as xr
from get_data_query import *
import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
import odc.geo.xr

variable_short_name = {
    "2m_temperature": "t2m",
}


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
    xa = raster_data_access_multiple_files(
        variable=variable,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
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
    xa = raster_data_access_multiple_files(
        variable=variable,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
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


def heat_map_query_single_layer(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    spatial_resolution: float = 0.25,  # e.g., 0.25, 0.5, 1.0, 2.5, 5.0
    spatial_agg_method: str = "mean",  # e.g., "mean", "max", "min"
    time_agg_method: str = "mean",  # e.g., "mean", "max", "min"
) -> xr.Dataset:
    """
    "have the heatmap of a certain variable V over a certain area A and certain time period T"
    E.g., "draw the average temperature heatmap of Green- land over the last year."
    """
    xa = raster_data_access_multiple_files(
        variable=variable,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        spatial_resolution=spatial_resolution,
        spatial_agg_method=spatial_agg_method,
    )
    if time_agg_method == "mean":
        result = xa.mean(dim="time")
    elif time_agg_method == "max":
        result = xa.max(dim="time")
    elif time_agg_method == "min":
        result = xa.min(dim="time")
    else:
        raise ValueError(f"Invalid aggregation method: {time_agg_method}")
    return result


def heat_map_query_multi_layer(
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
    return raster_data_access_multiple_files(
        variable=variable,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        spatial_resolution=spatial_resolution,
        spatial_agg_method=spatial_agg_method,
        time_resolution=time_resolution,
        time_agg_method=time_agg_method,
    )


def value_criteria_query(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    criteria_predicate: str,  # e.g., "=", ">", "<"
    criteria_value: float,
    spatial_resolution: float = 0.25,  # e.g., 0.25, 0.5, 1.0, 2.5, 5.0
    spatial_agg_method: str = "mean",  # e.g., "mean", "max", "min"
    time_resolution: str = "hour",  # e.g., "hour", "day", "month", "year"
    time_agg_method: str = "mean",  # e.g., "mean", "max", "min"
) -> xr.Dataset:
    xa = raster_data_access_multiple_files(
        variable=variable,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        spatial_resolution=spatial_resolution,
        spatial_agg_method=spatial_agg_method,
        time_resolution=time_resolution,
        time_agg_method=time_agg_method,
    )
    if criteria_predicate == "=":
        result = xa.where(xa == criteria_value)
    elif criteria_predicate == ">":
        result = xa.where(xa > criteria_value)
    elif criteria_predicate == "<":
        result = xa.where(xa < criteria_value)
    else:
        raise ValueError(f"Invalid criteria predicate: {criteria_predicate}")
    return result


def area_finding_query(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    criteria_predicate: str,  # e.g., "=", ">", "<"
    criteria_value: float,
    any_or_all: str,  # e.g., "any", "all"
    spatial_resolution: float = 0.25,  # e.g., 0.25, 0.5, 1.0, 2.5, 5.0
    spatial_agg_method: str = "mean",  # e.g., "mean", "max", "min"
    time_resolution: str = "hour",  # e.g., "hour", "day", "month", "year"
    time_agg_method: str = "mean",  # e.g., "mean", "max", "min"
) -> xr.Dataset:
    xa = value_criteria_query(
        variable=variable,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        criteria_predicate=criteria_predicate,
        criteria_value=criteria_value,
        spatial_resolution=spatial_resolution,
        spatial_agg_method=spatial_agg_method,
        time_resolution=time_resolution,
        time_agg_method=time_agg_method,
    )
    short_name = variable_short_name[variable]
    if any_or_all == "any":
        xa["spatial_mask"] = xa[short_name].notnull().any(dim=["time"]).astype(bool)
    elif any_or_all == "all":
        xa["spatial_mask"] = xa[short_name].notnull().all(dim=["time"]).astype(bool)
    else:
        raise ValueError(f"Invalid any_or_all: {any_or_all}")
    return xa


def time_period_query(
    variable: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_datetime: str,
    end_datetime: str,
    criteria_predicate: str,  # e.g., "=", ">", "<"
    criteria_value: float,
    any_or_all: str,  # e.g., "any", "all"
    spatial_resolution: float = 0.25,  # e.g., 0.25, 0.5, 1.0, 2.5, 5.0
    spatial_agg_method: str = "mean",  # e.g., "mean", "max", "min"
    time_resolution: str = "hour",  # e.g., "hour", "day", "month", "year"
    time_agg_method: str = "mean",  # e.g., "mean", "max", "min"
) -> xr.Dataset:
    xa = value_criteria_query(
        variable=variable,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        criteria_predicate=criteria_predicate,
        criteria_value=criteria_value,
        spatial_resolution=spatial_resolution,
        spatial_agg_method=spatial_agg_method,
        time_resolution=time_resolution,
        time_agg_method=time_agg_method,
    )
    short_name = variable_short_name[variable]
    if any_or_all == "any":
        xa["time_mask"] = xa[short_name].notnull().any(dim=["latitude", "longitude"]).astype(bool)
    elif any_or_all == "all":
        xa["time_mask"] = xa[short_name].notnull().all(dim=["latitude", "longitude"]).astype(bool)
    else:
        raise ValueError(f"Invalid any_or_all: {any_or_all}")
    return xa


def shape_query(
    variable: str,
    shape_fpath: str,
    start_datetime: str,
    end_datetime: str,
    spatial_resolution: float = 0.25,  # e.g., 0.25, 0.5, 1.0, 2.5, 5.0
    spatial_agg_method: str = "mean",  # e.g., "mean", "max", "min"
    time_resolution: str = "hour",  # e.g., "hour", "day", "month", "year"
    time_agg_method: str = "mean",  # e.g., "mean", "max", "min"
) -> xr.Dataset:
    gdf_shape = gpd.read_file(shape_fpath)
    xa = raster_data_access_multiple_files(
        variable=variable,
        min_lat=gdf_shape.bounds.miny[0],
        max_lat=gdf_shape.bounds.maxy[0],
        min_lon=gdf_shape.bounds.minx[0],
        max_lon=gdf_shape.bounds.maxx[0],
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        spatial_resolution=spatial_resolution,
        spatial_agg_method=spatial_agg_method,
        time_resolution=time_resolution,
        time_agg_method=time_agg_method,
    )

    geom_mask = geometry_mask(geometries=gdf_shape.iloc[0], out_shape=xa.odc.geobox.shape, transform=xa.odc.geobox.affine, invert=True)
    xa = xa.assign(shape_mask=(("latitude", "longitude"), geom_mask))
    return xa
