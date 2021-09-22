import pandas as pd

from etna.datasets.tsdataset import TSDataset
from etna.models import ProphetModel


def test_run(new_format_df):
    df = new_format_df

    ts = TSDataset(df, "1d")

    model = ProphetModel()
    model.fit(ts)
    future_ts = ts.make_future(3)
    model.forecast(future_ts)
    if not future_ts.isnull().values.any():
        assert True
    else:
        assert False


def test_run_with_reg(new_format_df, new_format_exog):
    df = new_format_df

    regressors = new_format_exog.copy()
    regressors.columns = pd.MultiIndex.from_arrays(
        [regressors.columns.get_level_values("segment").unique().tolist(), ["regressor_exog", "regressor_exog"]]
    )
    regressors_cap = new_format_exog.copy()
    regressors_cap.columns = pd.MultiIndex.from_arrays(
        [regressors_cap.columns.get_level_values("segment").unique().tolist(), ["regressor_cap", "regressor_cap"]]
    )
    exog = pd.concat([regressors, regressors_cap], axis=1)

    ts = TSDataset(df, "1d", df_exog=exog)

    model = ProphetModel()
    model.fit(ts)
    future_ts = ts.make_future(3)
    model.forecast(future_ts)
    if not future_ts.isnull().values.any():
        assert True
    else:
        assert False
