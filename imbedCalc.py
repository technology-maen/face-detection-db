# importing the required libraries
import cv2
from imgbedding import imgbedding
from PIL import Image
import psycopg2
import os
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class InfoDialog(QDialog):
    def __init__(self, title: str, message: str):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedSize(300, 150)  # Set a fixed size for the dialog

        # Main layout
        layout = QVBoxLayout()

        # Add message label
        label = QLabel(message)
        label.setWordWrap(True)  # Enable text wrapping
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Add Close button
        close_button = QPushButton("OK")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        # Set layout
        self.setLayout(layout)

class AddImagetoDBFromFolder:
    def __init__(self, dbname, user, folder):
        # connecting to the database - replace the SERVICE URI with the service URI
        conn = psycopg2.connect(f"dbname={dbname} user={user}")

        for filename in os.listdir(folder):
            # opening the image
            img = Image.open(folder + filename)
            # loading the `imgbeddings`
            ibed = imgbedding()
            # calculating the embeddings
            embedding = ibed.to_embeddings(img)
            cur = conn.cursor()
            name = input("Enter Name for image: ")
            try:
                cur.execute(
                    "INSERT INTO pictures values (%s,%s)", (name, embedding[0].tolist())
                )
            except psycopg2.errors.UniqueViolation:
                print(f"{filename} exists")
            print(filename)
        conn.commit()


class AddImagetoDB:
    def __init__(
        self,
        dbname,
        user,
        img,
        name,
        ID,
        bday,
        fatherid,
        motherid,
        mothername,
        fathername,
    ):
        # connecting to the database - replace the SERVICE URI with the service URI
        conn = psycopg2.connect(f"dbname={dbname} user={user}")
        # loading the `imgbeddings`
        ibed = imgbedding()
        # calculating the embeddings
        embedding = ibed.to_embeddings(img)
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO pictures values (%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    name,
                    embedding[0].tolist(),
                    ID,
                    bday,
                    fatherid,
                    motherid,
                    mothername,
                    fathername,
                ),
            )
        except psycopg2.errors.UniqueViolation:
            print(f"{name} already exists")
            pass
        conn.commit()


class CalcImbed:
    def __init__(self, img):
        ibed = imgbedding()
        embedding = ibed.to_embeddings(img)
        self.embedding = embedding


class Search:
    def __init__(self, dbname, user, embedding):
        conn = psycopg2.connect(f"dbname={dbname} user={user}")
        cur = conn.cursor()
        string_representation = (
            "[" + ",".join(str(x) for x in embedding[0].tolist()) + "]"
        )
        cur.execute(
            "SELECT * FROM pictures ORDER BY embedding <-> %s LIMIT 1;",
            (string_representation,),
        )
        rows = cur.fetchall()
        for row in rows:
            dialog = InfoDialog(f"Found {row[0]}",f"Who's ID is {row[2]}. and father's name is {row[7]} and mother's name is {row[6]} and his father's ID is {row[5]} and his mother's ID is {row[4]}")
            dialog.exec()
            print(
                f"Found {row[0]}. Who's ID is {row[2]}. and father's name is {row[7]} and mother's name is {row[6]} and his father's ID is {row[5]} and his mother's ID is {row[4]}"
            )
            cv2.imshow("Image", cv2.imread(f"stored-faces/{row[0]}.jpg"))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        cur.close()
