import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def customer_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `balance` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def executor_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `balance` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_customer_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `balance` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def get_executor_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `balance` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_customer(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `balance` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_executor(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `balance` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()
