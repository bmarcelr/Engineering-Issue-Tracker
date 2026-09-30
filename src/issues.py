from datetime import date
from datetime import datetime

# User Inputs

def get_text_input(prompt):
    while True:
        text = input(prompt).strip()

        if text:
            return text

        print("Please enter a valid text string.")

def get_date_input(prompt):
    while True:
        try:
            user_input = input(prompt)
            return datetime.strptime(user_input, "%Y-%m-%d").date()
            
        except ValueError:
            print("Please enter dates in YYYY-MM-DD format.")
    
def get_list_input(prompt):
    while True:
        user_input = input(prompt)

        items = [item.strip() for item in user_input.split(",") if item.strip()]

        if items == []:
            print("Please enter at least one valid item.")
            continue

        return items

def add_update_comment(issue):
    comment_author = get_text_input("Please input comment author: ")
    comment_text = get_text_input("Please input comment text: ")

    comments_updates = {
            'date_time': datetime.now().isoformat(),
            'author': comment_author,
            'comment': comment_text
        }

    issue["comments_updates"].append(comments_updates)

def pause():
    input("\nPress Enter to return to the main menu...")

# Menu Options

def show_menu():
    print("Please select an option:")
    print("1. Create a new issue")
    print("2. View a single issue")
    print("3. View all issues")
    print("4. Search issues by keyword")
    print("5. Filter by field")
    print("6. View Overdue Issues")
    print("7. Update Existing Issue")
    print("8. Archive an Issue")
    print("9. View Archived Issue")
    print("10. Exit")

def show_filter_menu():
    print("Please select an option to filter by:")
    print("1. Status")
    print("2. RAG")
    print("3. Assignee")
    print("4. Component")
    print("5. Programme/s Affected")
    print("6. Build/s Affected")
    print("7. Back to main menu")

def show_update_menu():
    print("Please select a field to update:")
    print("1. Status")
    print("2. RAG")
    print("3. Assignee")
    print("4. Reporter/Champion")
    print("5. Target Approval Date")
    print("6. Target Completion Date")
    print("7. Components")
    print("8. Programmes Affected")
    print("9. Build Affected")
    print("10. Add Comment/Update")
    print("11. Back to main menu")

def create_issue(tracker_data):
    issue_title = get_text_input("Please input Issue Title: ")
    issue_description = get_text_input("Please input Issue Description: ")
    rag = get_text_input("Please input RAG status (Red, Amber, Green): ")
    assignee = get_text_input("Please input Assignee name: ")
    reporter_champion = get_text_input("Please input Reporter/Champion name: ")
    components = get_list_input("Please enter components affected: ")
    programmes_affected = get_list_input("Please enter programmes affected: ")
    builds_affected = get_list_input("Please enter builds affected: ")
    target_approval_date = get_date_input("Please input Target Approval Date (YYYY-MM-DD): ")
    target_completion_date = get_date_input("Please input Target Completion Date (YYYY-MM-DD): ")
    comment_author = get_text_input("Please input comment author: ")
    comment_text = get_text_input("Please input comment text: ")

    comments_updates = [
        {
            'date_time': datetime.now().isoformat(),
            'author': comment_author,
            'comment': comment_text
        }
    ]
    rag = rag.strip().capitalize()

    allowed_rag = ["Red", "Amber", "Green"]

    if rag not in allowed_rag:
        raise ValueError("Please enter a valid RAG status (Red, Amber, Green).")

    if target_approval_date <= date.today():
        raise ValueError("Target approval date must be later than today.")

    if target_completion_date <= date.today():
        raise ValueError("Target completion date must be later than today.")
    
    if target_approval_date > target_completion_date:
        raise ValueError("Target completion date must be equal to or later than target approval date.")

    # Issue ID Creation

    issue_number = (tracker_data["next_issue_number"])

    issue_id = f"ISSUE-{issue_number:03d}"

    # Dictionary loading
    issue = {
        'issue_id': issue_id,
        'issue_title': issue_title,
        'issue_description': issue_description,
        'issue_status': "Open",
        'record_state': "Active",
        'rag': rag,
        'assignee': assignee,
        'reporter_champion': reporter_champion,
        'components': components,
        'programmes_affected': programmes_affected,
        'builds_affected': builds_affected,              
        'date_raised': date.today().isoformat(),
        'target_approval_date': target_approval_date.isoformat(),
        'target_completion_date': target_completion_date.isoformat(),
        'comments_updates': comments_updates,
    }

    # Now update json values and write back to json
    tracker_data["issues"].append(issue)
    tracker_data["next_issue_number"] += 1 

    return issue
    

