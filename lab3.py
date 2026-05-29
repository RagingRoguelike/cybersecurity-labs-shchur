import os
from PIL import Image

# Персональні дані для автоматичного приховування
SECRET_MESSAGE = "Віталій Щур, 29.05.2001"

def text_to_bits(text):
    # Конвертація тексту в послідовність бітів (у кодуванні utf-8)
    bits = []
    # Додаємо маркер кінця повідомлення (\x00), щоб знати, де зупинити читання
    encoded_text = text.encode('utf-8') + b'\x00'
    for byte in encoded_text:
        for i in range(8):
            # Витягуємо кожен біт з байта (від старшого до молодшого)
            bits.append((byte >> (7 - i)) & 1)
    return bits

def bits_to_text(bits):
    # Конвертація послідовності бітів назад у текстовий рядок
    bytes_list = bytearray()
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            break
        byte_val = 0
        for bit in byte_bits:
            byte_val = (byte_val << 1) | bit
        # Якщо зустріли нульовий байт (маркер кінця), припиняємо зчитування
        if byte_val == 0:
            break
        bytes_list.append(byte_val)
    
    try:
        return bytes_list.decode('utf-8')
    except UnicodeDecodeError:
        return "Помилка: Не вдалося коректно декодувати дані."

def hide_message(image_path, output_path, text):
    # Приховування тексту в молодших бітах RGB компонент пікселів
    img = Image.open(image_path)
    # Переводимо в режим RGB, якщо зображення має інший формат (наприклад, RGBA)
    img = img.convert('RGB')
    pixels = img.load()
    
    width, height = img.size
    bit_sequence = text_to_bits(text)
    bit_count = len(bit_sequence)
    
    if bit_count > width * height * 3:
        return "Помилка: Розмір повідомлення занадто великий для цього зображення."
        
    bit_idx = 0
    for y in range(height):
        for x in range(width):
            if bit_idx >= bit_count:
                break
                
            r, g, b = pixels[x, y]
            
            # Модифікуємо молодший біт червоного каналу
            if bit_idx < bit_count:
                r = (r & ~1) | bit_sequence[bit_idx]
                bit_idx += 1
            # Модифікуємо молодший біт зеленого каналу
            if bit_idx < bit_count:
                g = (g & ~1) | bit_sequence[bit_idx]
                bit_idx += 1
            # Модифікуємо молодший біт синього каналу
            if bit_idx < bit_count:
                b = (b & ~1) | bit_sequence[bit_idx]
                bit_idx += 1
                
            pixels[x, y] = (r, g, b)
            
        if bit_idx >= bit_count:
            break
            
    img.save(output_path, format="PNG")
    return "Повідомлення успішно впроваджено в стегоконтейнер."

def extract_message(image_path):
    # Витягування прихованого тексту з молодших бітів пікселів
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()
    
    width, height = img.size
    extracted_bits = []
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Зчитуємо останні біти з кожного каналу
            extracted_bits.append(r & 1)
            extracted_bits.append(g & 1)
            extracted_bits.append(b & 1)
            
            # Перевіряємо кожні 8 біт на наявність нульового байта (маркера кінця)
            if len(extracted_bits) % 8 == 0:
                # Беремо останній сформований байт
                last_byte_bits = extracted_bits[-8:]
                byte_val = 0
                for bit in last_byte_bits:
                    byte_val = (byte_val << 1) | bit
                if byte_val == 0:
                    return bits_to_text(extracted_bits)
                    
    return bits_to_text(extracted_bits)

def main():
    print("--- Програма LSB-стеганографії (ЛР №3) ---")
    print("Введіть 'exit' або 'вихід' для завершення.")
    print("-" * 50)
    
    while True:
        print("\nОберіть дію:")
        print("1. Заховати персональні дані в картинку")
        print("2. Прочитати приховані дані з картинки")
        choice = input("Твій вибір (1/2): ").strip()
        
        if choice.lower() in ['exit', 'вихід', 'q']:
            print("Роботу програми завершено.")
            break
            
        if choice == "1":
            input_img = input("Вкажіть шлях до оригінального зображення (наприклад, input.jpg): ").strip()
            if not os.path.exists(input_img):
                print("Помилка: Файл не знайдено.")
                continue
                
            output_img = input("Вкажіть назву для збереженого файлу (обов'язково .png): ").strip()
            if not output_img.lower().endswith('.png'):
                print("Помилка: Для збереження LSB-контейнера необхідний формат PNG (без втрат стиснення).")
                continue
                
            result = hide_message(input_img, output_img, SECRET_MESSAGE)
            print(result)
            if "успішно" in result:
                print(f"У файл було запечено рядок: '{SECRET_MESSAGE}'")
                
        elif choice == "2":
            stego_img = input("Вкажіть шлях до стегоконтейнера (.png файл): ").strip()
            if not os.path.exists(stego_img):
                print("Помилка: Файл не знайдено.")
                continue
                
            extracted = extract_message(stego_img)
            print(f"\nЗнайдений прихований текст: {extracted}")
        else:
            print("Некоректний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()