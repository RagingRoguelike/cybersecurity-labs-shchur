# Персональні дані для автоматичної генерації криптографічних ключів
USER_LAST_NAME = "Щур"
USER_BIRTH_DATE = "29.05.2001"

# Базовий український алфавіт у нижньому регістрі для розрахунку індексів
UA_ALPHABET = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"

def calculate_caesar_shift(date_str):
    # Обчислення зсуву як суми всіх цифр у рядку дати народження
    return sum(int(char) for char in date_str if char.isdigit())

def caesar_cipher(text, shift, decrypt=False):
    # Реалізація моноалфавітного шифру Цезаря для українського алфавіту
    if decrypt:
        shift = -shift
        
    result = []
    alpha_len = len(UA_ALPHABET)
    
    for char in text:
        is_upper = char.isupper()
        char_lower = char.lower()
        
        if char_lower in UA_ALPHABET:
            current_idx = UA_ALPHABET.index(char_lower)
            new_idx = (current_idx + shift) % alpha_len
            new_char = UA_ALPHABET[new_idx]
            result.append(new_char.upper() if is_upper else new_char)
        else:
            # Розділові знаки, пробіли та цифри залишаються без змін
            result.append(char)
            
    return "".join(result)

def vigenere_cipher(text, key, decrypt=False):
    # Реалізація поліалфавітного шифру Віженера з підтримкою кирилиці
    result = []
    alpha_len = len(UA_ALPHABET)
    key_lower = key.lower()
    
    # Формування масиву зсувів на основі позицій літер ключа в алфавіті
    key_indices = [UA_ALPHABET.index(k) for k in key_lower if k in UA_ALPHABET]
    
    if not key_indices:
        return "Помилка: Ключ повинен містити літери українського алфавіту."
        
    key_cycle_idx = 0
    
    for char in text:
        is_upper = char.isupper()
        char_lower = char.lower()
        
        if char_lower in UA_ALPHABET:
            shift = key_indices[key_cycle_idx % len(key_indices)]
            if decrypt:
                shift = -shift
                
            current_idx = UA_ALPHABET.index(char_lower)
            new_idx = (current_idx + shift) % alpha_len
            new_char = UA_ALPHABET[new_idx]
            
            result.append(new_char.upper() if is_upper else new_char)
            key_cycle_idx += 1
        else:
            result.append(char)
            
    return "".join(result)

def main():
    caesar_shift = calculate_caesar_shift(USER_BIRTH_DATE)
    vigenere_key = USER_LAST_NAME
    
    print("--- Програма шифрування повідомлень (ЛР №2) ---")
    print(f"Персоналізований зсув Цезаря: {caesar_shift}")
    print(f"Персоналізований ключ Віженера: '{vigenere_key}'")
    print("Введіть 'exit' або 'вихід' для завершення роботи.")
    print("-" * 50)
    
    while True:
        message = input("\nВведіть текст для обробки: ").strip()
        
        if message.lower() in ['exit', 'вихід', 'q']:
            print("Роботу програми завершено.")
            break
            
        if not message:
            print("Рядок не може бути порожнім.")
            continue
            
        # Демонстрація роботи шифру Цезаря
        caesar_encrypted = caesar_cipher(message, caesar_shift)
        caesar_decrypted = caesar_cipher(caesar_encrypted, caesar_shift, decrypt=True)
        
        # Демонстрація роботи шифру Віженера
        vigenere_encrypted = vigenere_cipher(message, vigenere_key)
        vigenere_decrypted = vigenere_cipher(vigenere_encrypted, vigenere_key, decrypt=True)
        
        # Виведення порівняльних результатів
        print("\nРезультати криптографічної обробки:")
        print(f"1. Шифр Цезаря")
        print(f"   Зашифровано:  {caesar_encrypted}")
        print(f"   Розшифровано: {caesar_decrypted}")
        print(f"2. Шифр Віженера")
        print(f"   Зашифровано:  {vigenere_encrypted}")
        print(f"   Розшифровано: {vigenere_decrypted}")
        print("-" * 50)

if __name__ == "__main__":
    main()