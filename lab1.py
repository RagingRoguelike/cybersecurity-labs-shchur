import re

# Персональні дані для аналізу потенційного зв'язку з паролем
USER_FIRST_NAME = "Віталій"
USER_LAST_NAME = "Щур"
USER_BIRTH_DATE = "29.05.2001"  # Формат: ДД.ММ.РРРР
USER_STUDENT_ID = "12345678"

def analyze_password_strength(password):
    score = 0
    recommendations = []
    
    # Приведення до нижнього регістру для уникнення проблем із чутливістю до регістру
    pwd_lower = password.lower()
    name_lower = USER_FIRST_NAME.lower()
    last_name_lower = USER_LAST_NAME.lower()
    
    # Розбиття дати на складові (день, місяць, рік)
    date_parts = USER_BIRTH_DATE.split('.')
    day = date_parts[0]
    month = date_parts[1]
    year = date_parts[2]
    
    # 1. Перевірка на використання персональних даних користувача
    personal_data_found = False
    
    if name_lower in pwd_lower and len(name_lower) > 2:
        recommendations.append(f"Вміст пароля: виявлено ім'я '{USER_FIRST_NAME}'.")
        personal_data_found = True
        
    if last_name_lower in pwd_lower and len(last_name_lower) > 2:
        recommendations.append(f"Вміст пароля: виявлено прізвище '{USER_LAST_NAME}'.")
        personal_data_found = True
        
    if day in password or month in password or year in password:
        recommendations.append(f"Вміст пароля: виявлено елементи дати народження ({USER_BIRTH_DATE}).")
        personal_data_found = True
        
    if USER_STUDENT_ID in password:
        recommendations.append("Вміст пароля: виявлено номер студентського квитка.")
        personal_data_found = True

    # 2. Оцінювання технічних критеріїв складності
    # Критерій довжини
    if len(password) >= 12:
        score += 3
    elif len(password) >= 8:
        score += 2
    else:
        recommendations.append("Порада: збільшіть довжину пароля (мінімум 8-12 символів).")
        score += 1

    # Наявність великих літер
    if re.search(r"[A-ZА-ЯҐЄІЇ]", password):
        score += 2
    else:
        recommendations.append("Порада: додайте хоча б одну велику літеру.")

    # Наявність малих літер
    if re.search(r"[a-zа-яґєії]", password):
        score += 1

    # Наявність цифр
    if re.search(r"[0-9]", password):
        score += 2
    else:
        recommendations.append("Порада: додайте цифри.")

    # Наявність спеціальних знаків
    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", password):
        score += 2
    else:
        recommendations.append("Порада: додайте спеціальні символи (наприклад: @, #, $, %).")

    # Штрафні санкції за використання персональної інформації
    if personal_data_found:
        recommendations.append("Критично: пароль побудований на особистих даних, що робить його вразливим до цільового підбору.")
        score = max(1, score - 3)

    # Максимальна підсумкова оцінка обмежена 10 балами
    final_score = min(10, score)
    
    return final_score, recommendations


def main():
    print("--- Програма аудиту стійкості паролів ---")
    print("Введіть 'exit' або 'вихід' для завершення роботи.")
    print("-" * 40)
    
    while True:
        user_password = input("\nВведіть пароль для перевірки: ").strip()
        
        # Перевірка умови виходу з циклу
        if user_password.lower() in ['exit', 'вихід', 'q']:
            print("Роботу програми завершено.")
            break
            
        if not user_password:
            print("Пароль не може бути порожнім. Спробуйте ще раз.")
            continue
            
        # Запуск аналізу
        score, recs = analyze_password_strength(user_password)
        
        print(f"Результат аналізу:")
        print(f"Підсумкова оцінка: {score} з 10 балів")
        
        if recs:
            print("Зауваження та рекомендації:")
            for r in recs:
                print(f" - {r}")
        else:
            print("Пароль відповідає критеріям безпеки. Зауважень немає.")
            
        print("-" * 40)


if __name__ == "__main__":
    main()