def view_single_issue(tracker_data):
    issue_id = get_text_input("Please enter Issue ID (ISSUE-XXX): ")

    found = False

    for issue in tracker_data["issues"]:
        if issue["issue_id"] == issue_id:
            print(
                f"Issue ID: {issue["issue_id"]}\n"
                f"Issue Title: {issue["issue_title"]}\n"
                f"Issue Description: {issue["issue_description"]}\n"
                f"Issue Status: {issue["issue_status"]}\n"
                f"RAG: {issue["rag"]}\n"
                f"Assignee: {issue["assignee"]}\n"
                f"Reporter/Champion: {issue["reporter_champion"]}\n"
                f"Components: {', '.join(issue["components"])}\n"
                f"Programmes Affected: {', '.join(issue["programmes_affected"])}\n"
                f"Builds Affected: {', '.join(issue["builds_affected"])}\n"
                f"Date Raised: {issue["date_raised"]}\n"
                f"Target Approval Date: {issue["target_approval_date"]}\n"
                f"Target Completion Date: {issue["target_completion_date"]}\n"
                )

            print(f"Comments/Updates:\n")
            for comment_update in issue["comments_updates"]:
                 print(
                    f"Date/Time: {comment_update["date_time"]}\n"
                    f"Author: {comment_update["author"]}\n"
                    f"Comment: {comment_update["comment"]}\n"
                 )
            found = True
            break
    pause()

    if not found:
        print(f"Issue ID {issue_id} not found.")

def view_all_issues(tracker_data):
    for issue in tracker_data["issues"]:
        print(
            f"Issue ID: {issue["issue_id"]}\n"
            f"Issue Title: {issue["issue_title"]}\n"
            f"Issue Status: {issue["issue_status"]}\n"
            f"RAG: {issue["rag"]}\n"
            f"Assignee: {issue["assignee"]}\n"
            f"\n"
        )
    pause()

def search_issues(tracker_data):
    keyword = get_text_input("Please enter keyword: ").lower()

    found = False

    for issue in tracker_data["issues"]:

        if keyword in issue["issue_title"].lower() or keyword in issue["issue_description"].lower():
            print(
                f"Issue ID: {issue["issue_id"]}\n"
                f"Issue Title: {issue["issue_title"]}\n"
            )

            found = True
    pause()

    if not found:
        print("Keyword search returned no issues.")

def filter_by_field(tracker_data):

    found = False

    show_filter_menu()

    filter_menu = {
        "1": "issue_status",
        "2": "rag",
        "3": "assignee",
        "4": "components",
        "5": "programmes_affected",
        "6": "builds_affected",
        }

    choice = input("Choose an Option: ")

    if choice in filter_menu:
        selected_field = filter_menu[choice]
        sub_filter_value = get_text_input("Enter filter value: ").lower()

        for issue in tracker_data["issues"]:

            if isinstance(issue[selected_field], str):

                if issue[selected_field].lower() == sub_filter_value:

                    print(f"{issue["issue_id"]}: {issue["issue_title"]}")

                    found = True
                
            elif isinstance(issue[selected_field], list):

                if sub_filter_value in [item.lower() for item in issue[selected_field]]:
            
                    print(f"{issue["issue_id"]}: {issue["issue_title"]}")


                    found = True

        if not found:
            print("No issues found for this filter.")
            return
        pause()

    elif choice == "7":
        return

    else:
        print("Invalid Option")

