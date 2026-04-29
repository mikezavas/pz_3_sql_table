from main import SQLTable
import json



if __name__ == "__main__":
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            db_config = json.load(f)
    except:
        db_config = db_config

    db = SQLTable(db_config, 'students')

    db.create_table('id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), grade INT')

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
