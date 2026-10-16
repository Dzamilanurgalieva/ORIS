# Task Manager (PyQt6)

Небольшое desktop-приложение для создания задач на Python с PyQt6

## Функционал

 Ввод названия задачи (QLineEdit)
 Ввод многострочного описания (QTextEdit)
 Выбор приоритета: Low / Medium / High, ровно один (QRadioButton)
 Дополнительные настройки: Important, Send notification (QCheckBox)
 Кнопка **Create task** - собирает данные из формы и выводит в консоль
 Проверка: если название пустое - задача не создаётся

## Виджеты
 QMainWindow, QWidget, QVBoxLayout, QHBoxLayout - каркас окна
 QLineEdit - название задачи
 QTextEdit - описание
 QRadioButton - выбор приоритета
 QCheckBox - независимые опции
 QPushButton- кнопка Create task
 QLabel - подписи

## Запуск

Если PyQt6 не установлен:
pip install PyQt6


Затем:
python task_manager.py