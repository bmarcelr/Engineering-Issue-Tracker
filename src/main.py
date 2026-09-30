from issues import (
    create_issue,
    view_all_issues,
    view_single_issue,
    search_issues,
    show_menu,
    filter_by_field,
    view_overdue_issues,
    update_existing_issue,
    archive_issues,
    view_archived_issues
)

from storage import (
    load_data,
    save_data
)

menu_option ={
    "1": create_issue,
    "2": view_single_issue,
    "3": view_all_issues,
    "4": search_issues,
    "5": filter_by_field,
    "6": view_overdue_issues,
    "7": update_existing_issue,
    "8": archive_issues,
    "9": view_archived_issues
    
}

def main ():

    tracker_data = load_data()

    while True:
        show_menu()
        # Input Area
        choice = input("Choose an Option: ")

        # Input Selection and Conversion
        if choice in menu_option:
            menu_option[choice](tracker_data)

            if choice in ["1", "7", "8"]:
                print("Saving data...")
                save_data(tracker_data)

        elif choice == "10":
            print("Goodbye!")
            break

        else:
            print("Invalid Option")

if __name__ == "__main__":
    main()
