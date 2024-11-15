# importing the required libraries
import cv2
from imgbeddings import imgbeddings
from PIL import Image
import psycopg2
import os

from transformers.models.cvt.convert_cvt_original_pytorch_checkpoint_to_pytorch import embeddings


class AddImagetoDBFromFolder:
    def __init__(self, dbname, user, folder):
        # connecting to the database - replace the SERVICE URI with the service URI
        conn = psycopg2.connect(f"dbname={dbname} user={user}")

        for filename in os.listdir(folder):
            # opening the image
            img = Image.open(folder + filename)
            # loading the `imgbeddings`
            ibed = imgbeddings()
            # calculating the embeddings
            embedding = ibed.to_embeddings(img)
            cur = conn.cursor()
            name = input("Enter Name for image: ")
            try:
                cur.execute("INSERT INTO pictures values (%s,%s)", (name, embedding[0].tolist()))
            except psycopg2.errors.UniqueViolation:
                print(f'{filename} exists')
            print(filename)
        conn.commit()

class AddImagetoDB:
    def __init__(self, dbname, user, img, name):
        # connecting to the database - replace the SERVICE URI with the service URI
        conn = psycopg2.connect(f"dbname={dbname} user={user}")
        # loading the `imgbeddings`
        ibed = imgbeddings()
        # calculating the embeddings
        embedding = ibed.to_embeddings(img)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO pictures values (%s,%s)", (name, embedding[0].tolist()))
        except psycopg2.errors.UniqueViolation:
            print(f'{name} already exists')
            pass
        conn.commit()

class CalcImbed:
    def __init__(self, img):
        ibed = imgbeddings()
        embedding = ibed.to_embeddings(img)
        self.embedding = embedding

class Search:
    def __init__(self, dbname, user, embedding):
        conn = psycopg2.connect(f"dbname={dbname} user={user}")
        cur = conn.cursor()
        string_representation = "["+ ",".join(str(x) for x in embedding[0].tolist()) +"]"
        cur.execute("SELECT * FROM pictures ORDER BY embedding <-> %s LIMIT 1;", (string_representation,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
            cv2.imshow('Image',cv2.imread(f"stored-faces/{row[0]}.jpg"))
        cur.close()
