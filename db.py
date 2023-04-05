import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли заказчик в базе"""
        result = self.cursor.execute("SELECT `id` FROM `account` WHERE `user_id` = ?", (user_id,))
        return not bool(result.fetchone() is None)

    def get_balance(self, user_id):
        """Достаем баланс в базе по его user_id"""
        result = self.cursor.execute("SELECT `balance` FROM `account` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]



    def add_user(self, user_id: int, first_name: str, last_name: str, surname: str, birth_date: str, tg_user_id : int):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO account (birth_date,surname,last_name,first_name,inn,user_id ) VALUES(?,?,?,?,?,?);",(birth_date, surname, last_name, first_name, int(user_id), tg_user_id))
        return self.conn.commit()
