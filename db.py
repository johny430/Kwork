import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли заказчик в базе"""
        result = self.cursor.execute("SELECT `id` FROM `account` WHERE `user_id` = (?)", (user_id,))
        return not bool(result.fetchone() is None)

    def get_balance(self, user_id):
        """Достаем баланс в базе по его user_id"""
        result = self.cursor.execute("select balance from account where user_id = (?)", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id: int, first_name: str, last_name: str, surname: str, birth_date: str, tg_user_id: int,
                 account_type: int):
        """Добавляем юзера в базу"""
        self.cursor.execute(
            "INSERT INTO account (birth_date,surname,last_name,first_name,inn,user_id,type_of_account ) VALUES(?,?,?,?,?,?,?);",
            (birth_date, surname, last_name, first_name, int(user_id), tg_user_id, account_type))
        return self.conn.commit()

    def add_order(self, name, price, description, customer_id):
        """Добавляем заказ в базу"""
        self.cursor.execute(
            "insert into orders (oder_name, order_price, order_description, customer_id) values (?,?,?,?);",
            (name, price, description, customer_id))
        return self.conn.commit()

    def add_profile(self, user_id, speciality, price, description):
        """Добавляем профиль в базу"""
        self.cursor.execute(
            "insert into profile (user_id, specialyti, price, description) values (?,?,?,?);",
            (user_id, speciality, price, description))
        return self.conn.commit()

    def get_orders(self):
        """Получаем заказ из базы"""
        results = self.cursor.execute("SELECT * FROM orders")
        return results.fetchall()

    def get_order_id(self, id):
        """Получаем конкретный заказ из базы"""
        results = self.cursor.execute(
            "SELECT id, oder_name, order_price, order_description, customer_id FROM orders WHERE id = (?)",
            (id,))
        return results.fetchone()

    def get_profile(self):
        """Получаем профили из базы"""
        results = self.cursor.execute("SELECT id, specialyti, price, description FROM profile")
        return results.fetchall()

    def get_profile_id(self, id):
        """Получаем конкретный профиль из базы"""
        results = self.cursor.execute(
            "SELECT id, oder_name, order_price, order_description, customer_id FROM orders WHERE id = (?)",
            (id,))
        return results.fetchone()

    def add_CoverLetter(self, order_id, CoverLetter, executor_id):
        """Добавляем сопроводительное письмо в базу"""
        self.cursor.execute("insert into Customer_review (order_id, CoverLetter, executor_id) values (?,?,?);",
                            (order_id, CoverLetter, executor_id))
        return self.conn.commit()

    def add_TZ(self, profile_id, tz, customer_id):
        """Добавляем ТЗ в базу"""
        self.cursor.execute("insert into tz (profile_id, tz, customer_id) values (?,?,?);",
                            (profile_id, tz, customer_id))
        return self.conn.commit()
