import sqlite3

def setup_database():
    # Ініціалізація бази даних в оперативній пам'яті
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    
    # Створення таблиці користувачів з персональними та тестовими даними
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            phone TEXT,
            secret_note TEXT
        )
    """)
    
    # Наповнення таблиці тестовими записами
    test_data = [
        ("vitaliy_shchur", "vitaliy.shchur8@gmail.com", "+380501234567", "Персональний закритий ключ: сума дат = 19"),
        ("admin", "admin@cybersec.local", "+380671112233", "Головний пароль системи: СклянаТвердиня2026"),
        ("ivan_petrenko", "ivan.pet@mail.com", "+380939998877", "Нотатка: забув змінити дефолтний пароль роутера"),
        ("maria_koval", "m.koval@gmail.com", "+380505554433", "Секретне слово для відновлення: Квітка")
    ]
    
    cursor.executemany("INSERT INTO users (username, email, phone, secret_note) VALUES (?, ?, ?, ?)", test_data)
    connection.commit()
    return connection

def vulnerable_search(connection, search_query):
    # Демонстрація вразливого пошуку через пряме підставлення рядка
    cursor = connection.cursor()
    
    # Формування вразливого SQL-запиту за допомогою конкатенації
    sql_raw = "SELECT username, email, phone FROM users WHERE username = '" + search_query + "'"
    
    print(f"\n[ЛОГ СИСТЕМИ] Виконується сирий SQL-запит:")
    print(f"  {sql_raw}")
    
    try:
        cursor.execute(sql_raw)
        results = cursor.fetchall()
        return results, None
    except sqlite3.Error as e:
        return None, str(e)

def secure_search(connection, search_query):
    # Демонстрація захищеного пошуку за допомогою параметризованого запиту
    cursor = connection.cursor()
    
    # Використання знаку питання як плейсхолдера для безпечної передачі аргументів
    sql_secure = "SELECT username, email, phone FROM users WHERE username = ?"
    
    print(f"\n[ЛОГ СИСТЕМИ] Виконується параметризований SQL-запит:")
    print(f"  {sql_secure}")
    print(f"  Параметр: ('{search_query}',)")
    
    try:
        cursor.execute(sql_secure, (search_query,))
        results = cursor.fetchall()
        return results, None
    except sqlite3.Error as e:
        return None, str(e)

def main():
    db_conn = setup_database()
    
    print("--- Програма емуляції SQL-ін'єкцій та методів захисту (ЛР №6) ---")
    print("Введіть 'exit' або 'вихід' для завершення роботи.")
    print("-" * 65)
    
    while True:
        user_input = input("\nВведіть ім'я користувача для пошуку (username): ").strip()
        
        if user_input.lower() in ['exit', 'вихід', 'q']:
            print("Роботу програми завершено.")
            break
            
        if not user_input:
            print("Рядок пошуку не може бути порожнім.")
            continue
            
        # Етап 1: Тестування вразливої версії системи
        print("\n=== ЕТАП 1: ТЕСТУВАННЯ ВРАЗЛИВОЇ ВЕРСІЇ ===")
        vuln_results, vuln_error = vulnerable_search(db_conn, user_input)
        
        if vuln_error:
            print(f"Помилка виконання СКБД: {vuln_error}")
        elif vuln_results:
            print("Знайдені записи користувачів:")
            for row in vuln_results:
                print(f"  Користувач: {row[0]} | Email: {row[1]} | Телефон: {row[2]}")
        else:
            print("Записів із таким іменем не знайдено.")
            
        # Етап 2: Тестування захищеної версії системи
        print("\n=== ЕТАП 2: ТЕСТУВАННЯ ЗАХИЩЕНОЇ ВЕРСІЇ ===")
        sec_results, sec_error = secure_search(db_conn, user_input)
        
        if sec_error:
            print(f"Помилка виконання СКБД: {sec_error}")
        elif sec_results:
            print("Знайдені записи користувачів:")
            for row in sec_results:
                print(f"  Користувач: {row[0]} | Email: {row[1]} | Телефон: {row[2]}")
        else:
            print("Записів із таким іменем не знайдено.")
            
        print("-" * 65)

if __name__ == "__main__":
    main()