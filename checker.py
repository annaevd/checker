import sys
import io
import time
import requests
import urllib3
import json
from http.cookies import SimpleCookie

# Нормальный UTF-8 вывод в лог
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://bpmgob.mec.gub.uy/etapas/agenda_sae_api_disponibilidades"

# Cookie из браузера (только ASCII / percent-encoding)
COOKIE_RAW = (
    "target_bal=!km1r9LB0E4JRgkfTTujzigjbW3HXOKyI8aPoEqjHSGto8q/X6UqB1rL11wWJSYkwHGrLiwlPOB30cg==; "
    "simple_bpm_query=ZnJvbnRlbmQ%3D; "
    "simple_bpm_location=aHR0cHM6Ly9icG1nb2IubWVjLmd1Yi51eS90cmFtaXRlcy9kaXNwb25pYmxlcw%3D%3D; "
    "simple_bpm_login_cuenta_id=1; "
    "TS01d82af7=01f421a8d87cd47503004e1eadf87838ba059c8027a046e1b1ff0e53a054c6be779d0565e43120cac69af2c717c2885b69a7da3fa8; "
    "simple_bpm_session=cjd98oOLpmaKRTcwzrSp2H%2BiPPQCA%2B7PdCctDenR1eCXPsPzj%2BLmty8nrvrRVExhoQMq9%2FDzzQnmVPxjiTjvRwDuF49iArH6OvWLW5SSzpJwsGkdVE0Mw8YWBBHBxGU3KEMKD9xDOAHR4FtZx3uK1cQyXaqv%2BT936SclxSxiqjvT9JyPYi4dmUkGRt1kr1Aimn4S3g7bpN30hQf%2FQ9skXJzCsa0CDVd5u4O1GcTINv6tXyMtFZQfyDDF1%2BOtFYzonKJq5iPrECLnVJuDilaaAiV1smzfeOqv36CeyiSZ5k4pheDT9RKQTaHUBos9UpmD4ANZxHY8GY6vtR%2Bcf%2BQ%2BgtgiER9GV9SK4HnNzZI8I2BleZXbIMMjG%2FQ5R3wNgbzT%2Bmgk9dxg8h8MwXRCFw7v2YH9PxaNefXHMLhCA86JepTHMzJ1gG1pyD6sKJXrLKxZ3IPA3%2Bvfn4OBPpuMvoa7QTp9Y%2FaYu%2FulyL3vyyInLd5jXKm0DerSBat8yKaUQpYI7UL127g%2BbogjnoGiXdB04n2wb1DOjkfy%2B0dG0LyW29RUUOHLkHLMitTiKwb39H%2BC6jbPKv3lPV5eTdAyWHkkA%3D%3D13fa268f2bf04b9d9e3531ec013e09c4162ecaea; "
    "TS0191f197=01f421a8d8646634c941d42a3477b2d2b61c8af459a046e1b1ff0e53a054c6be779d0565e4bd7d99bf117920677bcb2a468550bd7e4da98c40d382e58fe92b3a29513acedb52e74467a25f5ce0a8f6f4ac87f080db; "
    "TS0191f197=018cd2258fb1355bfef6cf71371742ecd4365815baacade22a9328d5ead7ed86bba94ebb9ed20f47ca8c3f170827e30d64b0d978d9c514163310e46e101adf1a4d63d9979e65564e9ea24dee573f5423ca836171ae476f6b58c76ab3f061c19acf968e63e4; "
    "TS01d82af7=018cd2258f5cac424e21b1215ec05f710bd309c958acade22a9328d5ead7ed86bba94ebb9eaa7c6152d1ef5473842d7e82b52a9fc2; "
    "simple_bpm_session=tRJKetlYbIh7smrUH15fXcx4rKGeco3WmyRs8L%2BfsZzouGOToU54h4cI4qiE8MT%2FefCg0zqRhU1TdWjavsbfd7B2DRgAmVSDEAVUNGq9EbzYczm2wLTA67z49u0MR31XE3HOVCmkWUkj1nVKRxT63TsDC3oJw5QgE1fxhQAVKHuCHpa%2Fp3HvWa63C2E4vK1jlrFU51gxl2W1F4EwNV5CxVQK3VFTovMYXDeeU9alr0agZ5YQOlJ7JcJ8gyauq3c4MFIn6AYUn1BJmB5TFucf8ScU6WXLlMiMCoAzgqFkspGZoq0N%2BK%2Fobzi7Kkd7Xla6YIQTu3OOEDu8HVeOpklJadnbBIwMy%2FqdKG8qkAHW8UAsSQCwLJONIsuFo2GSmUtm30JATpFSym5iy0kgHeJd5oIleq6io8ObispJNYtHIoNs6ug013sMkwGf03B2YS33uWbG2NsRB6qbSQ9oY%2BG8g%2FudqlvTu7I9EXe01KMRen%2FUcDoYQPqh%2F9%2FW5gyewGHxaf030d22893d748062f8a847602f697531b98cf0; "
    "target_bal=!Rz3oe2yoTcefLI7TTujzigjbW3HXOD4PF9X7m1wXVRNiKAcXQEW5U9vgJD8zT08ww/Ko2TMIDAbmPA=="
)

