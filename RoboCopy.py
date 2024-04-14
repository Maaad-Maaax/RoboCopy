from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter
import shutil
import winreg
import os
import sys

"""Конфигурация"""

drives = os.listdrives()  # Получение информации о существующих томах в системе
# Названия копируемых пользовательских папок
folders = ['Видео', 'Документы', 'Загрузки', 'Изображения', 'Музыка', 'Рабочий стол']
# Названия параметров реестра отвечающих за расположение данных пользовательских папок
regedit_patch = ['My Video', '{35286A68-3C57-41A1-BBB1-0EAE73D76C95}',  # Видео
                 'Personal', '{F42EE2D3-909F-4907-8871-4C22FC0BF756}',  # Документы
                 '{374DE290-123F-4565-9164-39C4925E467B}', '{7D83EE9B-2244-4E70-B1F5-5393042AF1E4}',  # Загрузки
                 'My Pictures', '{0DDD015D-B06C-45D5-8C4C-F59713854639}',  # Изображения
                 'My Music', '{A0C69A99-21C8-4671-8703-7934162FCF1D}',  # Музыка
                 'Desktop', '{754AC886-DF64-4CBA-86B5-F7FBF4FBCEF5}']  # Рабочий стол
destination_folder = "Mirror"  # Название новой корневой папки для пользовательских данных

"""Блок функций"""


# Лямбда-функция, обработки кнопок (главная)
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


#  Функция изменения параметров ключей реестра отвечающих за расположение пользовательских папок
def wr_regedit_patch(wr_branch, wr_key, wr_parameter, wr_value_key):
    wr_keys = winreg.OpenKey(wr_branch, wr_key, 0, winreg.KEY_ALL_ACCESS)  # Открыть ключ
    if wr_key == r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders':
        try:
            winreg.QueryValueEx(wr_keys, wr_parameter)  # Существует ли параметр
            winreg.SetValueEx(wr_keys, wr_parameter, 0, winreg.REG_SZ, wr_value_key)  # Изменить значение параметра
            #  print(f'Найден {wr_branch} + {wr_key} + {wr_parameter}')
        except FileNotFoundError:
            print(f'Не найден {wr_branch} + {wr_key} + {wr_parameter}')
    if wr_key == r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders':
        try:
            winreg.QueryValueEx(wr_keys, wr_parameter)  # Существует ли параметр
            winreg.SetValueEx(wr_keys, wr_parameter, 0, winreg.REG_EXPAND_SZ, wr_value_key)
            #  print(f'Найден {wr_branch} + {wr_key} + {wr_parameter}')
        except FileNotFoundError:
            print(f'Не найден {wr_branch} + {wr_key} + {wr_parameter}')
    winreg.CloseKey(wr_keys)


