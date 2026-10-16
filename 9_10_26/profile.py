import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton,
    QRadioButton, QCheckBox, QButtonGroup
)


class ProfileWindow(QWidget):#окно виджет
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Profile")
        self.resize(500, 600)

        
        main_layout = QVBoxLayout()#столбк

        
        title = QLabel("Create your profile")#просто надпись
        main_layout.addWidget(title)


        #кнопки с названием в одну строку и вложенные
        name_row = QHBoxLayout()
        name_label = QLabel("Name:")
        #self - чтобы можно было поизменять потом
        self.name_edit = QLineEdit()
        self.name_edit.setText("Катя")
        name_row.addWidget(name_label)
        name_row.addWidget(self.name_edit)
        main_layout.addLayout(name_row)
    
        age_row = QHBoxLayout()
        age_label = QLabel("Age:")
        self.age_edit = QLineEdit()
        self.age_edit.setText("29")
        age_row.addWidget(age_label)
        age_row.addWidget(self.age_edit)
        main_layout.addLayout(age_row)


        
        main_layout.addWidget(QLabel("Work format:"))

        work_row = QHBoxLayout()#в строку
        #взаимоисключающие кнопки
        self.radio_office = QRadioButton("Office")
        self.radio_remote = QRadioButton("Remote")
        self.radio_hybrid = QRadioButton("Hybrid")
        self.radio_remote.setChecked(True)   

       
        self.work_group = QButtonGroup(self)
        self.work_group.addButton(self.radio_office)
        self.work_group.addButton(self.radio_remote)
        self.work_group.addButton(self.radio_hybrid)

        work_row.addWidget(self.radio_office)
        work_row.addWidget(self.radio_remote)
        work_row.addWidget(self.radio_hybrid)
        main_layout.addLayout(work_row)



        #ufkjxrf
        self.notify_check = QCheckBox("Receive notifications")
        self.notify_check.setChecked(True)#по умолчанию
        main_layout.addWidget(self.notify_check)

        



        main_layout.addWidget(QLabel("About:"))
        self.about_edit = QTextEdit()
        self.about_edit.setPlainText("I'm a teacher.")
        main_layout.addWidget(self.about_edit)



      #запуск
        self.create_btn = QPushButton("Create profile")
        self.create_btn.clicked.connect(self.on_create)#запуск при клике
        main_layout.addWidget(self.create_btn)




        
        main_layout.addWidget(QLabel("Result:"))
        self.result_view = QTextEdit()
        self.result_view.setReadOnly(True)  #неизменяемый пользоваелеем 
        main_layout.addWidget(self.result_view)

        
        self.setLayout(main_layout)



    def on_create(self):
        name = self.name_edit.text().strip()#читает имя и убирает пробелы
        age = self.age_edit.text().strip()


        #взаимоисключающие кнопки
        if self.radio_office.isChecked():
            work_format = "Office"
        elif self.radio_remote.isChecked():
            work_format = "Remote"
        else:
            work_format = "Hybrid"

        #Переводит тру и фалс в ес и ноу
        notifications = "Yes" if self.notify_check.isChecked() else "No"

        #доп текст
        about = self.about_edit.toPlainText().strip()

        result = (
            f"Name: {name}\n"
            f"Age: {age}\n"
            f"Work format: {work_format}\n"
            f"Notifications: {notifications}\n"
            f"\n"
            f"About:\n"
            f"{about}"
        )
        #в результ
        self.result_view.setPlainText(result)


def main():
    app = QApplication(sys.argv)
    window = ProfileWindow()
    window.show()
    sys.exit(app.exec())#hf,jnftn gjrf gjkmpjdfntkm yt pfrhjtn jryj


if __name__ == "__main__":
    main()