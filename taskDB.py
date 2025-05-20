import sqlite3

class TaskDB:
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, done INTEGER DEFAULT 0)"
        )
        self.conn.commit()

    def add_task(self, task):
        self.cursor.execute("INSERT INTO tasks (task, done) VALUES (?, 0)", (task,))
        self.conn.commit()

    def delete_task(self, task):
        self.cursor.execute("DELETE FROM tasks WHERE task = ?", (task,))
        self.conn.commit()

    def mark_done(self, task):
        self.cursor.execute("UPDATE tasks SET done = 1 WHERE task = ?", (task,))
        self.conn.commit()

    def get_tasks(self):
        return self.cursor.execute("SELECT task, done FROM tasks").fetchall()

    def close(self):
        self.conn.close()