# Функция - тело программы, которую вызывает лямбда-функция
def warning_message_lambda(def_lambda_drive):
    if messagebox.askyesno(title='Подтверждение операции',
                           message='Вы уверены что хотите выбрать диск ' + def_lambda_drive + '?'):
        # Поиск текущего расположения пользовательских папок через реестр
        counter_patch = 0  # Итератор для перебора массива содержащего ключи реестра
        regedit_patch_folders = list()
        while counter_patch < len(regedit_patch):
            regedit_patch_folder = regedit_search_folders(regedit_patch[counter_patch],
                                                          regedit_patch[counter_patch + 1])
            regedit_patch_folders.append(regedit_patch_folder)  # Массив содержащий текущие пути
            counter_patch += 2
        # Создание нового дерева каталогов
        root = os.path.join(def_lambda_drive, destination_folder)
        if not os.path.isdir(root):
            os.mkdir(root)
            # print(f'Папка {root} создана!')
        else:
            showwarning = str("Диск " + "'" + def_lambda_drive + "'" + " уже содержит пользовательские данные!"
                                                                       "\n" + "'" + root + "'" + " уже существует!")
            messagebox.showwarning("Внимание", showwarning)
            sys.exit()
        i_new_folders = 0
        while i_new_folders < len(folders):
            stat_folder_to = regedit_patch_folders[i_new_folders]
            stat_folder_do = os.path.join(root, folders[i_new_folders])
            if not os.path.isdir(stat_folder_do):
                # Создание новой папки и копирование метаданных исходной
                os.mkdir(stat_folder_do)
                shutil.copystat(stat_folder_to, stat_folder_do)
                # print(f'Папка {stat_folder_do} создана!')
            #  else:
            # print(f'Папка {stat_folder_do} уже существует!')
            i_new_folders += 1

        # Подсчет максимального значения прогресс бара
        number_of_roots = 0
        for regedit_patch_folder in regedit_patch_folders:  # Перебор директорий и подсчет вложений (файлы, папки)
            number_of_roots += len(os.listdir(regedit_patch_folder))
            # print(f'Папка {regedit_patch_folder} содержит {len(os.listdir(regedit_patch_folder))} объектов')

        # Копирование пользовательских каталогов и обновление прогресс бара
        progress_bar['maximum'] = number_of_roots  # Максимальное значение прогресс бара
        copy_i = 0
        while copy_i < len(regedit_patch_folders):
            root_folder_to = os.path.join(def_lambda_drive, destination_folder, folders[copy_i])
            for file in os.listdir(regedit_patch_folders[copy_i]):
                regedit_patch_folder = regedit_patch_folders[copy_i]
                if os.path.isfile(os.path.join(regedit_patch_folder, file)):  # Если это файл то
                    file_do = os.path.join(regedit_patch_folder, file)
                    file_to = os.path.join(root_folder_to, file)
                    percent_bar = str(round(progress_bar['value'] / progress_bar['maximum'] * 100))  # % прогресса
                    patch_info = '|' + percent_bar + '%|...копирование файла ' + '\'' + file_do + '\'' + '\n'
                    scr.insert(1.0, patch_info)
                    if not os.path.isfile(file_to):  # Если этого файла нет в конечной папке
                        # print(f'Копирование файла {file_do}')
                        # Информация о копирование
                        shutil.copy2(file_do, file_to, follow_symlinks=False)
                        progress_bar['value'] += 1
                        robocopy.update()
                        # print(f'Файл {file_do} скопирован!')
                    else:
                        patch_info = ('|' + percent_bar + '%|' + ' Warning: Файл \'' + str(file_to)
                                      + '\' уже существует\n')
                        scr.insert(1.0, patch_info)
                        progress_bar['maximum'] -= 1  # Уменьшаем размер пр-бара, поскольку пропущен был файл
                if os.path.isdir(os.path.join(regedit_patch_folder, file)):  # Если это папка то
                    folder_do = os.path.join(regedit_patch_folder, file)
                    folder_to = os.path.join(root_folder_to, file)
                    # print(f'Копирование директории {folder_do}')
                    # Информация о копирование
                    percent_bar = str(round(progress_bar['value'] / progress_bar['maximum'] * 100))  # % прогресса
                    patch_info = '|' + percent_bar + '%|...копирование директории ' + '\'' + folder_do + '\'' + '\n'
                    scr.insert(1.0, patch_info)
                    try:
                        shutil.copytree(folder_do, folder_to, symlinks=True, ignore=None,
                                        copy_function=shutil.copy2, dirs_exist_ok=False, ignore_dangling_symlinks=True)
                    except FileExistsError:
                        patch_info = ('|' + percent_bar + '%|' + ' Warning: Директория \'' + str(folder_to)
                                      + '\' уже существует\n')
                        scr.insert(1.0, patch_info)
                    progress_bar['value'] += 1
                    robocopy.update()
                    # print(f'Папка {folder_do} скопирована!')
            copy_i += 1
        scr.insert(1.0, '|100%|...success full!\n')

        # Правка реестра
        # Параметры записи реестра
        i_wr_regedit_patch = 0  # Итератор для перебора параметров реестра
        wr_branch = winreg.HKEY_CURRENT_USER
        wr_key1 = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        wr_key2 = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'
        # Изменение параметров реестра
        for folder in folders:
            # Значение параметра ключа реестра
            wr_value_key = os.path.join(def_lambda_drive, destination_folder, folder)
            # Ключ Shell Folders, человеко читаемые параметры
            wr_parameter = regedit_patch[i_wr_regedit_patch]
            wr_regedit_patch(wr_branch, wr_key1, wr_parameter, wr_value_key)
            # Ключ Shell Folders, человеко не читаемые параметры
            wr_parameter = regedit_patch[i_wr_regedit_patch + 1]
            wr_regedit_patch(wr_branch, wr_key1, wr_parameter, wr_value_key)
            # Ключ User Shell Folders, человеко читаемые параметры
            wr_parameter = regedit_patch[i_wr_regedit_patch]
            wr_regedit_patch(wr_branch, wr_key2, wr_parameter, wr_value_key)
            # Ключ User Shell Folders, человеко не читаемые параметры
            wr_parameter = regedit_patch[i_wr_regedit_patch + 1]
            wr_regedit_patch(wr_branch, wr_key2, wr_parameter, wr_value_key)
            i_wr_regedit_patch += 2
        #  Добавление задачи планировщика, для копирования на системный диск пользовательских данных
        #  Создание .bat файла
        # Содержимое bat файла
        bat_content = "robocopy " + def_lambda_drive + destination_folder + " C:\\" + destination_folder + " /MIR"
        # bat будет создан на выбранном пользователем диске
        bat_path = os.path.join(def_lambda_drive, 'RoboCopy_start.bat')
        if not os.path.isfile(bat_path):
            with open(bat_path, 'w+', encoding='utf-8') as bat:
                bat.write(bat_content)
                bat.close()
            #  Объявление задачи, для планировщика windows на исполнение bat файла
            cmd_bat = 'SchTasks /Create /SC DAILY /TN "RoboCopy" /TR ' + bat_path + ' /ST 12:00'
            #  Кодировка терминала python
            os.system("chcp 65001 > nul")
            #  Исполнение задачи через интерфейс командной строки
            os.system(cmd_bat)

        #  Удаление файлов предыдущего расположения расположению
        if messagebox.askyesno(title='Подтверждение операции',
                               message='Операция успешно завершена! \n\n'
                                       'Удалить данные предыдущего расположения?'):
            #  Создание bat файла в автозагрузке на удаление старых директорий и самого себя
            bat_file = 'Dell_bat.bat'
            bat_path = 'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
            bat_way = os.path.join('C:\\',
                                   os.environ['homepath'],
                                   bat_path,
                                   bat_file)  # bat будет в папке автозагрузки
            top = "@echo off\nchcp 65001>nul \n"
            bat_content_del = ""
            for regedit_patch_folder in regedit_patch_folders:
                bat_content_del = bat_content_del + "RD /S /Q \"" + regedit_patch_folder + "\"\n"  # Содержимое bat
            bat_content_del = top + bat_content_del + "start /b \"\" cmd /c del \"%~f0\"&exit /b"
            if not os.path.isfile(bat_way):
                with open(bat_way, 'w+', encoding='utf-8') as bat:
                    bat.write(bat_content_del)
            bat.close()

        #  Перезагрузка ПК
        if messagebox.askyesno(title='Подтверждение операции',
                               message='Требуется перезагрузка ОС.\n Перезагрузить сейчас?'):
            os.system("shutdown /r /t 0")


