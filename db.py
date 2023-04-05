import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def customer_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `customer` WHERE `user_id` = ?", (user_id,))
        return not bool(result.fetchone() is None)

    def executor_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `executor` WHERE `user_id` = ?", (user_id,))
        return not bool(result.fetchone() is None)

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

    def add_executor(self, user_id: int, first_name: str, last_name: str, surname: str, birth_date: str, tg_user_id: int):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO executor (birth_date,surname,last_name,first_name,executor_id,user_id ) VALUES(?,?,?,?,?,?);", (birth_date, surname, last_name, first_name,int(user_id),tg_user_id))
        return self.conn.commit()
