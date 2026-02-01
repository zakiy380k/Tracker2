from client import client
from utils import convert_utc_to_local, format_status, resolve_target
from config import LOCAL_TZ
import asyncio
from colorama import Fore, Style, init
from datetime import datetime
import time

init(autoreset=True)

print(Fore.CYAN + '''
███████╗░█████╗░██╗░░██╗██╗
╚════██║██╔══██╗██║░██╔╝██║
░░███╔═╝███████║█████═╝░██║
██╔══╝░░██╔══██║██╔═██╗░██║
███████╗██║░░██║██║░╚██╗██║
╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝''' + Style.RESET_ALL)


async def run_tracker(target_input):
    
    # Первичная проверка, существует ли пользователь
    initial_entity = await resolve_target(target_input)
    if not initial_entity:
        return
    
    target_id = initial_entity.id

    # Определяем имя для логов
    target_label = f"{initial_entity.first_name} {initial_entity.last_name or ''}".strip()
    if not target_label:
        target_label = initial_entity.username or str(initial_entity.id)

    print(f"\n📡 Начинаю слежку за: {Fore.CYAN}{target_label}{Style.RESET_ALL} (Timezone: {LOCAL_TZ.zone})")
    print("Нажмите Ctrl+C для выхода.\n")
    
    previous_state = None # "Online" или "Offline"
    last_online_start = None # Время начала онлайна

    while True:
        try:
            # 1. ОБЯЗАТЕЛЬНО обновляем сущность, чтобы получить свежий статус
            # Используем target_input, так как объект entity устаревает
            entity = await client.get_entity(target_id)
            
            status_text, state = format_status(entity)
            current_time = datetime.now(LOCAL_TZ).strftime('%H:%M:%S')

            # Логика смены статуса
            if state != previous_state:
                
                # ---> Переход в ONLINE
                if state == "Online":
                    print(f"[{current_time}] {Fore.GREEN}● {target_label} is ONLINE{Style.RESET_ALL}")
                    last_online_start = time.time()
                    await client.send_message('me', f"🟢 {target_label} появился в сети.")

                # ---> Переход в OFFLINE
                elif state == "Offline":
                    print(f"[{current_time}] {Fore.RED}○ {target_label} is OFFLINE {Style.RESET_ALL} | {status_text}")
                    
                    if last_online_start is not None:
                        session_duration = time.time() - last_online_start
                        
                        # Сообщение о длительности
                        duration_msg = f"⏱ Был в сети: {int(session_duration)} сек."
                        print(f"   └── {duration_msg}")
                        
                        # Проверка на микро-онлайн (< 12 сек)
                        if session_duration < 12:
                            alert = f"⚡ Микро-онлайн! {target_label} зашел на {round(session_duration, 1)} сек."
                            print(f"{Fore.YELLOW}{alert}{Style.RESET_ALL}")
                            await client.send_message('me', alert)
                        else:
                            await client.send_message('me', f"🔴 {target_label} вышел. {duration_msg}")
                        
                        last_online_start = None # Сброс таймера
                
                # Сохраняем текущее состояние как предыдущее
                previous_state = state
            
            # Если статус не менялся, просто ждем
            # Уменьшил задержку до 5 секунд для точности микро-онлайна
            await asyncio.sleep(5) 

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}🚨 Отслеживание остановлено пользователем.{Style.RESET_ALL}")
            break
