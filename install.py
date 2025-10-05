import os
import secrets
from getpass import getpass
from werkzeug.security import generate_password_hash

def main():
    print("=== Установка LocalCloudKT ===")

    # 1. Secret key — запрашиваем, если пусто — генерируем
    secret_key = input("Введите секретный ключ приложения (press Enter для генерации): ").strip()
    if not secret_key:
        secret_key = secrets.token_urlsafe(32)
        print(f"Сгенерирован секретный ключ приложения: {secret_key}")

    # 2. Корневая папка — если пусто, используем C:\LocalCloudKT
    base_folder = input(r"Введите путь для корневой папки (по умолчанию C:\LocalCloudKT): ").strip()
    if not base_folder:
        base_folder = r"C:\LocalCloudKT"
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        print(f"Создана папка: {base_folder}")

    # 3. Пароль для входа — обязательное поле
    password = getpass("Введите пароль для входа: ").strip()
    if not password:
        print("Ошибка: пароль не может быть пустым")
        return
    password_hash = generate_password_hash(password)

    # 4. Запись в переменные окружения пользователя
    os.system(f'setx LCKT_APP_SECRET "{secret_key}"')
    os.system(f'setx LCKT_BASE_FOLDER "{base_folder}"')
    os.system(f'setx LCKT_PASSWORD_HASH "{password_hash}"')

    print("\nУстановка завершена!")
    print("Теперь запустите приложение LocalCloudKT. Новые переменные окружения будут видны после перезапуска терминала или системы.")

if __name__ == "__main__":
    main()
