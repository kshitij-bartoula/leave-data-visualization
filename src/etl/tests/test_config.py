import pytest
from unittest import mock
from sqlalchemy.engine import Engine
from etl.main import fetch_config_flags

def test_fetch_config_flags():
    # Mock the connection context manager
    mock_engine = mock.MagicMock(spec=Engine)
    mock_conn = mock.MagicMock()
    mock_result = mock.Mock()
    mock_result._mapping = {'is_ingestion_enabled': True, 'is_transformation_enabled': False}

    # Set up return values for context manager
    mock_engine.connect.return_value.__enter__.return_value.execute.return_value.fetchone.return_value = mock_result

    flags = fetch_config_flags(mock_engine)
    assert flags == {'is_ingestion_enabled': True, 'is_transformation_enabled': False}
