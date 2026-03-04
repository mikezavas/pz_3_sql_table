from main import SQLTable
import json


db_config = {
    'host': 'srv221-h-st.jino.ru',
    'user': 'j30084097_13418',
    'password': 'pPS090207/()',
    'database': 'j30084097_13418',
    'port': 3306
}

if __name__ == "__main__":
    # Загрузка конфигурации
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            db_config = json.load(f)
    except:
        db_config = db_config

    # Создание объекта для работы с таблицей 'students'
    db = SQLTable(db_config, 'students')

    # 1. CREATE TABLE - Создание таблицы
    db.create_table('id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), grade INT')

    # 2. INSERT - Вставка данных
    db.insert_create({'name': 'Napoleon', 'grade': 85})
    db.insert_create({'name': 'Putin', 'grade': 90})
    db.insert_create({'name': 'Trump', 'grade': 78})

    print("\nВсе студенты")
    all_students = db.select()
    for student in all_students:
        print(f"  {student['id']}. {student['name']} - {student['grade']} баллов")

    print("\nСтуденты с оценкой > 80")
    good_students = db.select(columns='name, grade', condition='grade > 80')
    for student in good_students:
        print(f"  {student['name']} - {student['grade']} баллов")

    db.update({'grade': 95}, 'name = "Napoleon"')

    db.delete('name = "Trump"')

    db.drop_table()

    db.disconnect()
