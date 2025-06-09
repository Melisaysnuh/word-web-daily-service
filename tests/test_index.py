import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from utilities.custom_types import WordObj
from index import store_list_model, DayModel  # Adjust import path

@pytest.mark.asyncio
@patch("index.insert_day_model")
@patch("index.construct_day")
@patch("index.get_existing_day_model")
@patch("index.ping_db")
@patch("index.get_db_client")
async def test_store_list_model_inserts_new_day_model(
    mock_get_db_client,
    mock_ping_db,
    mock_get_existing_day_model,
    mock_construct_day,
    mock_insert_day_model
):
    # Arrange: Setup mock values
    mock_db = MagicMock()
    mock_get_db_client.return_value = MagicMock(__getitem__=lambda _, x: mock_db)
    mock_ping_db.return_value = True
    mock_get_existing_day_model.return_value = None

    fake_day_model = DayModel(
        centerLetter='a',
        letters=['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        validWords=[WordObj(word="face"), WordObj(word="badge")],
        daylist_id=datetime.now().strftime("%Y_%m_%d"),
        isograms=[WordObj(word="face")],
        total_points=49
    )

    mock_construct_day.return_value = fake_day_model
    mock_insert_day_model.return_value = fake_day_model

    # Act
    result = await store_list_model()

    # Assert
    assert isinstance(result, DayModel)
    mock_get_db_client.assert_called_once()
    mock_ping_db.assert_called_once()
    mock_get_existing_day_model.assert_called_once()
    mock_construct_day.assert_called_once()
    mock_insert_day_model.assert_called_once_with(mock_db, fake_day_model)
