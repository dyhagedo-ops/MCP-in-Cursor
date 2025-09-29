PRAGMA foreign_keys = ON;

BEGIN;

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    hire_date TEXT NOT NULL,
    salary REAL NOT NULL CHECK (salary >= 0),
    department TEXT
);

-- Non-breaking guardrails: audit trail for INSERT/UPDATE/DELETE on employees
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('INSERT','UPDATE','DELETE')),
    row_id INTEGER NOT NULL,
    changed_at TEXT NOT NULL DEFAULT (datetime('now')),
    old_values TEXT,
    new_values TEXT
);

-- Record INSERTs on employees
CREATE TRIGGER IF NOT EXISTS employees_ai
AFTER INSERT ON employees
BEGIN
    INSERT INTO audit_log(table_name, action, row_id, new_values)
    VALUES(
        'employees',
        'INSERT',
        NEW.id,
        'first_name=' || NEW.first_name ||
        ';last_name=' || NEW.last_name ||
        ';email=' || NEW.email ||
        ';phone=' || IFNULL(NEW.phone, '') ||
        ';hire_date=' || NEW.hire_date ||
        ';salary=' || NEW.salary ||
        ';department=' || IFNULL(NEW.department, '')
    );
END;

-- Record UPDATEs on employees
CREATE TRIGGER IF NOT EXISTS employees_au
AFTER UPDATE ON employees
BEGIN
    INSERT INTO audit_log(table_name, action, row_id, old_values, new_values)
    VALUES(
        'employees',
        'UPDATE',
        NEW.id,
        'first_name=' || OLD.first_name ||
        ';last_name=' || OLD.last_name ||
        ';email=' || OLD.email ||
        ';phone=' || IFNULL(OLD.phone, '') ||
        ';hire_date=' || OLD.hire_date ||
        ';salary=' || OLD.salary ||
        ';department=' || IFNULL(OLD.department, ''),
        'first_name=' || NEW.first_name ||
        ';last_name=' || NEW.last_name ||
        ';email=' || NEW.email ||
        ';phone=' || IFNULL(NEW.phone, '') ||
        ';hire_date=' || NEW.hire_date ||
        ';salary=' || NEW.salary ||
        ';department=' || IFNULL(NEW.department, '')
    );
END;

-- Record DELETEs on employees
CREATE TRIGGER IF NOT EXISTS employees_ad
AFTER DELETE ON employees
BEGIN
    INSERT INTO audit_log(table_name, action, row_id, old_values)
    VALUES(
        'employees',
        'DELETE',
        OLD.id,
        'first_name=' || OLD.first_name ||
        ';last_name=' || OLD.last_name ||
        ';email=' || OLD.email ||
        ';phone=' || IFNULL(OLD.phone, '') ||
        ';hire_date=' || OLD.hire_date ||
        ';salary=' || OLD.salary ||
        ';department=' || IFNULL(OLD.department, '')
    );
END;

COMMIT;


