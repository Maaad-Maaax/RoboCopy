import tkinter as tk
from tkinter import messagebox
import os
import shutil
import winreg
import tkinter.ttk as ttk

# Получение информации о существующих томах в системе
drives = os.listdrives()
# Массив с именами копируемых пользовательских папок
folders = ['Видео', 'Документы', 'Загрузки', 'Изображения', 'Музыка', 'Рабочий стол']
regedit_patch = ['My Video', '{35286A68-3C57-41A1-BBB1-0EAE73D76C95}',  # Видео
                 'Personal', '{F42EE2D3-909F-4907-8871-4C22FC0BF756}',  # Документы
                 '{374DE290-123F-4565-9164-39C4925E467B}', '{7D83EE9B-2244-4E70-B1F5-5393042AF1E4}',  # Загрузки
                 'My Pictures', '{0DDD015D-B06C-45D5-8C4C-F59713854639}',  # Изображения
                 'My Music', '{A0C69A99-21C8-4671-8703-7934162FCF1D}',  # Музыка
                 'Desktop', '{754AC886-DF64-4CBA-86B5-F7FBF4FBCEF5}']  # Рабочий стол


# Функция обработки кнопок в которую помещена лямбда
def warning_message(def_drive):
    return lambda: warning_message_lambda(def_drive)


# Функция поиска расположения пользовательских папок в реестре
def regedit_search_folders(regedit_patch_1, regedit_patch_2):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',
                             0, winreg.KEY_READ)
        key = winreg.QueryValueEx(key, regedit_patch_1)
        return key[0]
    except OSError:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',
                                 0, winreg.KEY_READ)
            key = winreg.QueryValueEx(key, regedit_patch_2)
            return key[0]
        except OSError:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders',
                                     0, winreg.KEY_READ)
                key = winreg.QueryValueEx(key, regedit_patch_1)
                return key[0]
            except OSError:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                         r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders',
                                         0, winreg.KEY_READ)
                    key = winreg.QueryValueEx(key, regedit_patch_2)
                    return key[0]
                except OSError:
                    print('Ключ реестра не найден')


# Функция, которую вызывает лямбда, тело программы после нажатия кнопок
def warning_message_lambda(def_lambda_drive):
    if messagebox.askyesno(title='Подтверждение операции',
                           message='Вы уверены что хотите выбрать диск ' + def_lambda_drive + '?'):
        # Поиск текущего расположения пользовательских папок через реестр
        counter_patch = 0  # Итератор для перебора массива содержащего ключи реестра
        regedit_patch_folders = list()
        while counter_patch < len(regedit_patch):
            regedit_patch_folder = regedit_search_folders(regedit_patch[counter_patch], regedit_patch[counter_patch+1])
            regedit_patch_folders.append(regedit_patch_folder)
            counter_patch += 2
        # Копирование пользовательских каталогов
        counter_patch = 0
        progress_bar['maximum'] = len(folders)
        for regedit_patch_folder in regedit_patch_folders:
            src = str(regedit_patch_folder)
            dst = 'D:\\Mirror\\' + folders[counter_patch]
            shutil.copytree(src, dst, symlinks=False, ignore=True,
                            copy_function=shutil.copy2, ignore_dangling_symlinks=False,
                            dirs_exist_ok=True)
            counter_patch += 1
            # Прогресс бар
            progress_bar['value'] += 1
            robocopy.update()


# Прорисовка графического интерфейса, создание окна приложения
robocopy = tk.Tk()
robocopy.title('RoboCopy 1.0')
robocopy.iconbitmap('RoboCopy.ico')

# Общий контейнер
frame = tk.Frame(
    robocopy,
    bg='black',
    padx=20,  # Задаём отступ по горизонтали.
    pady=20  # Задаём отступ по вертикали
)
frame.pack(expand=True)

# Блок с текстом
message_to_admin = tk.Label(
    master=frame,
    text='Выберите диск назначения (расположения пользовательских папок):',
    bg='black',
    fg='white',
    font='Courier 22'
)
message_to_admin.pack(pady=20)

# Вывод кнопок с информацией о диске и его емкости
for drive in drives:
    drive = str(drive)
    try:
        disk_resource = shutil.disk_usage(drive)
        disk_total = str(round(disk_resource[0] / 1024 / 1024 * 0.000977))
        disk_used = str(round(disk_resource[2] / 1024 / 1024 * 0.000977))
        button_content = 'Диск ' + drive + ' (Свободно ' + disk_used + 'ГБ из ' + disk_total + 'ГБ)'
        button = tk.Button(
            master=frame,
            text=button_content,
            command=warning_message(drive)
        )
        button.configure(
            bg='black',
            fg='white',
            font='Courier 18',
            cursor='hand2',
            width=44
        )
        button.pack(
            pady=4
        )
    except OSError:
        disk_none = 'Диск ' + str(drive) + ' (Нет накопителя)'
        button = tk.Button(
            master=frame,
            text=disk_none,
            bg='black',
            fg='white',
            font='Courier 18',
            state='disabled',
            width=44
        )
        button.pack(pady=4)

progress_bar = ttk.Progressbar(robocopy, orient="horizontal",
                               mode="determinate", maximum=6, value=0)
progress_bar.pack()

# Центровка окна программы посередине экрана
robocopy.update_idletasks()
s = robocopy.geometry()
s = s.split('+')
s = s[0].split('x')
width_root = int(s[0])
height_root = int(s[1])
w = robocopy.winfo_screenwidth()
h = robocopy.winfo_screenheight()
w = w // 2
h = h // 2
w = w - width_root // 2
h = h - height_root // 2
robocopy.geometry('+{}+{}'.format(w, h))
robocopy.resizable(width=False, height=False)
robocopy.mainloop()
