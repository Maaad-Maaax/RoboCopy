Данное программное обеспечение разработано для системных администраторов. ПО позволяет повысить уровень сохранности пользовательских данных на рабочих станциях с несколькими устройствами хранения. По умолчанию пользовательские данные хранятся на том же носителе, что и операционная система. Данное ПО позволяет переместить пользовательские папки на отличный от системного накопитель, приоритетным следует выбирать устройство типа HDD.
Алгоритм работы:
-	Выбор диска будущего расположения пользовательских папок, программа в корневой директории выбранного диска создаст каталог Mirror со следующими вложениями, повторяющими пользовательские: Видео, Документы, Загрузки, Изображения, Музыка, Рабочий стол. Если каталог Mirror уже существует, программа завершит свою работу;
-	Далее программа осуществит копирование аналогичных пользовательских директорий, поиск текущего их расположения осуществляется через реестр Windows, по окончанию копирования вносятся соответствующие правки ключей реестра отвечающих за их расположение, на новые значения;
-	По окончанию копирования будет предложено удалить прежние файлы, по старому расположению. В случае согласия генерируется Dell_bat.bat файл помещаемый в автозагрузку, который сработает только один раз, сотрет данные по прежнему расположению и сам себя уничтожит;
-	В целях усиления сохранности данных, дополнительно программа генерирует в корне выбранного диска, RoboCopy_start.bat файл, содержащий команды резервного копирования пользовательских папок на диск с операционной системой. В планировщике Windows формируется задача, ежедневно в 12:00, которая будет обращаться к RoboCopy_start.bat файлу, для резервного копирования;
-	Для применения изменений и удаления прежних данных потребуется перезагрузка, что далее будет предложено.
