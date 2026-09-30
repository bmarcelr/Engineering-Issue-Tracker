import pytest
import json
from storage import load_data, save_data

def test_save_data(tmp_path):
    test_file = tmp_path / "issues.json"

    tracker_data = {
        "next_issue_number": 2,
        "issues": []
    }

    save_data(tracker_data, test_file)

    with open(test_file, "r") as file:
        saved_data = json.load(file)

    assert saved_data == tracker_data

def test_load_data(tmp_path):
    test_file = tmp_path / "issues.json"

    expected_data = {
        "next_issue_number": 2,
        "issues": []
    }

    with open(test_file, "w") as file:
        json.dump(expected_data, file)

    loaded_data = load_data(test_file)

    assert loaded_data == expected_data