"""Отрисовка графического интерфейса библиотекой tkinter"""
robocopy = tkinter.Tk()  # Объявление окна приложения
robocopy.title('RoboCopy 1.0')  # Заголовок окна приложения
robocopy.iconbitmap('RoboCopy.ico')  # ICO приложения
robocopy.attributes('-alpha', 0.875)  # Задание прозрачности окна приложения

# Главный контейнер
frame = tkinter.Frame(
    robocopy,
    bg='black',  # Фон окна приложения
    padx=20,  # Задаём отступ по горизонтали
    pady=20  # Задаём отступ по вертикали
)
frame.pack(expand=True)  # Позиционирование главного контейнера

# Блок с текстом расположенный под заголовком
message_to_admin = tkinter.Label(
    master=frame,
    text='Выберите диск назначения (расположения пользовательских папок):',
    bg='black',
    fg='white',
    font='Courier 22'
)
message_to_admin.pack(pady=20)

# Вывод кнопок с информацией о диске и его емкости
for drive in drives:  # Перебор массива хранящего информацию о дисках
    drive = str(drive)
    #  Обработка исключения вызываемого при отсутствии дискового накопителя
    try:
        disk_resource = shutil.disk_usage(drive)  # Считывание емкости диска
        disk_total = str(round(disk_resource[0] / 1024 / 1024 * 0.000977))  # Общая емкость
        disk_free = str(round(disk_resource[2] / 1024 / 1024 * 0.000977))  # Свободно на диске
        button_content = 'Диск ' + drive + ' (Свободно ' + disk_free + 'ГБ из ' + disk_total + 'ГБ)'
        button = tkinter.Button(
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
        button = tkinter.Button(
            master=frame,
            text=disk_none,
            bg='black',
            fg='white',
            font='Courier 18',
            state='disabled',  # Кнопка не активна
            width=44
        )
        button.pack(pady=4)

# Поле вывода информации о копируемых файлах
scr = Text(robocopy,
           height=2,
           font=('Courier', 10),
           bg='black',
           fg='white',
           wrap="word",
           padx=10,
           pady=5,
           bd=0
           )
scr.pack(
    fill=BOTH
)

# Прогресс бар
progress_bar = ttk.Progressbar(robocopy,
                               orient="horizontal",
                               mode="determinate",
                               value=0,
                               length=1117
                               )
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
robocopy.resizable(width=False, height=False)  # Запретить пользователю изменять размеры
robocopy.mainloop()
