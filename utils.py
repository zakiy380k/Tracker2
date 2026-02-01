from client import client
from config import LOCAL_TZ, UTC_TZ

from telethon.tl.types import UserStatusOnline, UserStatusOffline, UserStatusRecently

async def resolve_target(target_input):
    try: 
        if target_input.isdigit():
            return await client.get_entity(int(target_input))
        target_input = target_input.lstrip('@')
        return await client.get_entity(target_input)
    except Exception as e:
        print(f'❌ Ошибка при поиске: {e}')
        return None
    

def convert_utc_to_local(utc_dt):
    """Конвертирует UTC datetime в локальное время."""
    if utc_dt.tzinfo is None or utc_dt.tzinfo.utcoffset(utc_dt) is None:
        utc_dt = UTC_TZ.localize(utc_dt)
    return utc_dt.astimezone(LOCAL_TZ)

def format_status(entity):
    """Анализирует статус и возвращает читаемую строку и тип статуса."""
    try:
        status = entity.status
        
        if isinstance(status, UserStatusOnline):
            # expires - это время, когда статус "Online" истечет (обычно +5 мин от активности)
            return "Online", "Online"
            
        elif isinstance(status, UserStatusOffline):
            local_was_online = convert_utc_to_local(status.was_online)
            time_str = local_was_online.strftime('%H:%M:%S')
            return f"Offline (был: {time_str})", "Offline"
            
        elif isinstance(status, UserStatusRecently):
            return "Offline (был недавно)", "Offline"
            
        elif status is None:
            return "Hidden/Unknown", "Unknown"
        else:
            return f"Status: {type(status).__name__}", "Unknown"

    except Exception as e:
        return f"Error: {e}", "Error"
