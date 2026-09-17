"""Removes rows left behind by test scripts (Persona/TEST data). Safe to run any time."""
import sqlite3, pathlib
db = pathlib.Path(__file__).resolve().parent.parent / "data" / "etc-labs.sqlite3"
con = sqlite3.connect(db)
n = con.execute("DELETE FROM project_requests WHERE name IN ('Persona Client') OR name LIKE 'TEST %'").rowcount
n += con.execute("DELETE FROM applications WHERE first_name = 'TEST'").rowcount
n += con.execute("DELETE FROM contributions WHERE note = 'TEST contribution'").rowcount
con.commit(); print("removed", n, "test rows")
