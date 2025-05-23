import os
import subprocess
import sys
import psycopg2
from PyQt6.QtWidgets import (
    QFileDialog,
    QApplication,
    QMainWindow,
    QColumnView,
    QDialog,
    QMessageBox,
)
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QPixmap
from PyQt6.uic import loadUi
from imbedCalc import *
from face_ext import *


class DatabaseReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI from a file
        loadUi("face-detection.ui", self)

        # Find the column view widget by its object name in the UI file
        self.column_view = self.findChild(QColumnView, "columnView")
        # Load data from the database
        self.load_data_from_db()
        # Add shortcuts
        self.actionRefresh.setShortcut("F5")
        self.actionAdd_person_to_DB.setShortcut("Ctrl+N")

        # Load Actions
        self.actionRefresh.triggered.connect(self.load_data_from_db)
        self.actionAdd_person_to_DB.triggered.connect(self.open_dialog)
        self.actionAbout_Face_Detection.triggered.connect(self.open_about_dialog)
        self.actionCompare_image_from_Camera.triggered.connect(self.compare_image)
        self.actionCompare_image_from_File.triggered.connect(self.compare_file)

    def open_dialog(self):
        # Create the dialog and display it
        dialog = FormDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Retrieve data from the dialog
            name = dialog.nameedit.text()
            date = dialog.dateedit.text()
            id = dialog.idedit.text()
            motherid = dialog.motheridedit.text()
            fatherid = dialog.fatheridedit.text()
            fathername = dialog.fathernameedit.text()
            mothername = dialog.mothernamedit.text()
            wait = InfoDialog(
                "Please Wait",
                "If Your OS give you a not responsing message click wait and ignore",
            )
            if (
                name != ""
                and date != ""
                and id != ""
                and motherid != ""
                and fatherid != ""
                and fathername != ""
                and mothername != ""
            ):
                wait.exec()
                cap = face_video(id)
                images = AddImagetoDB(
                    "techman",
                    "techman",
                    cap.frame,
                    name,
                    id,
                    date,
                    fatherid,
                    motherid,
                    fathername,
                    mothername,
                )
                wait.destroy()
            else:
                wait.destroy()
                errore = InfoDialog(
                    f"Unexpected Error", f"Make sure all fields are correct"
                )
                errore.exec()

    def open_about_dialog(self):
        dialog = AboutDialog()
        dialog.exec()

    def open_file_dialog(self):
        # Open file dialog to select images
        file_filter = "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", file_filter
        )
        if not (os.path.isdir(file_path)):
            return file_path
        else:
            err = InfoDialog(f"Unexcpected Error", "Please Select a proper image")
            err.exec()

    def compare_file(self):
        wait = InfoDialog(
            "Please Wait",
            "If Your OS give you a not responsing message click wait and ignore",
        )
        wait.exec()
        try:
            wait.destroy()
            file = self.open_file_dialog()
            wait.exec()
            if not os.path.isdir(file):
                calc = CalcImbed(file)
                searc = Search("techman", "techman", calc.embedding)
                wait.destroy()
            else:
                wait.destroy()
                err = InfoDialog(f"Unexcpected Error", "Please Select a proper image")
                err.exec()
        except IsADirectoryError:
            err = InfoDialog(f"Unexcpected Error", "Please Select a proper image")
            err.exec()

    def compare_image(self):
        wait = InfoDialog(
            "Please Wait",
            "If Your OS give you a not responsing message click wait and ignore",
        )
        wait.exec()
        cap = face_capture("temp")
        calc = CalcImbed(cap.image)
        searc = Search("techman", "techman", calc.embedding)
        wait.destroy(True)

    def load_data_from_db(self):

        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            user="techman",
            password="159357",
            host="localhost",
            port="5432",
        )
        cursor = connection.cursor()

        connection.commit()

        # Fetch data from the table
        cursor.execute(
            "SELECT id, name, date, fatherid, motherid, fathername, mothername FROM pictures"
        )
        rows = cursor.fetchall()

        # Prepare data for the column view
        model = QStandardItemModel()
        # Read Data
        for user_id, name, age, fatherid, motherid, fathername, mothername in rows:
            user_item = QStandardItem(f"ID: {user_id}")
            name_item = QStandardItem(f"Name: {name}")
            date_item = QStandardItem(f"Date of Birth: {age}")
            fatherid_item = QStandardItem(f"Father's ID: {fatherid}")
            motherid_item = QStandardItem(f"Mother's ID: {motherid}")
            fathername_item = QStandardItem(f"Father's name: {fathername}")
            mothername_item = QStandardItem(f"Mother's name: {mothername}")
            user_item.appendRow(name_item)
            user_item.appendRow(date_item)
            user_item.appendRow(fatherid_item)
            user_item.appendRow(motherid_item)
            user_item.appendRow(fathername_item)
            user_item.appendRow(mothername_item)
            model.appendRow(user_item)
            pixmap = QPixmap(f"stored-faces/{user_id}.jpg").scaled(
                300, 100, Qt.AspectRatioMode.KeepAspectRatio
            )
            photo = QStandardItem()
            photo.setData(pixmap, Qt.ItemDataRole.DecorationRole)
            name_item.appendRow(photo)
        # Set up the model for the column view
        self.column_view.setModel(model)
        # Close the database connection
        cursor.close()
        connection.close()


class FormDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog UI
        loadUi("dialogadd.ui", self)
        self.buttonsubmit.clicked.connect(self.accept)


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("about.ui", self)


# Run App
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = DatabaseReaderApp()
        window.show()
        sys.exit(app.exec())
    except psycopg2.OperationalError:
        os.system("PGDATA=/var/lib/data/ /usr/bin/pg_ctl start")
        window = DatabaseReaderApp()
        window.show()
        sys.exit(app.exec())
