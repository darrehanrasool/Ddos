"""Integration test verifying end-to-end data pipeline from synthesis to splitting."""

import tempfile
from pathlib import Path
import pytest
import pandas as pd

from ddos_ai.data.dataset_downloader import DatasetDownloader
from ddos_ai.data.feature_engineering import FeatureEngineer
from ddos_ai.data.preprocessing import Preprocessor
from ddos_ai.data.data_splitting import DataSplitter


def test_full_data_pipeline():
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = DatasetDownloader(raw_dir=tmpdir)
        sample_path = downloader.generate_synthetic_benchmark("CIC-DDoS2019", n_samples=200)

        assert sample_path.exists()
        df = pd.read_csv(sample_path)
        assert len(df) == 200

        # Feature engineering
        fe = FeatureEngineer()
        df_feat = fe.compute_flow_features(df)
        assert df_feat.shape[1] > df.shape[1]

        # Splitting
        splitter = DataSplitter(train_ratio=0.70, val_ratio=0.15, test_ratio=0.15)
        train_df, val_df, test_df = splitter.split(df_feat)
        assert len(train_df) == 140
        assert len(val_df) == 30
        assert len(test_df) == 30

        # Preprocessing
        pre = Preprocessor()
        X_train, y_train = pre.fit_transform(train_df)
        X_test, y_test = pre.transform(test_df)

        assert X_train.shape[0] == 140
        assert X_test.shape[0] == 30
