from dal import EmployeeDAL
from controllers import (
    list_employees_controller,
    add_employee_controller,
    update_employee_controller,
    delete_employee_controller,
)
import views as view


def main() -> None:
    dal = EmployeeDAL("employees.db")
    actions = {
        "1": ("View employees", list_employees_controller),
        "2": ("Add employee", add_employee_controller),
        "3": ("Update employee", update_employee_controller),
        "4": ("Delete employee", delete_employee_controller),
        "5": ("Exit", None),
    }
    while True:
        view.show_menu("Employee Manager", ((k, v[0]) for k, v in actions.items()))
        choice = view.get_menu_choice()
        if choice == "5":
            view.show_message("Goodbye!")
            break
        action = actions.get(choice)
        if not action:
            view.show_message("Invalid choice.")
            continue
        _, func = action
        func(dal)


if __name__ == "__main__":
    main()


