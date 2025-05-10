import sqlite3

# TODO: Where should the database file be located?

DB_NAME = "llm.db"
DB_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS Student (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        credits INTEGER
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Professor (
        professor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        password TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Administrator (
        administrator_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        password TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Class (
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        course_name TEXT,
        professor INTEGER,
        FOREIGN KEY (professor) REFERENCES Professor(professor_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Student_Class (
        student_id INTEGER,
        class_id INTEGER,
        PRIMARY KEY (student_id, class_id),
        FOREIGN KEY (student_id) REFERENCES Student(student_id),
        FOREIGN KEY (class_id) REFERENCES Class(class_id)
    );
    """,
]


def create_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        for table in DB_TABLES:
            _ = conn.execute(table)
        conn.commit()


# -------------------- INSERT FUNCTIONS --------------------


def insert_student(
    first_name: str, last_name: str, email: str, password: str, credits: int
):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        _ = cursor.execute(
            """
            INSERT INTO Student (first_name, last_name, email, password, credits)
            VALUES (?, ?, ?, ?, ?)
        """,
            (first_name, last_name, email, password, credits),
        )
        conn.commit()


def insert_professor(first_name: str, last_name: str, email: str, password: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        _ = cursor.execute(
            """
            INSERT INTO Professor (first_name, last_name, email, password)
            VALUES (?, ?, ?, ?)
        """,
            (first_name, last_name, email, password),
        )
        conn.commit()


def insert_administrator(first_name: str, last_name: str, email: str, password: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        _ = cursor.execute(
            """
            INSERT INTO Administrator (first_name, last_name, email, password)
            VALUES (?, ?, ?, ?)
        """,
            (first_name, last_name, email, password),
        )
        conn.commit()


def insert_class(course_id: int, course_name: str, professor: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        _ = cursor.execute(
            """
            INSERT INTO Class (course_id, course_name, professor)
            VALUES (?, ?, ?)
        """,
            (course_id, course_name, professor),
        )
        conn.commit()


def insert_student_class(student_id: int, class_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        _ = cursor.execute(
            """
            INSERT INTO Student_Class (student_id, class_id)
            VALUES (?, ?)
        """,
            (student_id, class_id),
        )
        conn.commit()


# -------------------- UPDATE FUNCTION --------------------


def update_record(table: str, id_field: str, record_id: int, **kwargs):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        fields = ", ".join([f"{key}=?" for key in kwargs])
        values = list(kwargs.values())
        values.append(record_id)
        query = f"UPDATE {table} SET {fields} WHERE {id_field}=?"
        _ = cursor.execute(query, values)
        conn.commit()


# -------------------- DELETE FUNCTION --------------------


def delete_record(table: str, id_field: str, record_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        _ = cursor.execute(f"DELETE FROM {table} WHERE {id_field}=?", (record_id,))
        conn.commit()


# -------------------- GET ALL ROWS FUNCTION --------------------


def get_all_rows(table: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        _ = cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()


def example():
    # Insert example professors
    insert_professor("Alan", "Turing", "aturing@univ.edu", "codebreaker")
    insert_professor("Grace", "Hopper", "ghopper@univ.edu", "debug")

    # Insert example administrators
    insert_administrator("Ada", "Lovelace", "ada@univ.edu", "math123")
    insert_administrator("Linus", "Torvalds", "linus@univ.edu", "kernel")

    # Insert example students
    insert_student("Alice", "Smith", "alice@univ.edu", "pass123", 30)
    insert_student("Bob", "Jones", "bob@univ.edu", "word456", 45)

    # Insert example classes (assuming professor IDs 1 and 2 exist)
    insert_class(101, "Intro to Computer Science", 1)
    insert_class(102, "Advanced Programming", 2)

    # Insert student-class relationships
    insert_student_class(1, 1)
    insert_student_class(2, 1)
    insert_student_class(2, 2)


if __name__ == "__main__":
    _ = create_db()
    create_tables()
    example()