# --- формируем cookie-jar ---
jar = requests.cookies.RequestsCookieJar()
c = SimpleCookie()
c.load(COOKIE_RAW)
for key in c.keys():
    jar.set(key, c[key].value)

HEADERS_BASE = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "ru,en-US;q=0.9,en;q=0.8,tr;q=0.7,es;q=0.6,el;q=0.5",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://bpmgob.mec.gub.uy",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

# ---------- ЗАПРОС #1 ----------
DATA_1 = {
    "method": "POST",
    "url": "https://sae.mec.gub.uy/sae-admin/rest/consultas/disponibilidades_por_recurso",
    "token": "OvJPbpQE/NVoj1D0bOsU0LlvHFh4oj3QjQ==",
    "id_empresa": "9",
    "id_agenda": "7",
    "id_recurso": "214",
    "idioma": "es",
}
REFERER_1 = "https://bpmgob.mec.gub.uy/etapas/ejecutar/296310/1"

# ---------- ЗАПРОС #2 ----------
DATA_2 = {
    "method": "POST",
    "url": "https://sae.mec.gub.uy/sae-admin/rest/consultas/disponibilidades_por_recurso",
    "token": "OvJPbpQE/NVoj1D0bOsU0LlvHFh4oj3QjQ==",
    "id_empresa": "9",
    "id_agenda": "82",
    "id_recurso": "213",
    "idioma": "es",
}
REFERER_2 = "https://bpmgob.mec.gub.uy/etapas/ejecutar/299903/1"

def send_one(name: str, referer: str, data: dict):
    headers = dict(HEADERS_BASE)
    headers["Referer"] = referer
    print(f"[{time.strftime('%H:%M:%S')}] [{name}] Старт запроса.")
    r = requests.post(URL, headers=headers, data=data, cookies=jar, timeout=40, verify=False)
    print(f"[{time.strftime('%H:%M:%S')}] [{name}] HTTP {r.status_code}")
    print(f"------ ОТВЕТ СЕРВЕРА ({name}) ------")
    print(r.text)
    print("------------------------------------")
    try:
        body = r.json()
        disp = body.get("disponibilidades")
        if isinstance(disp, list) and len(disp) > 0:
            print(f"[{time.strftime('%H:%M:%S')}] [{name}] ЕСТЬ свободные места: {len(disp)}")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] [{name}] Нет свободных мест.")
    except ValueError:
        print(f"[{time.strftime('%H:%M:%S')}] [{name}] Ответ не JSON.")

def main():
    send_one("REQ#1", REFERER_1, DATA_1)
    send_one("REQ#2", REFERER_2, DATA_2)

if __name__ == "__main__":
    main()
