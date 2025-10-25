import sys
import io
import time
import requests
import urllib3

# Нормальный UTF-8 вывод в лог
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://bpmgob.mec.gub.uy/etapas/agenda_sae_api_disponibilidades"

# Минимальные «нейтральные» заголовки (без Referer/Origin/Accept-Language/Connection/кук)
HEADERS_BASE = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",  # оставляем, т.к. у тебя в рабочем curl он есть
}

# ---------- ЗАПРОС #1 (agenda=82, recurso=213) ----------
DATA_1 = {
    "method": "POST",
    "url": "https://sae.mec.gub.uy/sae-admin/rest/consultas/disponibilidades_por_recurso",
    "token": "OvJPbpQE/NVoj1D0bOsU0LlvHFh4oj3QjQ==",
    "id_empresa": "9",
    "id_agenda": "82",
    "id_recurso": "213",
    "idioma": "es",
}

# ---------- ЗАПРОС #2 (agenda=7, recurso=214) ----------
DATA_2 = {
    "method": "POST",
    "url": "https://sae.mec.gub.uy/sae-admin/rest/consultas/disponibilidades_por_recurso",
    "token": "OvJPbpQE/NVoj1D0bOsU0LlvHFh4oj3QjQ==",
    "id_empresa": "9",
    "id_agenda": "7",
    "id_recurso": "214",
    "idioma": "es",
}

def send_one(name: str, data: dict):
    headers = dict(HEADERS_BASE)
    print(f"[{time.strftime('%H:%M:%S')}] [{name}] Старт запроса.")
    try:
        r = requests.post(
            URL,
            headers=headers,
            data=data,
            timeout=40,
            verify=False,          # игнорируем проблемный сертификат
            allow_redirects=False, # не следуем редиректам внутри одного вызова
            cookies=None           # явная гарантия: куки не отправляем
        )
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] [{name}] Ошибка запроса: {e}")
        return

    print(f"[{time.strftime('%H:%M:%S')}] [{name}] HTTP {r.status_code}")
    print(f"------ ОТВЕТ СЕРВЕРА ({name}) ------")
    print(r.text)
    print("------------------------------------")

    # Разбор JSON и вывод результата
    try:
        body = r.json()
    except ValueError:
        print(f"[{time.strftime('%H:%M:%S')}] [{name}] Ответ не JSON.")
        return

    disp = body.get("disponibilidades")
    if isinstance(disp, list) and len(disp) > 0:
        print(f"[{time.strftime('%H:%M:%S')}] [{name}] ЕСТЬ свободные места: {len(disp)}")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] [{name}] Нет свободных мест.")

def main():
    send_one("REQ#1 agenda=82 recurso=213", DATA_1)
    send_one("REQ#2 agenda=7 recurso=214",  DATA_2)

if __name__ == "__main__":
    main()
