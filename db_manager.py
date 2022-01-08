import sqlite3


class DbManager:
    def __init__(self):
        self.connect = sqlite3.connect('./db/points.sqlite')
        self.cursor = self.connect.cursor()

    def add_score(self, score):
        self.cursor.execute(
            "INSERT INTO points(points) VALUES(?)", (score, )
        )

        self.connect.commit()

    def get_max_score(self):
        result = self.cursor.execute(
            "SELECT MAX(points) FROM points"
        ).fetchone()

        return result[0]
