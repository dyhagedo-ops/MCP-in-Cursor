from typing import Optional, Iterable, Dict, Any, Tuple


def prompt_text(prompt_text: str) -> str:
    return input(prompt_text).strip()


def prompt_float(prompt_text: str) -> float:
    while True:
        try:
            return float(prompt_text_and_get(prompt_text))
        except ValueError:
            print("Please enter a valid number.")


def prompt_optional(prompt_text: str) -> Optional[str]:
    value = prompt_text_and_get(prompt_text)
    return value if value else None


def prompt_text_and_get(prompt_text: str) -> str:
    return input(prompt_text).strip()


def show_message(message: str) -> None:
    print(message)


def show_employees(employees: Iterable[Dict[str, Any]]) -> None:
    employees = list(employees)
    if not employees:
        print("No employees found.")
        return
    print("\nEmployees:")
    for e in employees:
        print(
            f"[{e['id']}] {e['first_name']} {e['last_name']} | {e['email']} | "
            f"{e.get('phone') or ''} | {e['hire_date']} | ${float(e['salary']):.2f} | {e.get('department') or ''}"
        )


def show_menu(title: str, actions: Iterable[Tuple[str, str]]) -> None:
    print(f"\n{title}")
    for key, label in actions:
        print(f"{key}. {label}")


def get_menu_choice(prompt_label: str = "Choose an option: ") -> str:
    return input(prompt_label).strip()



