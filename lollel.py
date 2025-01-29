import os
import sys
import httpx
from colorama import Fore, init

# Инициализация Colorama
init(autoreset=True)

# Цвета для вывода
FR = Fore.RED
FG = Fore.GREEN
FY = Fore.YELLOW
FW = Fore.WHITE
FRE = Fore.RESET

def clear_screen():
    """Очистка экрана."""
    os.system('cls' if os.name == 'nt' else 'clear')

def read_proxies(file_name):
    """Чтение прокси из файла."""
    if not os.path.isfile(file_name):
        print(f"{FR}Файл {file_name} не найден!")
        sys.exit(1)
    with open(file_name, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def save_proxies_to_file(proxies, file_name):
    """Сохранение прокси в файл."""
    with open(file_name, 'w') as file:
        file.write("\n".join(proxies))
    print(f"\n{FW}({FY}{len(proxies)}{FW}) {FG}Рабочие прокси успешно сохранены в файл {file_name}.")

def check_proxy(proxy, timeout=5):
    """Проверка работоспособности прокси."""
    try:
        # Тестовый URL (можно заменить на другой)
        test_url = "http://www.google.com"
        with httpx.Client(proxies={"http://": f"http://{proxy}", "https://": f"http://{proxy}"}, timeout=timeout) as client:
            response = client.get(test_url)
            if response.status_code == 200:
                print(f" -| {FG}Прокси работает: {proxy}")
                return True
            else:
                print(f" -| {FR}Прокси не работает: {proxy}")
                return False
    except Exception:
        print(f" -| {FR}Прокси не работает: {proxy}")
        return False

def validate_proxies(proxies):
    """Проверка всех прокси на валидность."""
    valid_proxies = []
    for proxy in proxies:
        if check_proxy(proxy):
            valid_proxies.append(proxy)
    return valid_proxies

def main():
    file_name = "proxy.txt"
    
    # Очистка экрана
    clear_screen()

    # Чтение прокси из файла
    print(f"{FW}Чтение прокси из файла {file_name}...")
    proxies = read_proxies(file_name)

    if not proxies:
        print(f"{FR}Файл {file_name} пуст!")
        sys.exit(1)

    # Проверка прокси
    print(f"{FW}Начинаю проверку {FY}{len(proxies)}{FW} прокси...")
    valid_proxies = validate_proxies(proxies)

    # Сохранение рабочих прокси
    if valid_proxies:
        save_proxies_to_file(valid_proxies, file_name)
    else:
        print(f"{FR}Не найдено ни одного рабочего прокси.")
        sys.exit(1)

if __name__ == "__main__":
    main()