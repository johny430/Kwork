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

    def add_user(self, user_id: int, account_type: int):
        """Добавляем юзера в базу"""
        self.cursor.execute(
            "INSERT INTO account (user_id,type_of_account ) VALUES(?,?);",
            (int(user_id), account_type))
        return self.conn.commit()

    def add_order(self, name, price, category, description, customer_id):
        """Добавляем заказ в базу"""
        self.cursor.execute(
            "insert into orders (oder_name, order_price, order_category, order_description, customer_id) values (?,?,?,?,?);",
            (name, price, category, description, customer_id))
        return self.conn.commit()

    def add_order_tz(self, name, price, category, description, customer_id, tz_file_id):
        """Добавляем заказ в базу"""
        self.cursor.execute(
            "insert into orders (oder_name, order_price, order_category, order_description, customer_id,tz_file_id) values (?,?,?,?,?,?);",
            (name, price, category, description, customer_id, tz_file_id))
        return self.conn.commit()

    def add_profile(self, user_id, speciality, category, price, description):
        """Добавляем профиль в базу"""
        self.cursor.execute(
            "insert into profile (user_id, specialyti,profile_category, price, description) values (?,?,?,?,?);",
            (user_id, speciality, category, price, description))
        return self.conn.commit()

    def get_orders_by_customer_id(self, customer_id):
        """Получаем заказ из базы"""
        results = self.cursor.execute("SELECT * FROM orders WHERE customer_id = (?)", (customer_id,))
        return results.fetchall()

    def get_orders_by_category(self, order_category):
        """Получаем заказ из базы"""
        results = self.cursor.execute("SELECT * FROM orders WHERE order_category = (?)", (order_category,))
        return results.fetchall()

    def get_order_for(self, castomer_id):
        """Получаем заказ из базы"""
        results = self.cursor.execute("SELECT * FROM orders WHERE castomer_id = (?)", (castomer_id,))
        return results.fetchall()

    def get_order_id(self, id):
        """Получаем конкретный заказ из базы"""
        results = self.cursor.execute(
            "SELECT id, oder_name, order_price, order_description, customer_id FROM orders WHERE id = (?)",
            (id,))
        return results.fetchone()

    def get_profile(self, profile_category):
        """Получаем профили из базы"""
        results = self.cursor.execute("SELECT * FROM profile WHERE profile_category = (?)", (profile_category))
        return results.fetchall()

    def get_profile_for(self, user_id):
        """Получаем профили из базы"""
        results = self.cursor.execute("SELECT * FROM profile WHERE user_id = (?)", (user_id,))
        return results.fetchall()

    def get_profile_id(self, id):
        """Получаем конкретный профиль из базы"""
        results = self.cursor.execute(
            "SELECT id, oder_name, order_price, order_description, customer_id FROM orders WHERE id = (?)",
            (id,))
        return results.fetchone()

    def add_CoverLetter(self, order_id, CoverLetter, executor_id):
        """Добавляем сопроводительное письмо в базу"""
        self.cursor.execute("insert into order_review (order_id, CoverLetter, executor_id) values (?,?,?);",
                            (order_id, CoverLetter, executor_id))
        return self.conn.commit()

    def add_TZ(self, profile_id, tz, customer_id):
        """Добавляем ТЗ в базу"""
        self.cursor.execute("insert into tz (profile_id, tz, customer_id) values (?,?,?);",
                            (profile_id, tz, customer_id))
        return self.conn.commit()

    def get_orders_reviews(self, order):
        """Получаем профили из базы"""
        results = self.cursor.execute("SELECT * FROM order_review where order_id = (?)", (order,))
        return results.fetchall()

    def get_profile_reviews(self, profile_id):
        """"Получаем отклики на профиль"""
        results = self.cursor.execute("SELECT * FROM tz WHERE profile_id = (?)", (profile_id,))
        return results.fetchall()

    def update_balance(self, user_id, upd_balance):
        """Заменяем значение балланса"""
        self.cursor.execute("UPDATE account SET balance = (?) WHERE user_id = (?) ", (upd_balance, user_id))
        return self.conn.commit()

    def add_message(self, chat_id, message_text, user_id,date):
        """Добавляем ТЗ в базу"""
        self.cursor.execute("insert into messages (text, chat_id, date, user_id) values (?,?,?,?);",
                            (message_text, chat_id, date, user_id))
        return self.conn.commit()
