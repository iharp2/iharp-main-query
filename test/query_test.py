import xarray
from context import *

MIN_LAT = 60
MAX_LAT = 80
MIN_LON = 285
MAX_LON = 350
START_DATETIME = "2023-01-01 00:00:00"
END_DATETIME = "2023-01-01 09:00:00"


def test_single_value_aggregation_query():
    result = single_value_aggregation_query(
        variable="2m_temperature",
        min_lat=MIN_LAT,
        max_lat=MAX_LAT,
        min_lon=MIN_LON,
        max_lon=MAX_LON,
        start_datetime=START_DATETIME,
        end_datetime=END_DATETIME,
        aggregation_method="mean",
    )
    print(result.info())
    assert isinstance(result, xarray.Dataset)  # check on type
    assert result.sizes == xarray.core.utils.Frozen({})  # check on size
    assert result.t2m.values[()] == 251.92674  # check on value

