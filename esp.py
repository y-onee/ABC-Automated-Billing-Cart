import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import socket

ip = "192.168.240.200"    # IP Address of Host (Laptop)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Socket object
print("Waiting for Client!!")
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((ip, 8002))
s.listen()
conn, addr = s.accept()

prevMsg = "0%0"+"%0"+"%0\n"     # variable to store the msg that has been sent to the esp

cam = cv2.VideoCapture(1)
cam.set(3, 640)
cam.set(6, 480)

data = pd.read_csv("barcode.csv")

codes = data['code'].tolist()
prices = data['price'].tolist()
# names = data['name'].tolist()

while True:

    # myData = 400
    myData = 0
    success, img = cam.read()
    for barcode in decode(img):
        print(barcode.data)
        global msg
        myData = barcode.data.decode('utf-8')
        # print(myData)
        a = int(myData)    
    print(myData)
    msg = str(myData)
    prevMsg = msg
    conn.sendall(msg.encode())   # Sending the string using the socket connection

    s.close()
    cv2.imshow('Result', img)
    cv2.waitKey(10)    

    # conn.close() 
 
                
    