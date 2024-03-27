import xarray
from context import *


def test_time_series_query():
    result = time_series_query(
        variable="2m_temperature",
        start_datetime="2023-01-01 00:00:00",
        end_datetime="2023-01-01 10:00:00",
        min_lat=50,
        max_lat=55,
        min_lon=10,
        max_lon=15,
        time_resolution="hour",
        aggregation_method="mean",
    )
    assert isinstance(result, xarray.DataArray)
    # assert result.shape == (0, 0, 0)
    # assert result.values == xarray.DataArray().values
