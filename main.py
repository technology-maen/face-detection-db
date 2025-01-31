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
from PyQt6.QtGui import QStandardItem, QStandardItemModel
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
        self.actionAdd_person_to_DB.triggered.connect(self.open_dialog)
        self.actionAbout_Face_Detection.triggered.connect(self.open_about_dialog)
        self.actionComparehaguihaghamhamazachi
        hamzh_image_from_Camera.triggered.connect(self.compare_image)
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
            cap = face_video(id)
            images = AddImagetoDB(
                "techman",
                "techman",
                cap.frame,
                name,
                id,
                "18/11/2008",
                fatherid,
                motherid,
                mothername,
                fathername,
            )

    def open_about_dialog(self):
        dialog = AboutDialog()
        dialog.exec()

    def open_file_dialog(self):
        # Open file dialog to select images
        file_filter = "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", file_filter
        )
        return file_path

    def compare_file(self):
        file = self.open_file_dialog()
        calc = CalcImbed(file)
        searc = Search("techman", "techman", calc.embedding)

    def compare_image(self):
        cap = face_capture("temp")
        calc = CalcImbed(cap.image)
        searc = Search("techman", "techman", calc.embedding)

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
        for user_id, name, age, fatherid, motherid, fathername, mothername in rows:
            user_item = QStandardItem(f"ID: {user_id}")
            name_item = QStandardItem(f"Name: {name}")
            # date_item = QStandardItem(f"Date of Birth: {age}")
            fatherid_item = QStandardItem(f"Father's ID: {fatherid}")
            motherid_item = QStandardItem(f"Mother's ID: {motherid}")
            fathername_item = QStandardItem(f"Father's name: {fathername}")
            mothername_item = QStandardItem(f"Mother's name: {mothername}")
            user_item.appendRow(name_item)
            # user_item.appendRow(date_item)
            user_item.appendRow(fatherid_item)
            user_item.appendRow(motherid_item)
            user_item.appendRow(fathername_item)
            user_item.appendRow(mothername_item)
            model.appendRow(user_item)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseReaderApp()
    window.show()
    sys.exit(app.exec())