def view_overdue_issues(tracker_data):

    overdue_approval = []
    overdue_completion = []

    for issue in tracker_data["issues"]:
        target_approval_date = datetime.strptime(issue["target_approval_date"], "%Y-%m-%d").date()
        target_completion_date = datetime.strptime(issue["target_completion_date"], "%Y-%m-%d").date()

        if target_approval_date < date.today():
            overdue_approval.append(issue)

        if target_completion_date < date.today():
            overdue_completion.append(issue)

    if overdue_approval:
        print("Issues with overdue approval dates:\n")

        for issue in overdue_approval:
            print(f"{issue["issue_id"]}: {issue["issue_title"]}\n")

    if overdue_completion:
        print("Issues with overdue completion dates:\n")

        for issue in overdue_completion:
            print(f"{issue["issue_id"]}: {issue["issue_title"]}\n")

    if not overdue_approval and not overdue_completion:
        print("No overdue issues.")
        return

def update_existing_issue(tracker_data):
    
    while True:
        issue_id = get_text_input("Please enter Issue ID (ISSUE-XXX): ")

        found_issue = None
        
        for issue in tracker_data["issues"]:
             if issue["issue_id"] == issue_id:
                found_issue = issue
                break    
        
        if found_issue is None:
            print("Please enter a valid Issue ID.")
            continue            
       
        if found_issue["record_state"] == "Archived":
            print(f"{issue_id} is archived and cannot be updated.")
            continue

        issue = found_issue
        print(f"Issue ID to update: {issue["issue_id"]}\n")

        break
              

    update_menu = {
        "1": "issue_status",
        "2": "rag",
        "3": "assignee",
        "4": "reporter_champion",
        "5": "target_approval_date",
        "6": "target_completion_date",
        "7": "components",
        "8": "programmes_affected",
        "9": "builds_affected",
        "10": "comments_updates"
        }

    show_update_menu()

    choice = input("Choose an Option: ")

    if choice == "11":
        return
    
    elif choice not in update_menu:
        print("Invalid option.")
        return

# Update Issue Status
    elif update_menu[choice] == "issue_status":
        current_status = issue["issue_status"]

        print(f"Current status: {current_status}")

        status_order = ["Open", "In Work", "In Approval", "Completed"]

        while True:
            update_status = get_text_input("Enter new issue status: ").title()

            if update_status not in status_order:
                print("Please enter a valid issue status.")
                continue
        
            current_index = status_order.index(current_status)

            update_index = status_order.index(update_status)

            if abs(update_index - current_index) == 1:

                issue["issue_status"] = update_status
                break

            else:
                print("Issue status must flow sequentially (Open <-> In Work <-> In Approval <-> Completed).")
                continue

        add_update_comment(issue)

        print("Issue status updated.")
        return

# Update RAG Status
    elif update_menu[choice] == "rag":
        current_rag = issue["rag"]

        print(f"Current RAG: {current_rag}")

        rag_order = ["Red", "Amber", "Green"]

        while True:
            update_rag = get_text_input("Enter new RAG status: ").capitalize()

            if update_rag not in rag_order:
                print("Please enter a valid RAG status.")
                continue
        
            current_index = rag_order.index(current_rag)

            update_index = rag_order.index(update_rag)

            if abs(update_index - current_index) == 1:

                issue["rag"] = update_rag
                break

            else:
                print("RAG status must flow sequentially (Red <-> Amber <-> Green).")
                continue

        add_update_comment(issue)

        print("RAG status updated.")
        return

# Update Assignee
    elif update_menu[choice] == "assignee":
        current_assignee = issue["assignee"]

        print(f"Current assignee: {current_assignee}")
        
        update_assignee = get_text_input("Enter new assignee: ")
        issue["assignee"] = update_assignee

        add_update_comment(issue)


        print("Assignee updated.")
        return

# Update Reporter
    elif update_menu[choice] == "reporter_champion":
        current_reporter_champion = issue["reporter_champion"]

        print(f"Current reporter/champion: {current_reporter_champion}")

        update_reporter_champion = get_text_input("Enter new reporter/champion: ")
        issue["reporter_champion"] = update_reporter_champion

        add_update_comment(issue)

        print("Reporter/Champion updated.")
        return

