# всякие импорты - система, интерфейс, дата, время, диалог, звуки, потоки

import os
from tkinter import *
import datetime
import time
from tkinter import filedialog, messagebox
import winsound
import threading


# класс - представление одного будильника
class AlarmEntry():
    def __init__(self, time, filename):
        self.time = time
        self.filename = filename


# список будильников
alarms = []


# функция для проигрывания 1 файла по имени
def play_sound(filename):
    winsound.PlaySound(filename, winsound.SND_ASYNC)
    pass


# флаг - нужно ли остановить фоновый поток
abort_background = False


# функция фоновой обработки
def background_work():
    global abort_background  # берём внешнюю переменную

    # пока не запрошена остановка
    # 3 раза в секунду проверяем равно ли текущее время какому-нибудь из будильников, и если да, запускаем файл
    while not abort_background:
        current_time = datetime.datetime.now()
        now = current_time.strftime("%H:%M:%S")
        i = 0
        while i < len(alarms):
            alarm = alarms[i]
            if alarm.time == now:
                play_sound(alarm.filename)
                alarms.pop(i)
                i -= 1
            i += 1
        time.sleep(0.3)


# формирование интерфейса
window = Tk()
window.title("Alarm Clock")
window.geometry("450x300")

# надписи времи
lblHour = Label(window, text="Час", font=12)
lblHour.grid(column=1, row=0)
lblMin = Label(window, text="Минуты", font=12)
lblMin.grid(column=2, row=0)
lblSec = Label(window, text="Секунды", font=12)
lblSec.grid(column=3, row=0)

# надпись - вопрос
setYourAlarm = Label(window, text="Во сколько вас разбудить?", fg="black", font=("Helvetica", 7, "bold"))
setYourAlarm.grid(column=0, row=1)

# переменные - контейнеры текущих введённых значений
enter_hour_val = StringVar(value=datetime.datetime.now().hour)
enter_min_val = StringVar(value=datetime.datetime.now().minute)
enter_sec_val = StringVar(value=datetime.datetime.now().second)
selected_file = StringVar()

# ввод времени
enter_hour = Entry(window, textvariable=enter_hour_val, bg="white", width=15)
enter_hour.grid(column=1, row=1)
enter_min = Entry(window, textvariable=enter_min_val, bg="white", width=15)
enter_min.grid(column=2, row=1)
enter_sec = Entry(window, textvariable=enter_sec_val, bg="white", width=15)
enter_sec.grid(column=3, row=1)


# функция - обработка создания нового будильника
def add_alarm():
    # проверяем выбранный файл
    if selected_file.get() == "":
        messagebox.showwarning("Ошибка", "Файл не выбран")
        return

    # строим строку выбранного времени
    selected_time_s = f"{enter_hour_val.get():2}:{enter_min_val.get():2}:{enter_sec_val.get():2}"

    # добавляем новый будильник
    alarms.append(AlarmEntry(selected_time_s, selected_file.get()))

    messagebox.showinfo("Успешно", f"Будильник установлен на {selected_time_s}")


# кнопка установить будильник
btn_set_alarm = Button(window, text="Установить будильник", fg="red", width=20, command=add_alarm)
btn_set_alarm.grid(column=1, row=4, columnspan=3)


# функция - обработка кнопки выбрать файл
def select_file():
    selected_file.set(
        filedialog.askopenfilename(
            # открываем выбор файла в текущей папке (os.getcwd())
            initialdir=os.getcwd(),
            # допускаем только .wav файлы, запятая в конце обязательна для формирования списка
            filetypes=(("Wav files", "*.wav"),)
        )
    )


# кнпока выбора файла
btn_select_file = Button(window, text="Выбрать файл", fg="red", width=20, command=select_file)
btn_select_file.grid(column=0, row=2, pady=10)

# текст - путь к выбранному файлу
enter_selected_file = Entry(window, textvariable=selected_file, state=DISABLED, bg="white", width=40)
enter_selected_file.grid(column=1, row=2, columnspan=3)

# запускаем фоновый поток обработки
thread = threading.Thread(target=background_work)
thread.start()

# запускаем окно
window.mainloop()

# когда окно закрылось, прерываем фоновое выполнение
abort_background = True

# ожидаем завершения фонового потока
thread.join()
