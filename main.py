from face_ext import *
from imbedCalc import *


def main():
    filename = input("Enter Name For image: ")
    cap = face_capture(filename)
    images = AddImagetoDB('techman','techman', cap.image, filename)
    calc = CalcImbed(cap.image)
    searc = Search('techman','techman',calc.embedding)
if __name__ == '__main__':
    main()