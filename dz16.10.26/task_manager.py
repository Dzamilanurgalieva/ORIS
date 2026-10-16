import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QRadioButton, QButtonGroup,
    QCheckBox, QPushButton,
)


class TaskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Manager")
        self.resize(500, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        task_label = QLabel("Task")
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Введите название задачи")
        main_layout.addWidget(task_label)
        main_layout.addWidget(self.task_input)

        description_label = QLabel("Description")
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Опишите задачу")
        main_layout.addWidget(description_label)
        main_layout.addWidget(self.description_input)

        priority_label = QLabel("Priority")
        main_layout.addWidget(priority_label)

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
        self.check_send_notification = QCheckBox("Send notification")
        main_layout.addWidget(self.check_important)
        main_layout.addWidget(self.check_send_notification)

        self.create_button = QPushButton("Create task")
        self.create_button.clicked.connect(self.on_create_task)
        main_layout.addWidget(self.create_button)

    def on_create_task(self):
        task_name = self.task_input.text().strip()

        if not task_name:
            print("[!] Task name is required")
            return

        description = self.description_input.toPlainText().strip()

        if self.radio_low.isChecked():
            priority = "Low"
        elif self.radio_medium.isChecked():
            priority = "Medium"
        else:
            priority = "High"

        important = "Yes" if self.check_important.isChecked() else "No"
        send_notification = "Yes" if self.check_send_notification.isChecked() else "No"

        print("=== New task ===")
        print(f"Task:               {task_name}")
        print(f"Description:        {description}")
        print(f"Priority:           {priority}")
        print(f"Important:          {important}")
        print(f"Send notification:  {send_notification}")


def main():
    app = QApplication(sys.argv)
    window = TaskManagerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()