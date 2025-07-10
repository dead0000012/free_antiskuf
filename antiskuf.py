import winsound
import time
import win32api
import pyttsx3
import threading
import ctypes
import os
import shutil
import sys


def add_to_startup():
    startup = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    script = os.path.abspath(sys.argv[0])
    target = os.path.join(startup, os.path.basename(script))
    if not os.path.exists(target):
        shutil.copy(script, target)

add_to_startup()

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

VK_CONTROL = 0x11
VK_F6 = 0x75
last_pos = win32api.GetCursorPos()

def reminder_loop(interval_sec):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    while True:
        time.sleep(interval_sec)
        for e in range(3):
            winsound.Beep(1000, 1000)
        time.sleep(1)
        engine.say("Прошло два часа. Сделай перерыв или разминку.")
        engine.runAndWait()

# Запускаем таймер в отдельном потоке
timer_thread = threading.Thread(target=reminder_loop, args=(2 * 60 * 60,), daemon=True)
timer_thread.start()

while True:
    hour = int(time.strftime("%H"))
    minut = int(time.strftime("%M"))

    if hour == 9 and minut < 5:
        for i in range(5):
            time.sleep(1)
            winsound.Beep(5000, 1000)
        engine.say("ПРИВЕТ — Это программа — АНТИСКУФ — сейчас 9 утра — пора завтракать!")
        engine.runAndWait()

    if hour == 12 and minut <= 10:
        current_pos = win32api.GetCursorPos()
        if current_pos != last_pos:
            winsound.Beep(4000, 1000)
        else:
            engine.setProperty('rate', 250)
            engine.say("Вставай — обедать!")
            engine.runAndWait()

        last_pos = current_pos

    if hour == 17 and minut < 10:
        for i in range(5):
            time.sleep(0.5)
            winsound.Beep(4000, 1000)
        engine.say("Эй - Надо - поужинать")
        engine.runAndWait()

    if hour == 22 and minut > 10:
        os.system("shutdown /s /t 60 /c \"Выключение через 1 минуту. Сохрани всё!\"")

    if hour == 17 and minut <= 10 or hour == 9 and minut <= 5:
        ctypes.windll.user32.BlockInput(True)
    else:
        ctypes.windll.user32.BlockInput(False)

    if (win32api.GetAsyncKeyState(VK_CONTROL) & 0x8000) and (win32api.GetAsyncKeyState(VK_F6) & 0x8000):
        break

    time.sleep(1)