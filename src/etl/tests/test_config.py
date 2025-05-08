import pytest
from unittest import mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from etl.main import fetch_config_flags


@pytest.fixture
def mock_db_engine():
    # Mock the SQLAlchemy engine and connection
    engine = mock.Mock()
    conn = mock.Mock()
    engine.connect.return_value = conn
    return engine


def test_fetch_config_flags(mock_db_engine):
    # Mock the database result
    mock_result = mock.Mock()
    mock_result._mapping = {'is_ingestion_enabled': True, 'is_transformation_enabled': False}
    mock_db_engine.connect.return_value.execute.return_value.fetchone.return_value = mock_result

    # Run the function
    flags = fetch_config_flags(mock_db_engine)

    # Validate results
    assert flags['is_ingestion_enabled'] is True
    assert flags['is_transformation_enabled'] is False
