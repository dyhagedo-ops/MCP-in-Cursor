from dal import EmployeeDAL


def main() -> None:
    dal = EmployeeDAL("employees.db")

    # Create
    emp_id = dal.create_employee(
        first_name="Test",
        last_name="User",
        email="test.user@example.com",
        phone=None,
        hire_date="2025-09-26",
        salary=70000.0,
        department="QA",
    )
    print(f"Created: {emp_id}")

    # List
    employees = dal.list_employees()
    print(f"List count after create: {len(employees)}")

    # Update
    updated = dal.update_employee(
        emp_id,
        first_name="Testy",
        last_name="User",
        email="test.user@example.com",
        phone="555-9999",
        hire_date="2025-09-26",
        salary=75000.0,
        department="QA",
    )
    print(f"Updated: {updated}")

    # Get
    got = dal.get_employee(emp_id)
    print(f"Got: {got['first_name']} {got['last_name']} ${got['salary']}")

    # Delete
    deleted = dal.delete_employee(emp_id)
    print(f"Deleted: {deleted}")


if __name__ == "__main__":
    main()


