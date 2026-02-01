
from colorama import Fore
from colorama import Style
from client import client
from tracker import run_tracker
from config import LOCAL_TZ
import commands  # Импорт для регистрации обработчиков


async def main():

    print("--- Запуск Tracker ---")
    
    await client.start()
    print(f"{Fore.GREEN}✅ Успешное подключение к Telegram.{Style.RESET_ALL}")
    print('''
 1️⃣ Отслеживать по USERNAME/ID
 2️⃣ Получить ID (команда /getid)
 3️⃣ Кира''')

    choice = input("Выберите опцию (1/2/3): ").strip()

    if choice == '1':
        target = input("Введите USERNAME (с @) или ID пользователя: ").strip()
        await run_tracker(target)
    elif choice == '2':
        print(Fore.YELLOW + "✉️ Напишите /getid в нужном чате")
        await client.run_until_disconnected()
    elif choice == '3':
        target = '1001871134'
        await run_tracker(target)


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())