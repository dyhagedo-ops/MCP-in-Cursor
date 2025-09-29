from typing import Optional

from dal import EmployeeDAL
import views as view


def list_employees_controller(dal: EmployeeDAL) -> None:
    employees = dal.list_employees()
    view.show_employees(employees)


def add_employee_controller(dal: EmployeeDAL) -> None:
    view.show_message("\nAdd Employee")
    first_name = view.prompt_text("First name: ")
    last_name = view.prompt_text("Last name: ")
    email = view.prompt_text("Email: ")
    phone = view.prompt_optional("Phone (optional): ")
    hire_date = view.prompt_text("Hire date (YYYY-MM-DD): ")
    salary = view.prompt_float("Salary: ")
    department = view.prompt_optional("Department (optional): ")

    employee_id = dal.create_employee(
        first_name, last_name, email, phone, hire_date, salary, department
    )
    created = dal.get_employee(employee_id)
    if created:
        view.show_message(
            f"Created employee: [{created['id']}] {created['first_name']} {created['last_name']} | "
            f"{created['email']} | {created.get('phone') or ''} | {created['hire_date']} | "
            f"${float(created['salary']):.2f} | {created.get('department') or ''}"
        )
    else:
        view.show_message(f"Created employee with id {employee_id}.")


def update_employee_controller(dal: EmployeeDAL) -> None:
    view.show_message("\nUpdate Employee")
    ident = view.prompt_text("Employee id or email: ")
    if ident.isdigit():
        existing = dal.get_employee(int(ident))
    else:
        existing = dal.get_employee_by_email(ident)
    if not existing:
        view.show_message("Employee not found.")
        return

    view.show_message("Leave blank to keep current value.")
    first_name = view.prompt_optional(f"First name [{existing['first_name']}]: ") or existing['first_name']
    last_name = view.prompt_optional(f"Last name [{existing['last_name']}]: ") or existing['last_name']
    email = view.prompt_optional(f"Email [{existing['email']}]: ") or existing['email']
    phone = view.prompt_optional(f"Phone [{existing.get('phone') or ''}]: ")
    if phone is None:
        phone = existing.get('phone')
    hire_date = view.prompt_optional(f"Hire date [{existing['hire_date']}]: ") or existing['hire_date']
    salary_input = view.prompt_optional(f"Salary [{existing['salary']}]: ")
    salary = float(salary_input) if salary_input is not None else float(existing['salary'])
    department = view.prompt_optional(f"Department [{existing.get('department') or ''}]: ")
    if department is None:
        department = existing.get('department')

    updated = dal.update_employee(
        existing['id'],
        first_name,
        last_name,
        email,
        phone,
        hire_date,
        salary,
        department,
    )
    view.show_message("Updated." if updated else "No changes applied.")


def delete_employee_controller(dal: EmployeeDAL) -> None:
    view.show_message("\nDelete Employee")
    ident = view.prompt_text("Employee id: ")
    try:
        employee_id = int(ident)
    except ValueError:
        view.show_message("Invalid id.")
        return
    deleted = dal.delete_employee(employee_id)
    view.show_message("Deleted." if deleted else "Employee not found.")



