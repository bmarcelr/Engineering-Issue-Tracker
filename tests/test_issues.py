import pytest
from datetime import date, datetime, timedelta

from issues import get_text_input, get_date_input, get_list_input, add_update_comment, show_menu, show_filter_menu, show_update_menu, create_issue, view_single_issue, view_all_issues, search_issues, filter_by_field, view_overdue_issues, update_existing_issue, archive_issues, view_archived_issues

# Define a pytest fixture to cut down on repetition:
@pytest.fixture
def tracker_data():
    return {
        "next_issue_number": 999,
        "issues": [
            {
                "issue_id": "ISSUE-998",
                "issue_title": "Airbag Connector Clash",
                "issue_description": "Harness connector is offset 5mm from airbag connector",
                "issue_status": "Open",
                "record_state": "Active",
                "rag": "Red",
                "assignee": "EDS Engineer",
                "reporter_champion": "Airbag Manager",
                "components": ["Harness", "Airbag", "Seat"],
                "programmes_affected": ["PRG-1", "PRG-2"],
                "builds_affected": ["BUILD-1", "BUILD-2"],
                "date_raised": date.today().isoformat(),
                "target_approval_date": "2026-09-30",
                "target_completion_date": "2026-10-31",
                "comments_updates": [
                    {
                        "date_time": "2026-09-29",
                        "author": "EDS Engineer",
                        "comment": "Issue raised and under investigation"
                    }
                ]
            }
        ]
    } 
@pytest.fixture
def tracker_data_long():
    return {
        "next_issue_number": 999,
        "issues": [
            {
                            "issue_id": "ISSUE-996",
                            "issue_title": "Test 1",
                            "issue_description": "Test desc 1",
                            "issue_status": "Open",
                            "record_state": "Active",
                            "rag": "Red",
                            "assignee": "Test 1",
                            "reporter_champion": "Test 1",
                            "components": ["Harness", "Airbag", "Seat"],
                            "programmes_affected": ["PRG-1", "PRG-2"],
                            "builds_affected": ["BUILD-1", "BUILD-2"],
                            "date_raised": date.today().isoformat(),
                            "target_approval_date": "2026-09-15",
                            "target_completion_date": "2026-10-31",
                            "comments_updates": [
                                {
                                    "date_time": "2026-09-29",
                                    "author": "EDS Engineer",
                                    "comment": "Issue raised and under investigation"
                                }
                            ]
                        },
            {
                            "issue_id": "ISSUE-997",
                            "issue_title": "Test 2",
                            "issue_description": "Test desc 2",
                            "issue_status": "Open",
                            "record_state": "Active",
                            "rag": "Red",
                            "assignee": "Test 2",
                            "reporter_champion": "Test 2",
                            "components": ["Harness", "Airbag", "Seat"],
                            "programmes_affected": ["PRG-1", "PRG-2"],
                            "builds_affected": ["BUILD-1", "BUILD-2"],
                            "date_raised": date.today().isoformat(),
                            "target_approval_date": "2026-09-15",
                            "target_completion_date": "2026-09-28",
                            "comments_updates": [
                                {
                                    "date_time": "2026-09-29",
                                    "author": "EDS Engineer",
                                    "comment": "Issue raised and under investigation"
                                }
                            ]
                        },
            {
                "issue_id": "ISSUE-998",
                "issue_title": "Test 3",
                "issue_description": "Test desc 3",
                "issue_status": "Open",
                "record_state": "Active",
                "rag": "Red",
                "assignee": "Test 3",
                "reporter_champion": "Test 3",
                "components": ["Harness", "Airbag", "Seat"],
                "programmes_affected": ["PRG-1", "PRG-2"],
                "builds_affected": ["BUILD-1", "BUILD-2"],
                "date_raised": date.today().isoformat(),
                "target_approval_date": "2026-09-30",
                "target_completion_date": "2026-10-31",
                "comments_updates": [
                    {
                        "date_time": "2026-09-29",
                        "author": "EDS Engineer",
                        "comment": "Issue raised and under investigation"
                    }
                ]
            }
        ]
    } 

# Basic Functions
#
#

def test_get_text_input_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Testing")
    
    test = get_text_input("Enter Text: ")

    assert test == "Testing"

def test_get_text_input_invalid(monkeypatch):
    inputs = iter(["", "Testing"])
    
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    test = get_text_input("Enter Text: ")

    assert test == "Testing"

def test_get_text_input_strip(monkeypatch):
    inputs = iter(["  ", "Testing"])
    
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    test = get_text_input("Enter Text: ")

    assert test == "Testing"

