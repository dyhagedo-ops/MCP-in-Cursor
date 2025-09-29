import os
import sqlite3
from typing import List, Optional, Dict, Any, Tuple


class EmployeeDAL:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._ensure_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _ensure_db(self) -> None:
        schema_path = os.path.join(os.path.dirname(__file__), "mcp.sql")
        with open(schema_path, "r") as f:
            schema_sql = f.read()

        with self._connect() as conn:
            # Ensure DB exists and attempt to create tables if missing
            conn.executescript(schema_sql)

            # Validate employees table has expected columns; rebuild if legacy schema found
            cur = conn.execute("PRAGMA table_info(employees);")
            existing_cols = [row[1] for row in cur.fetchall()]
            expected_cols = {
                "id",
                "first_name",
                "last_name",
                "email",
                "phone",
                "hire_date",
                "salary",
                "department",
            }
            if existing_cols and not expected_cols.issubset(set(existing_cols)):
                # Legacy or conflicting schema; drop and recreate cleanly in one transaction
                conn.executescript(
                    """
                    BEGIN;
                    DROP TABLE IF EXISTS employees;
                    COMMIT;
                    """
                )
                conn.executescript(schema_sql)

    def list_employees(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                """
                SELECT id, first_name, last_name, email, phone, hire_date, salary, department
                FROM employees
                ORDER BY id
                """
            )
            return [dict(row) for row in cur.fetchall()]

    def get_employee(self, employee_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                """
                SELECT id, first_name, last_name, email, phone, hire_date, salary, department
                FROM employees
                WHERE id = ?
                """,
                (employee_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def get_employee_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                """
                SELECT id, first_name, last_name, email, phone, hire_date, salary, department
                FROM employees
                WHERE email = ?
                """,
                (email,),
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def create_employee(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str],
        hire_date: str,
        salary: float,
        department: Optional[str],
    ) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO employees (first_name, last_name, email, phone, hire_date, salary, department)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (first_name, last_name, email, phone, hire_date, salary, department),
            )
            return cur.lastrowid

    def update_employee(
        self,
        employee_id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str],
        hire_date: str,
        salary: float,
        department: Optional[str],
    ) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                """
                UPDATE employees
                SET first_name = ?, last_name = ?, email = ?, phone = ?, hire_date = ?, salary = ?, department = ?
                WHERE id = ?
                """,
                (first_name, last_name, email, phone, hire_date, salary, department, employee_id),
            )
            return cur.rowcount > 0

    def delete_employee(self, employee_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            return cur.rowcount > 0


