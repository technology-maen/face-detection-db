# importing the required libraries
from imgbeddings import imgbeddings
from PIL import Image
import psycopg2
import os

class calcNewImageImbed:
    def __init__(self, dbname, user):
        # connecting to the database - replace the SERVICE URI with the service URI
        conn = psycopg2.connect(f"dbname={dbname} user={user}")

        for filename in os.listdir("stored-faces"):
            # opening the image
            img = Image.open("preimages/" + filename)
            # loading the `imgbeddings`
            ibed = imgbeddings()
            # calculating the embeddings
            embedding = ibed.to_embeddings(img)
            cur = conn.cursor()
            cur.execute("INSERT INTO pictures values (%s,%s)", (filename, embedding[0].tolist()))
            print(filename)
        conn.commit()