def test_get_date_input_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "2026-10-12")
    
    test = get_date_input("Enter Date: ")

    assert test == date(2026, 10, 12)

def test_get_date_input_empty(monkeypatch, capsys):
    inputs = iter(["string", "2026-10-12"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    test = get_date_input("Enter Date: ")
    captured = capsys.readouterr()

    assert "Please enter dates in YYYY-MM-DD format." in captured.out
    assert test == date(2026, 10, 12)

def test_get_date_input_invalid(monkeypatch, capsys):
    inputs = iter(["2026-15-35", "2026-10-12"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    test = get_date_input("Enter Date: ")
    captured = capsys.readouterr()

    assert "Please enter dates in YYYY-MM-DD format." in captured.out
    assert test == date(2026, 10, 12)

def test_get_list_input_valid(monkeypatch):
    
    list_input = "test_1, test_2"

    monkeypatch.setattr("builtins.input", lambda _: list_input)

    items = get_list_input("Enter List: ")

    assert items == ["test_1", "test_2"]

def test_get_list_input_invalid(monkeypatch, capsys):

    list_input = iter(["", "test_1, test_2"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    items = get_list_input("Enter List: ")
    captured = capsys.readouterr()

    assert "Please enter at least one valid item." in captured.out
    assert items == ["test_1", "test_2"]

def test_get_list_input_strip(monkeypatch):
    
    list_input = " test_1 , test_2 "

    monkeypatch.setattr("builtins.input", lambda _: list_input)

    items = get_list_input("Enter List: ")

    assert items == ["test_1", "test_2"]

def test_add_update_comment(monkeypatch):

    issue = {
        'issue_id': "ISSUE-999",
        'comments_updates': []
    }
    
    list_input = iter(["BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    add_update_comment(issue)

    assert len(issue["comments_updates"]) == 1

    assert issue["comments_updates"][-1]["author"] == "BR"
    assert issue["comments_updates"][-1]["comment"] == "Test"

def test_add_update_comment_append(monkeypatch):

    issue = {
        'issue_id': "ISSUE-999",
        'comments_updates': [{

            'date_time': '2026-10-12',
            'author': 'RB',
            'comment': 'comment'
            }]
        }
    
    list_input = iter(["BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    add_update_comment(issue)

    assert len(issue["comments_updates"]) == 2
    assert issue["comments_updates"][-2]["author"] == "RB"
    assert issue["comments_updates"][-2]["comment"] == "comment"
    assert issue["comments_updates"][-1]["author"] == "BR"
    assert issue["comments_updates"][-1]["comment"] == "Test"

def test_add_update_comment_date(monkeypatch):
    issue = {
        'issue_id': "ISSUE-999",
        'comments_updates': []
    }
    
    list_input = iter(["BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    add_update_comment(issue)

    assert len(issue["comments_updates"]) == 1
    # Take datetime from dictionary, in YYY-MM-DD:Time format, change to iso format, and check it equals today's date.
    assert datetime.fromisoformat(issue["comments_updates"][-1]["date_time"]).date() == date.today()

# Menu Functions
#
#

def test_show_menu(capsys):
    show_menu()

    captured = capsys.readouterr()

    assert(
    "Please select an option:\n"
    "1. Create a new issue\n"
    "2. View a single issue\n"
    "3. View all issues\n"
    "4. Search issues by keyword\n"
    "5. Filter by field\n"
    "6. View Overdue Issues\n"
    "7. Update Existing Issue\n"
    "8. Archive an Issue\n"
    "9. View Archived Issue\n"
    "10. Exit\n"
    ) in captured.out

def test_show_filter_menu(capsys):
    show_filter_menu()

    captured = capsys.readouterr()

    assert(
    "Please select an option to filter by:\n"
    "1. Status\n"
    "2. RAG\n"
    "3. Assignee\n"
    "4. Component\n"
    "5. Programme/s Affected\n"
    "6. Build/s Affected\n"
    "7. Back to main menu\n"
    ) in captured.out

def test_show_update_menu(capsys):
    show_update_menu()

    captured = capsys.readouterr()

    assert(
    "Please select a field to update:\n"
    "1. Status\n"
    "2. RAG\n"
    "3. Assignee\n"
    "4. Reporter/Champion\n"
    "5. Target Approval Date\n"
    "6. Target Completion Date\n"
    "7. Components\n"
    "8. Programmes Affected\n"
    "9. Build Affected\n"
    "10. Add Comment/Update\n"
    "11. Back to main menu\n"
    ) in captured.out


# Main Functions
#
#

def test_create_issue_id_gen(monkeypatch):
    # Input Dates - adjust dynamically
    today = date.today()
    approval_date = (today + timedelta(days=15)).isoformat()
    completion_date = (today + timedelta(days=25)).isoformat()
   
    tracker_data = {
    "next_issue_number": 999,
    "issues": []
    }

    list_input = iter([
    "Airbag Connector Clash",
    "Harness connector is offset 5mm from airbag connector",
    "Red",
    "EDS Engineer",
    "Airbag Manager",
    "Harness, Airbag, Seat",
    "PRG-1, PRG-2",
    "BUILD-1, BUILD-2",
    approval_date,
    completion_date,
    "EDS Engineer",
    "Issue raised and under investigation"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    create_issue(tracker_data)

    assert len(tracker_data["issues"]) == 1
    assert tracker_data["next_issue_number"] == 1000
    assert tracker_data["issues"][-1]["issue_id"] == "ISSUE-999"
    assert tracker_data["issues"][-1]["issue_title"] == "Airbag Connector Clash"

def test_create_issue_fields(monkeypatch):
    # Input Dates - adjust dynamically
    today = date.today()
    approval_date = (today + timedelta(days=15)).isoformat()
    completion_date = (today + timedelta(days=25)).isoformat()
    
    tracker_data = {
    "next_issue_number": 999,
    "issues": []
    }

    list_input = iter([
    "Airbag Connector Clash",
    "Harness connector is offset 5mm from airbag connector",
    "Red",
    "EDS Engineer",
    "Airbag Manager",
    "Harness, Airbag, Seat",
    "PRG-1, PRG-2",
    "BUILD-1, BUILD-2",
    approval_date,
    completion_date,
    "EDS Engineer",
    "Issue raised and under investigation"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    create_issue(tracker_data)

    assert tracker_data["issues"][-1]["issue_title"] == "Airbag Connector Clash"
    assert tracker_data["issues"][-1]["issue_description"] ==     "Harness connector is offset 5mm from airbag connector"
    assert tracker_data["issues"][-1]["issue_status"] == "Open"
    assert tracker_data["issues"][-1]["record_state"] == "Active"
    assert tracker_data["issues"][-1]["rag"] == "Red"
    assert tracker_data["issues"][-1]["assignee"] == "EDS Engineer" 
    assert tracker_data["issues"][-1]["reporter_champion"] == "Airbag Manager"
    assert tracker_data["issues"][-1]["components"] == ["Harness", "Airbag", "Seat"]
    assert tracker_data["issues"][-1]["programmes_affected"] == ["PRG-1", "PRG-2"]
    assert tracker_data["issues"][-1]["builds_affected"] == ["BUILD-1", "BUILD-2"]
    assert datetime.fromisoformat(tracker_data["issues"][-1]["date_raised"]).date() == date.today()
    assert tracker_data["issues"][-1]["target_approval_date"] == approval_date
    assert tracker_data["issues"][-1]["target_completion_date"] == completion_date
    assert tracker_data["issues"][-1]["comments_updates"][-1]["author"] == "EDS Engineer"
    assert tracker_data["issues"][-1]["comments_updates"][-1]["comment"] == "Issue raised and under investigation"

def test_create_issue_fields_invalid_rag(monkeypatch):
    # Input Dates - adjust dynamically
    today = date.today()
    approval_date = (today + timedelta(days=15)).isoformat()
    completion_date = (today + timedelta(days=25)).isoformat()
    
    tracker_data = {
    "next_issue_number": 999,
    "issues": []
    }

    list_input = iter([
    "Airbag Connector Clash",
    "Harness connector is offset 5mm from airbag connector",
    "Blue",
    "EDS Engineer",
    "Airbag Manager",
    "Harness, Airbag, Seat",
    "PRG-1, PRG-2",
    "BUILD-1, BUILD-2",
    approval_date,
    completion_date,
    "EDS Engineer",
    "Issue raised and under investigation"
    ])


    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    with pytest.raises(ValueError) as exc_info:
        create_issue(tracker_data)

    assert str(exc_info.value) == "Please enter a valid RAG status (Red, Amber, Green)."


def test_create_issue_fields_invalid_approval_before_today(monkeypatch):
    # Input Dates - adjust dynamically
    today = date.today()
    approval_date = (today - timedelta(days=1)).isoformat()
    completion_date = (today + timedelta(days=25)).isoformat()
    
    tracker_data = {
    "next_issue_number": 999,
    "issues": []
    }

    list_input = iter([
    "Airbag Connector Clash",
    "Harness connector is offset 5mm from airbag connector",
    "Red",
    "EDS Engineer",
    "Airbag Manager",
    "Harness, Airbag, Seat",
    "PRG-1, PRG-2",
    "BUILD-1, BUILD-2",
    approval_date,
    completion_date,
    "EDS Engineer",
    "Issue raised and under investigation"
    ])


    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    with pytest.raises(ValueError) as exc_info:
        create_issue(tracker_data)

    assert str(exc_info.value) == "Target approval date must be later than today."

def test_create_issue_fields_invalid_completion_before_today(monkeypatch):
    # Input Dates - adjust dynamically
    today = date.today()
    approval_date = (today + timedelta(days=1)).isoformat()
    completion_date = (today - timedelta(days=1)).isoformat()
    
    tracker_data = {
    "next_issue_number": 999,
    "issues": []
    }

    list_input = iter([
    "Airbag Connector Clash",
    "Harness connector is offset 5mm from airbag connector",
    "Red",
    "EDS Engineer",
    "Airbag Manager",
    "Harness, Airbag, Seat",
    "PRG-1, PRG-2",
    "BUILD-1, BUILD-2",
    approval_date,
    completion_date,
    "EDS Engineer",
    "Issue raised and under investigation"
    ])


    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    with pytest.raises(ValueError) as exc_info:
        create_issue(tracker_data)

    assert str(exc_info.value) == "Target completion date must be later than today."

def test_create_issue_fields_invalid_completion_before_approval(monkeypatch):
    # Input Dates - adjust dynamically
    today = date.today()
    approval_date = (today + timedelta(days=15)).isoformat()
    completion_date = (today + timedelta(days=14)).isoformat()
    
    tracker_data = {
    "next_issue_number": 999,
    "issues": []
    }

    list_input = iter([
    "Airbag Connector Clash",
    "Harness connector is offset 5mm from airbag connector",
    "Red",
    "EDS Engineer",
    "Airbag Manager",
    "Harness, Airbag, Seat",
    "PRG-1, PRG-2",
    "BUILD-1, BUILD-2",
    approval_date,
    completion_date,
    "EDS Engineer",
    "Issue raised and under investigation"
    ])


    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    with pytest.raises(ValueError) as exc_info:
        create_issue(tracker_data)

    assert str(exc_info.value) == "Target completion date must be equal to or later than target approval date."

def test_view_single_issue_valid(tracker_data, monkeypatch, capsys):
    list_input = iter(["ISSUE-998", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    view_single_issue(tracker_data)
    captured = capsys.readouterr()
    
    assert ("Issue ID: ISSUE-998\n"
            "Issue Title: Airbag Connector Clash\n"
            "Issue Description: Harness connector is offset 5mm from airbag connector\n"
            "Issue Status: Open\n"
            "RAG: Red\n"
            "Assignee: EDS Engineer\n"
            "Reporter/Champion: Airbag Manager\n"
            "Components: Harness, Airbag, Seat\n"
            "Programmes Affected: PRG-1, PRG-2\n"
            "Builds Affected: BUILD-1, BUILD-2\n"
            f"Date Raised: {date.today().isoformat()}\n"
            "Target Approval Date: 2026-09-30\n"
            "Target Completion Date: 2026-10-31\n\n"
            "Comments/Updates:\n\n"
            "Date/Time: 2026-09-29\n"
            "Author: EDS Engineer\n"
            "Comment: Issue raised and under investigation") in captured.out

def test_view_all_issues(tracker_data_long, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "")

    view_all_issues(tracker_data_long)
    captured = capsys.readouterr()

    assert(
        "Issue ID: ISSUE-996\n"
        "Issue Title: Test 1\n"
        "Issue Status: Open\n"
        "RAG: Red\n"
        "Assignee: Test 1\n"
    ) in captured.out

    assert(
        "Issue ID: ISSUE-997\n"
        "Issue Title: Test 2\n"
        "Issue Status: Open\n"
        "RAG: Red\n"
        "Assignee: Test 2\n"
    ) in captured.out

    assert(
        "Issue ID: ISSUE-998\n"
        "Issue Title: Test 3\n"
        "Issue Status: Open\n"
        "RAG: Red\n"
        "Assignee: Test 3\n"
    ) in captured.out

def test_search_issues_valid(tracker_data_long, monkeypatch, capsys):
    list_input = iter(["Test", ""])
    
    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    search_issues(tracker_data_long)
    captured = capsys.readouterr()

    assert(
        "Issue ID: ISSUE-996\n"
        "Issue Title: Test 1\n"
    ) in captured.out

    assert(
        "Issue ID: ISSUE-997\n"
        "Issue Title: Test 2\n"
    ) in captured.out

    assert(
        "Issue ID: ISSUE-998\n"
        "Issue Title: Test 3\n"
    ) in captured.out

def test_search_issues_invalid(tracker_data_long, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "long")
    search_issues(tracker_data_long)
    
    captured = capsys.readouterr()

    assert "Keyword search returned no issues." in captured.out

def test_filter_by_field_invalid_menu(tracker_data, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "15")
    filter_by_field(tracker_data)

    captured = capsys.readouterr()

    assert "Invalid Option" in captured.out

def test_filter_by_field_str_valid(tracker_data_long, monkeypatch, capsys):
    list_input = iter(["2", "Red", ""])
    
    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    filter_by_field(tracker_data_long)
    captured = capsys.readouterr()    

    assert "ISSUE-996: Test 1" in captured.out
    assert "ISSUE-997: Test 2" in captured.out
    assert "ISSUE-998: Test 3" in captured.out

def test_filter_by_field_str_invalid(tracker_data_long, monkeypatch, capsys):
    list_input = iter(["2", "Green", ""])
    
    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    filter_by_field(tracker_data_long)
    captured = capsys.readouterr()    

    assert "No issues found for this filter" in captured.out

def test_filter_by_field_list_valid(tracker_data_long, monkeypatch, capsys):
    list_input = iter(["5", "PRG-1", ""])
    
    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    filter_by_field(tracker_data_long)
    captured = capsys.readouterr()    

    assert "ISSUE-996: Test 1" in captured.out
    assert "ISSUE-997: Test 2" in captured.out
    assert "ISSUE-998: Test 3" in captured.out

def test_filter_by_field_list_invalid(tracker_data_long, monkeypatch, capsys):
    list_input = iter(["5", "PRG-100", ""])
    
    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    filter_by_field(tracker_data_long)
    captured = capsys.readouterr()    

    assert "No issues found for this filter" in captured.out

def test_view_overdue_issues_none(tracker_data, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "")
    view_overdue_issues(tracker_data)

    captured = capsys.readouterr()

    assert "No overdue issues" in captured.out

def test_view_overdue_issues_overdue(tracker_data_long, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "")
    view_overdue_issues(tracker_data_long)

    captured = capsys.readouterr()

    assert ("Issues with overdue approval dates:\n\n" 
            "ISSUE-996: Test 1\n\n"
            "ISSUE-997: Test 2\n\n") in captured.out

    assert ("Issues with overdue completion dates:\n\n" 
            "ISSUE-997: Test 2\n\n") in captured.out

def test_update_existing_issue_input(monkeypatch, capsys):
    tracker_data = {
        "next_issue_number": 1000,
        "issues": [
            {
            'issue_id': "ISSUE-998",
            'issue_title': "Airbag Connector Clash",
            'issue_description': "Harness connector is offset 5mm from airbag connector",
            'issue_status': "Open",
            'record_state': "Archived",
            'rag':"Red",
            'assignee': "EDS Engineer",
            'reporter_champion': "Airbag Manager",
            'components': ["Harness", "Airbag", "Seat"],
            'programmes_affected': ["PRG-1", "PRG-2"],
            'builds_affected': ["BUILD-1", "BUILD-2"],              
            'date_raised': date.today().isoformat(),
            'target_approval_date': "2026-09-30",
            'target_completion_date': "2026-10-31",
            'comments_updates': [{
                'author': "EDS Engineer",
                'comment': "Isuue raised and under investigation"
            }]
            },
            {
            'issue_id': "ISSUE-999",
            'issue_title': "Airbag Connector Clash",
            'issue_description': "Harness connector is offset 5mm from airbag connector",
            'issue_status': "Open",
            'record_state': "Active",
            'rag':"Red",
            'assignee': "EDS Engineer",
            'reporter_champion': "Airbag Manager",
            'components': ["Harness", "Airbag", "Seat"],
            'programmes_affected': ["PRG-1", "PRG-2"],
            'builds_affected': ["BUILD-1", "BUILD-2"],              
            'date_raised': date.today().isoformat(),
            'target_approval_date': "2026-09-30",
            'target_completion_date': "2026-10-31",
            'comments_updates': [{
                'author': "EDS Engineer",
                'comment': "Isuue raised and under investigation"
            }]
            }
        ]
    }

    list_input = iter(["ISSUE-997", "ISSUE-998", "ISSUE-999", "11"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    update_existing_issue(tracker_data)
    captured = capsys.readouterr()

    assert "Please enter a valid Issue ID." in captured.out
    assert "ISSUE-998 is archived and cannot be updated." in captured.out
    assert "Issue ID to update: ISSUE-999" in captured.out

def test_update_existing_issue_status(tracker_data, monkeypatch, capsys):
    list_input = iter(["ISSUE-998", "1", "test", "In Approval", "In Work", "BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    update_existing_issue(tracker_data)
    captured = capsys.readouterr()

    assert "Current status: Open" in captured.out
    assert "Please enter a valid issue status." in captured.out
    assert "Issue status must flow sequentially (Open <-> In Work <-> In Approval <-> Completed)." in captured.out
    assert "Issue status updated." in captured.out
    assert tracker_data["issues"][-1]["issue_status"] == "In Work" 
    assert len(tracker_data["issues"][-1]["comments_updates"]) == 2
    assert tracker_data["issues"][-1]["comments_updates"][-1]["author"] == "BR"
    assert tracker_data["issues"][-1]["comments_updates"][-1]["comment"] == "Test"


def test_update_existing_issue_rag(tracker_data, monkeypatch, capsys):
    list_input = iter(["ISSUE-998", "2", "blue", "Green", "Amber", "BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    update_existing_issue(tracker_data)
    captured = capsys.readouterr()

    assert "Current RAG: Red" in captured.out
    assert "Please enter a valid RAG status." in captured.out
    assert "RAG status must flow sequentially (Red <-> Amber <-> Green)." in captured.out
    assert "RAG status updated." in captured.out
    assert tracker_data["issues"][-1]["rag"] == "Amber" 
    assert len(tracker_data["issues"][-1]["comments_updates"]) == 2

def test_update_assignee(tracker_data, monkeypatch, capsys):
    list_input = iter(["ISSUE-998", "3", "", "Airbag Engineer", "BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    update_existing_issue(tracker_data)
    captured = capsys.readouterr()
    
    assert "Current assignee: EDS Engineer" in captured.out
    assert "Please enter a valid text string." in captured.out
    assert "Assignee updated." in captured.out
    assert tracker_data["issues"][-1]["assignee"] == "Airbag Engineer" 
    assert len(tracker_data["issues"][-1]["comments_updates"]) == 2

def test_update_reporter(tracker_data, monkeypatch, capsys):
    list_input = iter(["ISSUE-998", "4", "", "EDS Manager", "BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    update_existing_issue(tracker_data)
    captured = capsys.readouterr()
    
    assert "Current reporter/champion: Airbag Manager" in captured.out
    assert "Please enter a valid text string." in captured.out
    assert "Reporter/Champion updated." in captured.out
    assert tracker_data["issues"][-1]["reporter_champion"] == "EDS Manager" 
    assert len(tracker_data["issues"][-1]["comments_updates"]) == 2

def test_update_target_approval_date(monkeypatch, capsys):
    # Input Dates - adjust dynamically
    today = date.today()
    approval_date = (today + timedelta(days=15)).isoformat()
    completion_date = (today + timedelta(days=25)).isoformat()
    invalid_before_today = (today - timedelta(days=1)).isoformat()
    invalid_after_completion = (today + timedelta(days=30)).isoformat()
    new_approval_date = (today + timedelta(days=20)).isoformat()
    
    # Fake Issue
    tracker_data = {
        "next_issue_number": 999,
        "issues": [
            {
            'issue_id': "ISSUE-998",
            'issue_title': "Airbag Connector Clash",
            'issue_description': "Harness connector is offset 5mm from airbag connector",
            'issue_status': "Open",
            'record_state': "Active",
            'rag':"Red",
            'assignee': "EDS Engineer",
            'reporter_champion': "Airbag Manager",
            'components': ["Harness", "Airbag", "Seat"],
            'programmes_affected': ["PRG-1", "PRG-2"],
            'builds_affected': ["BUILD-1", "BUILD-2"],              
            'date_raised': today.isoformat(),
            'target_approval_date': approval_date,
            'target_completion_date': completion_date,
            'comments_updates': [{
                'author': "EDS Engineer",
                'comment': "Isuue raised and under investigation"
            }]
            }
        ]
    }
    
    list_input = iter(["ISSUE-998", "5", invalid_before_today, invalid_after_completion, new_approval_date, "BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    update_existing_issue(tracker_data)
    captured = capsys.readouterr()

    assert f"Current Target Approval Date: {approval_date}" in captured.out
    assert captured.out.count("Please enter a valid date (YYYY-MM-DD), which must be on or before the current target completion date or after today") == 2    
    assert tracker_data["issues"][-1]["target_approval_date"] == new_approval_date
    assert "Target approval date updated." in captured.out

def test_update_target_completion_date(monkeypatch, capsys):
    # Input Dates - adjust dynamically
    today = date.today()
    approval_date = (today + timedelta(days=15)).isoformat()
    completion_date = (today + timedelta(days=25)).isoformat()
    invalid_before_today = (today - timedelta(days=1)).isoformat()
    invalid_before_approval = (today + timedelta(days=14)).isoformat()
    new_completion_date = (today + timedelta(days=30)).isoformat()

    # Fake Issue
    tracker_data = {
        "next_issue_number": 999,
        "issues": [
            {
            'issue_id': "ISSUE-998",
            'issue_title': "Airbag Connector Clash",
            'issue_description': "Harness connector is offset 5mm from airbag connector",
            'issue_status': "Open",
            'record_state': "Active",
            'rag':"Red",
            'assignee': "EDS Engineer",
            'reporter_champion': "Airbag Manager",
            'components': ["Harness", "Airbag", "Seat"],
            'programmes_affected': ["PRG-1", "PRG-2"],
            'builds_affected': ["BUILD-1", "BUILD-2"],              
            'date_raised': today.isoformat(),
            'target_approval_date': approval_date,
            'target_completion_date': completion_date,
            'comments_updates': [{
                'author': "EDS Engineer",
                'comment': "Isuue raised and under investigation"
            }]
            }
        ]
    }

    # Test 
    list_input = iter(["ISSUE-998", "6", invalid_before_today, invalid_before_approval, new_completion_date, "BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    update_existing_issue(tracker_data)
    captured = capsys.readouterr()

    assert f"Current Target Completion Date: {completion_date}" in captured.out
    assert captured.out.count("Please enter a valid date (YYYY-MM-DD), which must be on or after the current target approval date or after today") == 2    
    assert tracker_data["issues"][-1]["target_completion_date"] == new_completion_date
    assert "Target completion date updated." in captured.out

def test_update_components(tracker_data, monkeypatch, capsys):
    list_input = iter(["ISSUE-998", "7", "", "Harness, Airbag", "BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    update_existing_issue(tracker_data)
    captured = capsys.readouterr()
    
    assert "Current components: Harness, Airbag, Seat" in captured.out
    assert "Please enter at least one valid item." in captured.out
    assert "Updated components." in captured.out
    assert tracker_data["issues"][-1]["components"] == ["Harness", "Airbag"] 
    assert len(tracker_data["issues"][-1]["comments_updates"]) == 2

def test_update_programmes_affected(tracker_data, monkeypatch, capsys):
    list_input = iter(["ISSUE-998", "8", "", "PRG-2, PRG-3", "BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    update_existing_issue(tracker_data)
    captured = capsys.readouterr()
    
    assert "Current programmes affected: PRG-1, PRG-2" in captured.out
    assert "Please enter at least one valid item." in captured.out
    assert "Updated programmes affected." in captured.out
    assert tracker_data["issues"][-1]["programmes_affected"] == ["PRG-2", "PRG-3"] 
    assert len(tracker_data["issues"][-1]["comments_updates"]) == 2

def test_update_builds_affected(tracker_data, monkeypatch, capsys):
    list_input = iter(["ISSUE-998", "9", "", "BUILD-2, BUILD-3", "BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    update_existing_issue(tracker_data)
    captured = capsys.readouterr()
    
    assert "Current builds affected: BUILD-1, BUILD-2" in captured.out
    assert "Please enter at least one valid item." in captured.out
    assert "Updated builds affected." in captured.out
    assert tracker_data["issues"][-1]["builds_affected"] == ["BUILD-2", "BUILD-3"] 
    assert len(tracker_data["issues"][-1]["comments_updates"]) == 2

def test_archive_issues_invalid_input(monkeypatch, capsys):
    # Fake Issue
    tracker_data = {
        "next_issue_number": 999,
        "issues": [
            {
            'issue_id': "ISSUE-997",
            'issue_title': "Airbag Connector Clash",
            'issue_description': "Harness connector is offset 5mm from airbag connector",
            'issue_status': "Open",
            'record_state': "Archived",
            'rag':"Red",
            'assignee': "EDS Engineer",
            'reporter_champion': "Airbag Manager",
            'components': ["Harness", "Airbag", "Seat"],
            'programmes_affected': ["PRG-1", "PRG-2"],
            'builds_affected': ["BUILD-1", "BUILD-2"],              
            'date_raised': date.today().isoformat(),
            'target_approval_date': "2026-09-30",
            'target_completion_date': "2026-10-31",
            'comments_updates': [{
                'author': "EDS Engineer",
                'comment': "Isuue raised and under investigation"
            }]
            },
            {
            'issue_id': "ISSUE-998",
            'issue_title': "Airbag Connector Clash",
            'issue_description': "Harness connector is offset 5mm from airbag connector",
            'issue_status': "Open",
            'record_state': "Active",
            'rag':"Red",
            'assignee': "EDS Engineer",
            'reporter_champion': "Airbag Manager",
            'components': ["Harness", "Airbag", "Seat"],
            'programmes_affected': ["PRG-1", "PRG-2"],
            'builds_affected': ["BUILD-1", "BUILD-2"],              
            'date_raised': date.today().isoformat(),
            'target_approval_date': "2026-09-30",
            'target_completion_date': "2026-10-31",
            'comments_updates': [{
                'author': "EDS Engineer",
                'comment': "Isuue raised and under investigation"
            }]
            }
        ]
    }

    list_input = iter(["ISSUE-999", "ISSUE-997", "SHOULD NOT BE IN DATA"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    archive_issues(tracker_data)
    captured = capsys.readouterr()

    assert "Issue ID ISSUE-999 not found." in captured.out
    assert "ISSUE-997 is already archived." in captured.out
    assert next(list_input) == "SHOULD NOT BE IN DATA"
    assert tracker_data["issues"][-2]["record_state"] == "Archived"

def test_archive_issues_valid_no_confirm(tracker_data, monkeypatch, capsys):
    list_input = iter(["ISSUE-998", "abc", "SHOULD NOT BE IN DATA"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    archive_issues(tracker_data)
    captured = capsys.readouterr()

    assert "Current record state: Active" in captured.out
    assert next(list_input) == "SHOULD NOT BE IN DATA"
    assert tracker_data["issues"][-1]["record_state"] == "Active"

def test_archive_issue_valid_confirm(tracker_data, monkeypatch, capsys):
    list_input = iter(["ISSUE-998", "confirm", "BR", "Test"])

    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    archive_issues(tracker_data)
    captured = capsys.readouterr()

    assert "Current record state: Active" in captured.out
    assert "ISSUE-998 is now archived." in captured.out
    assert tracker_data["issues"][-1]["record_state"] == "Archived"
    assert len(tracker_data["issues"][-1]["comments_updates"]) == 2

def test_view_archived_issues(monkeypatch, capsys):
    # Fake Issue
    tracker_data = {
        "next_issue_number": 999,
        "issues": [
            {
            'issue_id': "ISSUE-997",
            'issue_title': "Airbag Connector Clash",
            'issue_description': "Harness connector is offset 5mm from airbag connector",
            'issue_status': "Open",
            'record_state': "Archived",
            'rag':"Red",
            'assignee': "EDS Engineer",
            'reporter_champion': "Airbag Manager",
            'components': ["Harness", "Airbag", "Seat"],
            'programmes_affected': ["PRG-1", "PRG-2"],
            'builds_affected': ["BUILD-1", "BUILD-2"],              
            'date_raised': date.today().isoformat(),
            'target_approval_date': "2026-09-30",
            'target_completion_date': "2026-10-31",
            'comments_updates': [{
                'author': "EDS Engineer",
                'comment': "Isuue raised and under investigation"
            }]
            },
            {
            'issue_id': "ISSUE-998",
            'issue_title': "Airbag Connector Clashes",
            'issue_description': "Harness connector is offset 5mm from airbag connector",
            'issue_status': "Open",
            'record_state': "Archived",
            'rag':"Amber",
            'assignee': "EDS Engineers",
            'reporter_champion': "Airbag Manager",
            'components': ["Harness", "Airbag", "Seat"],
            'programmes_affected': ["PRG-1", "PRG-2"],
            'builds_affected': ["BUILD-1", "BUILD-2"],              
            'date_raised': date.today().isoformat(),
            'target_approval_date': "2026-09-30",
            'target_completion_date': "2026-10-31",
            'comments_updates': [{
                'author': "EDS Engineer",
                'comment': "Isuue raised and under investigation"
            }]
            }
        ]
    }
    monkeypatch.setattr("builtins.input", lambda _: "")
    view_archived_issues(tracker_data)

    captured = capsys.readouterr()

    assert ("Issue ID: ISSUE-997\n"
            "Issue Title: Airbag Connector Clash\n"
            "Issue Status: Open\n"
            "RAG: Red\n"
            "Assignee: EDS Engineer\n") in captured.out

    assert ("Issue ID: ISSUE-998\n"
            "Issue Title: Airbag Connector Clashes\n"
            "Issue Status: Open\n"
            "RAG: Amber\n"
            "Assignee: EDS Engineers\n") in captured.out

def test_view_archived_issues_no_issues(tracker_data, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "")
    view_archived_issues(tracker_data)
    
    captured = capsys.readouterr()

    assert "No archived issues found." in captured.out