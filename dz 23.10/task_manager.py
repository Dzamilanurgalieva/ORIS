import sys
import json
import os

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QRadioButton, QButtonGroup,
    QCheckBox, QPushButton, QListWidget, QDialog, QDialogButtonBox,
    QMessageBox
)
from PyQt6.QtCore import pyqtSignal

# Настройки пути к файлу
FOLDER_NAME = "dz 23.10"
DATA_FILE = os.path.join(FOLDER_NAME, "tasks.json")


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(300, 100)

        layout = QVBoxLayout(self)
        self.dark_theme_check = QCheckBox("Enable Dark Theme")
        layout.addWidget(self.dark_theme_check)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)


class TaskManagerWindow(QMainWindow):
    task_created = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager 2.0")
        self.resize(500, 600)

        self.tasks = []
        self.edit_index = -1
        self.load_json()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        main_layout.addWidget(QLabel("Task"))
        self.task_input = QLineEdit()
        main_layout.addWidget(self.task_input)

        main_layout.addWidget(QLabel("Description"))
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)
        main_layout.addWidget(self.desc_input)

        priority_layout = QHBoxLayout()
        self.radio_low = QRadioButton("Low")
        self.radio_medium = QRadioButton("Medium")
        self.radio_high = QRadioButton("High")
        self.radio_medium.setChecked(True)

        self.priority_group = QButtonGroup(self)
        self.priority_group.addButton(self.radio_low)
        self.priority_group.addButton(self.radio_medium)
        self.priority_group.addButton(self.radio_high)

        priority_layout.addWidget(self.radio_low)
        priority_layout.addWidget(self.radio_medium)
        priority_layout.addWidget(self.radio_high)
        main_layout.addLayout(priority_layout)

        self.check_important = QCheckBox("Important")
        self.check_send = QCheckBox("Send notification")
        main_layout.addWidget(self.check_important)
        main_layout.addWidget(self.check_send)

        btn_layout = QHBoxLayout()
        self.btn_create = QPushButton("Create task")
        self.btn_update = QPushButton("Save changes")
        self.btn_update.hide()
        self.btn_delete = QPushButton("Delete selected")
        self.btn_clear = QPushButton("Clear")
        self.btn_settings = QPushButton("Settings")

        btn_layout.addWidget(self.btn_create)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_settings)
        main_layout.addLayout(btn_layout)

        main_layout.addWidget(QLabel("Tasks list:"))
        self.tasks_list = QListWidget()
        main_layout.addWidget(self.tasks_list)

        self.status_label = QLabel("Status: Ready")
        main_layout.addWidget(self.status_label)

        self.btn_create.clicked.connect(self.create_task)
        self.btn_update.clicked.connect(self.update_task)
        self.btn_delete.clicked.connect(self.delete_selected_task)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_settings.clicked.connect(self.open_settings)
        self.tasks_list.itemClicked.connect(self.load_task_to_form)
        self.task_created.connect(self.on_task_created)

        self.refresh_list()

    def on_task_created(self, name):
        self.status_label.setText(f"Status: Task '{name}' created")

    def create_task(self):
        name = self.task_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Task name is required")
            return

        task = {
            "name": name,
            "desc": self.desc_input.toPlainText().strip(),
            "priority": self.get_priority(),
            "important": self.check_important.isChecked(),
            "send": self.check_send.isChecked()
        }

        self.tasks.append(task)
        self.save_json()
        self.refresh_list()
        self.task_created.emit(name)
        self.clear_form()

    def update_task(self):
        if self.edit_index == -1:
            return

        name = self.task_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Task name is required")
            return

        self.tasks[self.edit_index] = {
            "name": name,
            "desc": self.desc_input.toPlainText().strip(),
            "priority": self.get_priority(),
            "important": self.check_important.isChecked(),
            "send": self.check_send.isChecked()
        }
        self.save_json()
        self.refresh_list()
        self.status_label.setText("Status: Task updated")
        self.clear_form()

    def delete_selected_task(self):
        row = self.tasks_list.currentRow()
        if row == -1:
            QMessageBox.information(self, "Info", "Select a task to delete")
            return

        reply = QMessageBox.question(
            self, "Confirm", "Delete this task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            del self.tasks[row]
            self.save_json()
            self.refresh_list()
            self.status_label.setText("Status: Task deleted")
            self.clear_form()

    def load_task_to_form(self, item):
        row = self.tasks_list.row(item)
        task = self.tasks[row]

        self.task_input.setText(task["name"])
        self.desc_input.setPlainText(task["desc"])
        
        if task["priority"] == "Low": self.radio_low.setChecked(True)
        elif task["priority"] == "High": self.radio_high.setChecked(True)
        else: self.radio_medium.setChecked(True)

        self.check_important.setChecked(task["important"])
        self.check_send.setChecked(task["send"])

        self.edit_index = row
        self.btn_create.hide()
        self.btn_update.show()
        self.status_label.setText("Status: Editing task")

    def clear_form(self):
        self.task_input.clear()
        self.desc_input.clear()
        self.radio_medium.setChecked(True)
        self.check_important.setChecked(False)
        self.check_send.setChecked(False)
        
        self.edit_index = -1
        self.btn_create.show()
        self.btn_update.hide()

    def get_priority(self):
        if self.radio_low.isChecked(): return "Low"
        if self.radio_high.isChecked(): return "High"
        return "Medium"

    def refresh_list(self):
        self.tasks_list.clear()
        for i, t in enumerate(self.tasks, start=1):
            mark = "[!]" if t["important"] else ""
            self.tasks_list.addItem(f"{i}. [{t['priority']}] {t['name']} {mark}")

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            if dialog.dark_theme_check.isChecked():
                self.setStyleSheet(
                    "QWidget { background-color: #2b2b2b; color: #ffffff; }"
                    "QLineEdit, QTextEdit { background-color: #3c3f41; color: #ffffff; }"
                )
            else:
                self.setStyleSheet("")

    def load_json(self):
        if not os.path.exists(DATA_FILE):
            self.tasks = []
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except json.JSONDecodeError:
            print(f"Ошибка: файл {DATA_FILE} поврежден. Создан новый список.")
            self.tasks = []
        except Exception as e:
            print(f"Неизвестная ошибка при чтении: {e}")
            self.tasks = []

    def save_json(self):
        try:
            os.makedirs(FOLDER_NAME, exist_ok=True)
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить задачи:\n{e}")


def main():
    app = QApplication(sys.argv)
    window = TaskManagerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()