"""Unit tests for preprocessing, missing values, and scaling."""

import numpy as np
import pandas as pd
import pytest

from ddos_ai.data.missing_values import MissingValueHandler
from ddos_ai.data.preprocessing import Preprocessor
from ddos_ai.data.feature_engineering import FeatureEngineer


def test_missing_value_handler():
    df = pd.DataFrame({
        "Flow Duration": [100.0, np.nan, 300.0, np.inf],
        "Packets": [10.0, 20.0, np.nan, 40.0],
    })
    handler = MissingValueHandler(strategy="median")
    df_clean = handler.fit_transform(df)

    assert not np.isnan(df_clean.values).any()
    assert not np.isinf(df_clean.values).any()
    assert df_clean["Flow Duration"].iloc[1] == 200.0  # median of 100 and 300


def test_feature_engineering():
    df = pd.DataFrame({
        "Total Fwd Packets": [100.0, 50.0],
        "Total Backward Packets": [10.0, 50.0],
        "SYN Flag Count": [10.0, 0.0],
        "ACK Flag Count": [0.0, 10.0],
    })
    fe = FeatureEngineer()
    df_feat = fe.compute_flow_features(df)

    assert "Packet_Asymmetry_Ratio" in df_feat.columns
    assert "SYN_to_ACK_Ratio" in df_feat.columns
    assert df_feat["Packet_Asymmetry_Ratio"].iloc[0] > 0.5


def test_preprocessor_end_to_end():
    df = pd.DataFrame({
        "Flow Duration": [100.0, 200.0, 300.0, 400.0],
        "Total Fwd Packets": [10.0, 20.0, 30.0, 40.0],
        "Label": ["BENIGN", "Syn", "BENIGN", "Syn"],
    })
    pre = Preprocessor(scaler_type="robust")
    X, y = pre.fit_transform(df)

    assert X.shape == (4, 2)
    assert y.shape == (4,)
    assert len(pre.label_encoder.classes_) == 2