# Update Target Approval Date
    elif update_menu[choice] == "target_approval_date":

        current_approval_date = datetime.strptime(issue["target_approval_date"], "%Y-%m-%d").date()

        print(f"Current Target Approval Date: {current_approval_date}")

        while True:
            update_approval_date = get_date_input("Enter new target approval date (YYYY-MM-DD): ")

            if update_approval_date > datetime.strptime(issue["target_completion_date"], "%Y-%m-%d").date() or update_approval_date <= date.today():
                print("Please enter a valid date (YYYY-MM-DD), which must be on or before the current target completion date or after today")
                continue

            issue["target_approval_date"] = update_approval_date.isoformat()
            break

        add_update_comment(issue)

        print("Target approval date updated.")
        return

# Update Target Completion Date

    elif update_menu[choice] == "target_completion_date":
        current_completion_date = datetime.strptime(issue["target_completion_date"], "%Y-%m-%d").date()

        print(f"Current Target Completion Date: {current_completion_date}")

        while True:
            update_completion_date = get_date_input("Enter new target completion date (YYYY-MM-DD): ")

            if update_completion_date < datetime.strptime(issue["target_approval_date"], "%Y-%m-%d").date() or update_completion_date <= date.today():
                print("Please enter a valid date (YYYY-MM-DD), which must be on or after the current target approval date or after today")
                continue

            issue["target_completion_date"] = update_completion_date.isoformat()
            break

        add_update_comment(issue)

        print("Target completion date updated.")
        return

# Update Components
    elif update_menu[choice] == "components":
        current_components = issue["components"]

        print(f"Current components: {', '.join(current_components)}")

        update_components = get_list_input("Enter new components: ")
        
        issue["components"] = update_components
      
        add_update_comment(issue)

        print("Updated components.")
        return

# Update Programmes Affected
    elif update_menu[choice] == "programmes_affected":
        current_programme = issue["programmes_affected"]

        print(f"Current programmes affected: {', '.join(current_programme)}")
        
        update_programmes_affected = get_list_input("Enter new programmes affected: ")
        
        issue["programmes_affected"] = update_programmes_affected
        
        add_update_comment(issue)

        print("Updated programmes affected.")
        return

# Update Builds Affected
    elif update_menu[choice] == "builds_affected":
        current_build = issue["builds_affected"]

        print(f"Current builds affected: {', '.join(current_build)}")

        update_builds_affected = get_list_input("Enter new builds affected: ")
        
        issue["builds_affected"] = update_builds_affected
        
        add_update_comment(issue)

        print("Updated builds affected.")
        return
        

# Add New Comment/Update
    elif update_menu[choice] == "comments_updates":
        add_update_comment(issue)

        print("Comment/update added.")
        return

def archive_issues(tracker_data):

    while True:
        issue_id = get_text_input("Please enter Issue ID (ISSUE-XXX): ")

        found_issue = None

        for issue in tracker_data["issues"]:
            if issue["issue_id"] == issue_id:
                found_issue = issue
                break

        if found_issue is None:
            print(f"Issue ID {issue_id} not found.")
            continue

        if found_issue["record_state"] == "Archived":
            print(f"{issue_id} is already archived.")
            return

        issue = found_issue
        break

    current_record_state = issue["record_state"]
    print(f"Current record state: {current_record_state}")

    approval = get_text_input("Please enter 'confirm' to archive issue: ")

    if approval.lower() != "confirm":
        return

    issue["record_state"] = "Archived"

    add_update_comment(issue)

    print(f"{issue_id} is now archived.")

def view_archived_issues(tracker_data):
    
    found = False
    
    for issue in tracker_data["issues"]:
        if issue["record_state"] == "Archived":
            found = True
            print(
                f"Issue ID: {issue["issue_id"]}\n"
                f"Issue Title: {issue["issue_title"]}\n"
                f"Issue Status: {issue["issue_status"]}\n"
                f"RAG: {issue["rag"]}\n"
                f"Assignee: {issue["assignee"]}\n"
                f"\n"
            )
    if not found:
        print("No archived issues found.")

    pause()