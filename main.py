import mysql.connector
import json


class SQLTable:
    def __init__(self, db_config, table_name):
        self.db_config = db_config
        self.table_name = table_name
        self.connection = None
        self.cursor = None
        self.columns = []

        self.connect()

        if not self._check_table_exists():
            print(f"Таблица '{self.table_name}' не существует.")
        else:
            self._update_column_names()

    def connect(self):
        """
        подключение к бд
        """
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            print("Подключено")
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False

    def disconnect(self):
        """
        отключение от бд
        """
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Соединение закрыто")

    def _check_table_exists(self):
        """
        проверка существования таблицы
        """
        try:
            query = "SHOW TABLES LIKE %s"
            self.cursor.execute(query, (self.table_name,))
            return bool(self.cursor.fetchone())
        except:
            return False

    def _update_column_names(self):
        """
        Получение имён колонок таблицы
        """
        try:
            query = f"DESCRIBE {self.table_name}"
            self.cursor.execute(query)
            self.columns = [row[0] for row in self.cursor.fetchall()]
        except:
            self.columns = []

    # операции crud
    def insert_create(self, data):
        cursor = self.connection.cursor()
        try:
            columns = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
            cursor.execute(query, list(data.values()))
            self.connection.commit()
            print(f"INSERT: Добавлено в {self.table_name}")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()

    def select(self, condition=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = f"SELECT * FROM {self.table_name}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query)
            result = cursor.fetchall()
            print(f"SELECT: Получено {len(result)} записей")
            return result
        except Exception as e:
            print(f"Ошибка: {e}")
            return []
        finally:
            cursor.close()

    def update(self, data, condition):
        cursor = self.connection.cursor()
        try:
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE {condition}"
            cursor.execute(query, list(data.values()))
            self.connection.commit()
            print(f"UPDATE: Обновлено в {self.table_name}")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()

    def delete(self, condition):
        cursor = self.connection.cursor()
        try:
            query = f"DELETE FROM {self.table_name} WHERE {condition}"
            cursor.execute(query)
            self.connection.commit()
            print(f"DELETE: Удалено из {self.table_name}")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()

    def select(self, columns='*', condition=None):
        """
        получение данных с выбором колонок
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = f"SELECT {columns} FROM {self.table_name}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query)
            result = cursor.fetchall()
            print(f"SELECT: Получено {len(result)} записей")
            return result
        except Exception as e:
            print(f"Ошибка: {e}")
            return []
        finally:
            cursor.close()

    def drop_table(self):
        """DROP TABLE - Удаление таблицы"""
        cursor = self.connection.cursor()
        try:
            query = f"DROP TABLE IF EXISTS {self.table_name}"
            cursor.execute(query)
            self.connection.commit()
            print(f"DROP TABLE: Таблица {self.table_name} удалена")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()

    def create_table(self, columns):
        cursor = self.connection.cursor()
        try:
            query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns})"
            cursor.execute(query)
            self.connection.commit()
            print(f"CREATE TABLE: Таблица {self.table_name} создана")
            self._update_column_names()
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()


