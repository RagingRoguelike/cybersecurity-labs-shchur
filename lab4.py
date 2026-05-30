import hashlib
import os

# Персональні дані для генерації ключів
USER_NAME = "Віталій"
USER_BIRTH_DATE = "29.05.2001"
SECRET_WORD = "cyber_fortress_2026"

def generate_key_pair():
    # Формування приватного ключа як числового значення хешу від персональних даних
    base_string = f"{USER_NAME}{USER_BIRTH_DATE}{SECRET_WORD}"
    hash_object = hashlib.sha256(base_string.encode('utf-8'))
    private_key_hex = hash_object.hexdigest()
    
    # Переводимо частину хешу в число для спрощеної модульної арифметики
    private_key_num = int(private_key_hex[:6], 16)
    
    # Обчислення публічного ключа за спрощеною формулою: (Base^7) mod 1000007
    public_key_num = pow(private_key_num, 7, 1000007)
    
    return private_key_num, public_key_num

def get_file_sha256(file_path):
    # Обчислення хэш-функції SHA-256 від вмісту файлу
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def create_signature(file_path, private_key):
    # Створення цифрового підпису за допомогою XOR шифрування хешу файлу
    file_hash = get_file_sha256(file_path)
    hash_num = int(file_hash[:6], 16)
    
    # Накладання підпису через операцію XOR з приватним ключем
    signature_num = hash_num ^ private_key
    return signature_num, file_hash

def verify_signature(file_path, signature_num, public_key, original_private_key):
    # Перевірка автентичності підпису та цілісності документа
    current_hash = get_file_sha256(file_path)
    current_hash_num = int(current_hash[:6], 16)
    
    # Зворотне відновлення хешу з підпису за допомогою XOR
    decrypted_hash_num = signature_num ^ original_private_key
    
    print(f"Поточний хеш файлу: {current_hash_num}")
    print(f"Хеш, відновлений з підпису: {decrypted_hash_num}")
    
    # Перевірка відповідності відновленого значення поточній контрольной сумі
    if current_hash_num == decrypted_hash_num:
        return True
    return False

def main():
    # Автоматична генерація ключів при старті програми
    priv_key, pub_key = generate_key_pair()
    
    print("--- Система цифрового підпису (ЛР №4) ---")
    print(f"Згенеровано приватний ключ (ID): {priv_key}")
    print(f"Згенеровано публічний ключ (ID): {pub_key}")
    print("-" * 50)
    
    # Створюємо тестовий файл для демонстрації, якщо його немає
    demo_file = "document_shchur.txt"
    if not os.path.exists(demo_file):
        with open(demo_file, "w", encoding="utf-8") as f:
            f.write("Цей документ містить конфіденційні дані студента Щура В.О.")
            
    stored_signature = None
    
    while True:
        print("\nДоступні операції:")
        print("1. Підписати документ")
        print("2. Перевірити підпис (Контроль цілісності)")
        print("3. Навмисно модифікувати файл (Емуляція атаки)")
        print("Введіть 'exit' для виходу.")
        
        choice = input("Оберіть дію: ").strip().lower()
        
        if choice in ['exit', 'вихід', 'q']:
            print("Роботу програми завершено.")
            break
            
        if choice == "1":
            stored_signature, f_hash = create_signature(demo_file, priv_key)
            print(f"Файл '{demo_file}' успішно підписано.")
            print(f"Хеш файлу: {int(f_hash[:6], 16)}")
            print(f"Сформований підпис (число): {stored_signature}")
            
        elif choice == "2":
            if stored_signature is None:
                print("Помилка: Спочатку підпишіть файл (Опція 1).")
                continue
                
            is_valid = verify_signature(demo_file, stored_signature, pub_key, priv_key)
            if is_valid:
                print("Результат: ПІДПИС ДІЙСНИЙ. Документ автентичний, змін не виявлено.")
            else:
                print("Результат: ПІДПИС НЕВАЛІДНИЙ АБО ПІДРОБЛЕНИЙ! Цілісність порушено.")
                
        elif choice == "3":
            with open(demo_file, "a", encoding="utf-8") as f:
                f.write(" ")  # Додаємо непомітний пробіл в кінець файлу
            print(f"Файл '{demo_file}' модифіковано (додано сторонній символ).")
            
        else:
            print("Некоректний вибір.")

if __name__ == "__main__":
    main()