import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли заказчик в базе"""
        result = self.cursor.execute("SELECT `id` FROM `account` WHERE `user_id` = (?)", (user_id,))
        return not bool(result.fetchone() is None)

    def get_order_id(self, customer_id):
        result = self.cursor.execute("select id from orders where customer_id = (?) order by id desc limit 0,1", (customer_id,))
        return result.fetchone()[0]

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

    def add_order(self, name, price, category, deadline, description, customer_id):
        """Добавляем заказ в базу"""
        self.cursor.execute(
            "insert into orders (oder_name, order_price, order_category, order_deadline, order_description, customer_id) values (?,?,?,?,?,?);",
            (name, price, category, deadline, description, customer_id))
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

    def get_order_by_group_id(self, group_id):
        results = self.cursor.execute(
            "select * from orders where id = (select order_id from order_review where id = (select review_id from review_group where chat_id = (?)))",
            (group_id,))
        return results.fetchone()

    def get_orders_by_customer_id(self, customer_id):
        """Получаем заказ из базы"""
        results = self.cursor.execute("SELECT * FROM orders WHERE customer_id = (?)", (customer_id,))
        return results.fetchall()

    def get_orders_by_category(self, order_category):
        """Получаем заказ из базы"""
        results = self.cursor.execute("SELECT * FROM orders WHERE order_category = (?)", (order_category,))
        return results.fetchall()

    def get_profile(self, profile_category):
        """Получаем профили из базы"""
        results = self.cursor.execute("SELECT * FROM profile WHERE profile_category = (?)", (profile_category,))
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

    def add_CoverLetter(self, order_id, deadline, cost, CoverLetter, executor_id):
        """Добавляем сопроводительное письмо в базу"""
        self.cursor.execute(
            "insert into order_review (order_id, dedline, cost, CoverLetter, executor_id) values (?,?,?,?,?);",
            (order_id, deadline, cost, CoverLetter, executor_id))
        return self.conn.commit()

    def add_TZ(self, profile_id, deadline, cost, tz, customer_id):
        """Добавляем ТЗ в базу"""
        self.cursor.execute("insert into tz (profile_id, deadline, cost, tz, customer_id) values (?,?,?,?,?);",
                            (profile_id, deadline, cost, tz, customer_id))
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

    def add_message(self, chat_id, message_text, user_id, date):
        """Добавляем ТЗ в базу"""
        self.cursor.execute("insert into messages (text, chat_id, date, user_id) values (?,?,?,?);",
                            (message_text, chat_id, date, user_id))
        return self.conn.commit()

    def get_executor_id_by_group_id(self, group_id):
        """"Получаем отклики на профиль"""
        results = self.cursor.execute(
            "SELECT executor_id from order_review where id = (SELECT review_id from review_group where chat_id = (?))",
            (group_id,))
        return results.fetchone()[0]

    def get_customer_id_by_group_id(self, group_id):
        """"Получаем отклики на профиль"""
        results = self.cursor.execute(
            "SELECT customer_id from orders WHERE id = (SELECT order_id from order_review where id = (SELECT review_id from review_group where chat_id = (?)))",
            (group_id,))
        return results.fetchone()[0]

    def add_review_group(self, group_id, review_id):
        """Добавляем ТЗ в базу"""
        self.cursor.execute(
            "insert into review_group (review_id, chat_id,customer_agree,executor_agree) values (?,?,?,?);",
            (review_id, group_id, 0, 0))
        return self.conn.commit()

    def agree_customer(self, group_id):
        """Добавляем ТЗ в базу"""
        self.cursor.execute("update review_group set customer_agree = 1  where chat_id = (?);", (group_id,))
        return self.conn.commit()

    def agree_executor(self, group_id):
        """Добавляем ТЗ в базу"""
        self.cursor.execute("update review_group set executor_agree = 1  where chat_id = (?);", (group_id,))
        return self.conn.commit()

    def conformation_count(self, group_id):
        result = self.cursor.execute("select customer_agree + executor_agree from review_group where chat_id = (?)",
                                     (group_id,))
        return result.fetchone()[0]

    def zero_conformation(self, group_id):
        self.cursor.execute("update review_group set executor_agree = 0, executor_agree = 0  where chat_id = (?);",
                            (group_id,))
        return self.conn.commit()

    def get_review_by_group(self, group_id):
        results = self.cursor.execute(
            "SELECT * from order_review where id = (SELECT review_id from review_group where chat_id = (?))",
            (group_id,))
        return results.fetchone()

    def get_confirmed_order(self, group_id):
        results = self.cursor.execute(
            "SELECT * from confirmed_orders where group_review_id = (SELECT id from review_group where chat_id = (?))",
            (group_id,))
        return results.fetchone()

    def clear_by_group(self, group_id, confirmed_order_id, order_id):
        # self.cursor.execute("DELETE FROM confirmed_orders WHERE id=(?)", confirmed_order_id)
        self.cursor.execute("DELETE FROM messages WHERE chat_id=(?)", (group_id,))
        self.cursor.execute("DELETE FROM review_group WHERE chat_id=(?)", (group_id,))
        self.cursor.execute("DELETE FROM orders WHERE id=(?)", (order_id,))
        self.cursor.execute("DELETE FROM order_review WHERE order_id=(?)", (order_id,))
        self.conn.commit()

    def get_review_group_id(self, group_id):
        results = self.cursor.execute(
            "SELECT id from review_group where chat_id = ((?))",
            (group_id,))
        return results.fetchone()

    def confirm_order_from_group(self, reward, group_review_id):
        self.cursor.execute("insert into confirmed_orders (reward, group_review_id) values (?,?)",
                            (reward, group_review_id))
        return self.conn.commit()

    def convert_profile(self, order_price, order_deadline, customer_id):
        self.cursor.execute("insert into orders (order_price, order_deadline, customer_id) values (?,?,?)",(order_price,order_deadline,customer_id))
        return self.conn.commit()

    def convert_review(self,order_id, order_price, order_deadline, executor_id):
        self.cursor.execute("insert into order_review (order_id, cost, dedline, executor_id) values (?,?,?,?)",(order_id, order_price,order_deadline,executor_id))
        return self.conn.commit()

    def  get_review_id(self, order_id):
        results = self.cursor.execute(
            "SELECT id from order_review where order_id = (?)",
            (order_id,))
        return results.fetchone()[0]

    def update_review_price(self,review_id,new_price):
        self.cursor.execute(f"update order_review set cost = {new_price} where id = {review_id}")
        return self.conn.commit()


    def update_review_dedline(self,review_id,new_dedline):
        self.cursor.execute(f"update order_review set dedline = {new_dedline} where id = {review_id}")
        return self.conn.commit()