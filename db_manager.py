import sqlite3
import os.path


class DbManager:
    def __init__(self):
        path = os.path.abspath('./db/points.sqlite')
        # Leave this out if the file doesn't exist yet
        assert os.path.exists(path), "The file doesn't exist"

        self.connect = sqlite3.connect(path)
        self.cursor = self.connect.cursor()

    def add_score(self, score):
        max_score = self.get_max_score()

        # adding only the first or a bigger values
        if max_score is None or score > max_score:
            self.cursor.execute(
                "INSERT INTO points(points) VALUES(?)", (score, )
            )

        self.connect.commit()

    def get_max_score(self):
        result = self.cursor.execute(
            "SELECT MAX(points) FROM points"
        ).fetchone()

        return result[0]
