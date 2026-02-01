from telethon import events
from client import client
from tracker import run_tracker
import asyncio
from colorama import Fore, Style
from main import main

tracker_task = None


@client.on(events.NewMessage(outgoing=True, pattern=r'^/stop$'))
async def handler_stop(event):
    global tracker_task

    me = await client.get_me()

    if event.chat_id != me.id:
        return
    
    if tracker_task and not tracker_task.done():
        tracker_task.cancel()
        tracker_task = None
        print(f"{Fore.YELLOW}🚨 Трекер остановлен пользователем.{Style.RESET_ALL}")
        await event.reply("✅ Трекер остановлен.")

        await main()
    else:
        await event.reply("⚠️ Трекер не запущен.")


@client.on(events.NewMessage(outgoing=True, pattern=r'(?i)/getid'))
async def handler_getid(event):
    global tracker_task
    if event.is_private:
        target_id = event.chat_id
        user = await event.get_chat()
        
        target_label = f"{user.first_name} (@{user.username})" if user.username else user.first_name

        print(f"{Fore.CYAN}ℹ️ ID пользователя {target_label}: {target_id}{Style.RESET_ALL}")

        await client.send_message('me', f"ℹ️ ID пользователя {target_label}: {target_id}\n\n")

        await event.delete()

        if tracker_task and not tracker_task.done():
            return

        await main()

        # print(f"{Fore.GREEN}🚀 Запуск трекера для {target_label}...{Style.RESET_ALL}")
        # tracker_task = asyncio.create_task(run_tracker(str(target_id)))
    
    elif event.is_group:
        await event.reply("❌ Эта команда работает только в личных сообщениях.")
