import tkinter as tk
from tkinter import messagebox
import os
import shutil
import winreg

# Получение информации о существующих томах в системе
drives = os.listdrives()
# Массив с именами копируемых пользовательских папок
folders = ['Видео', 'Документы', 'Загрузки', 'Изображения', 'Музыка', 'Рабочий стол']
regeditpatchs = ['My Video', '{35286A68-3C57-41A1-BBB1-0EAE73D76C95}',  # Видео
                 'Personal', '{F42EE2D3-909F-4907-8871-4C22FC0BF756}',  # Документы
                 '{374DE290-123F-4565-9164-39C4925E467B}', '{7D83EE9B-2244-4E70-B1F5-5393042AF1E4}',  # Загрузки
                 'My Pictures', '{0DDD015D-B06C-45D5-8C4C-F59713854639}',  # Изображения
                 'My Music', '{A0C69A99-21C8-4671-8703-7934162FCF1D}',  # Музыка
                 'Desktop', '{754AC886-DF64-4CBA-86B5-F7FBF4FBCEF5}']  # Рабочий стол


# Функция обработки кнопок в которую помещена лямбда
def warningmessage(driv):
    return lambda: warningmessagelambda(driv)


# Функция поиска расположения пользовательских папок в реестре
def regeditsearchfolders(folder1, folder2):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',
                             0, winreg.KEY_READ)
        key = winreg.QueryValueEx(key, folder1)
        return key[0]
    except OSError:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',
                                 0, winreg.KEY_READ)
            key = winreg.QueryValueEx(key, folder2)
            return key[0]
        except OSError:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders',
                                     0, winreg.KEY_READ)
                key = winreg.QueryValueEx(key, folder1)
                return key[0]
            except OSError:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                         r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders',
                                         0, winreg.KEY_READ)
                    key = winreg.QueryValueEx(key, folder2)
                    return key[0]
                except OSError:
                    print('Ключ реестра не найден')


# Функция, которую вызывает лямбда, тело программы после нажатия кнопок
def warningmessagelambda(dri):
    if messagebox.askyesno(title='Подтверждение операции',
                           message='Вы уверены что хотите выбрать диск ' + dri + '?'):
        print("!")
        # Поиск текущего расположения пользовательских папок через реестр
        iregeditpatchs = 0  # Итератор для перебора массива содержащего ключи реестра
        regeditpatchfolders = list()
        while iregeditpatchs < len(regeditpatchs):
            regeditpatchfolder = regeditsearchfolders(regeditpatchs[iregeditpatchs], regeditpatchs[iregeditpatchs + 1])
            regeditpatchfolders.append(regeditpatchfolder)
            iregeditpatchs += 2
        print(regeditpatchfolders)
        # Копирование пользовательских каталогов
        iregeditpatchs = 0
        for regeditpatchfolder in regeditpatchfolders:
            regeditpatchfolder = str(regeditpatchfolder)
            shutil.copytree(regeditpatchfolder, 'D:\\Mirror\\' + folders[iregeditpatchs], symlinks=False, ignore=None,
                            copy_function=shutil.copy2, ignore_dangling_symlinks=False,
                            dirs_exist_ok=True)
            iregeditpatchs += 1
        #  Необходимо добавить прогресс бар
    else:
        print('Пользователь нажал нет')


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

# Блок с текстом
messagetoadmin = tk.Label(
    master=frame,
    text='Выберите диск назначения (расположения пользовательских папок):',
    bg='black',
    fg='white',
    font='Courier 22'
)
messagetoadmin.pack(pady=20)

# Вывод кнопок с информацией о диске и его емкости
for drive in drives:
    drive = str(drive)
    try:
        diskresurse = shutil.disk_usage(drive)
        disktotal = str(round(diskresurse[0] / 1024 / 1024 * 0.000977))
        diskused = str(round(diskresurse[2] / 1024 / 1024 * 0.000977))
        buttoncontent = 'Диск ' + drive + ' (Использовано ' + diskused + 'ГБ из ' + disktotal + 'ГБ)'
        button = tk.Button(
            master=frame,
            text=buttoncontent,
            command=warningmessage(drive)
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
        disknone = 'Диск ' + str(drive) + ' (Нет накопителя)'
        button = tk.Button(
            master=frame,
            text=disknone,
            bg='black',
            fg='white',
            font='Courier 18',
            state='disabled',
            width=44
        )
        button.pack(pady=4)
frame.pack(expand=True)
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
