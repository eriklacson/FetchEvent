import pytest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from FetchEvent import (
    initialize_config,
    parse_arguments,
    fetch_event_data,
    process_event_data,
    save_to_csv,
    handle_errors
)

def test_initialize_config():
    with patch("FetchEvent.load_dotenv", return_value=True), \
         patch("FetchEvent.os.getenv", side_effect=["dummy_api_key", "dummy_app_key"]):
        config = initialize_config()
        assert config.api_key["apiKeyAuth"] == "dummy_api_key"
        assert config.api_key["appKeyAuth"] == "dummy_app_key"

def test_parse_arguments():
    test_args = ["--query", "test_query", "--days", "7"]
    with patch("FetchEvent.argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(query="test_query", days=7)):
        args = parse_arguments()
        assert args.query == "test_query"
        assert args.days == 7

def test_fetch_event_data():
    mock_events_api = MagicMock()
    mock_events_api.list_events.return_value = MagicMock(data=["event1", "event2"])
    events = fetch_event_data(mock_events_api, "test_query", 7)
    assert events == ["event1", "event2"]

def test_process_event_data():
    mock_event_data = [
        MagicMock(
            id="1",
            type="type1",
            attributes=MagicMock(
                tags=["tag1", "tag2"],
                timestamp=pd.Timestamp("2023-01-01 00:00:00"),
                attributes={"title": "Event Title", "status": "Active"}
            )
        )
    ]
    processed_df = process_event_data(mock_event_data)
    assert isinstance(processed_df, pd.DataFrame)
    assert not processed_df.empty
    assert processed_df.iloc[0]["event_title"] == "Event Title"

def test_save_to_csv(tmp_path):
    test_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    output_dir = tmp_path / "output"
    output_file = output_dir / "events_output.csv"
    save_to_csv(test_df, str(output_dir), str(output_file))
    assert os.path.exists(output_file)

def test_handle_errors(capfd):
    handle_errors("Test error message")
    captured = capfd.readouterr()
    assert "Test error message" in captured.out
