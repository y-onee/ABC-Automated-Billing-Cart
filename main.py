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

cam = cv2.VideoCapture(1)
cam.set(3, 640)
cam.set(6, 480)

bar_arr = []

data = pd.read_csv("barcode.csv")

codes = data['code'].tolist()
prices = data['price'].tolist()
names =  data['title'].tolist()

p_arr = []
items = {}

total = 0

print("Press Ctrl+C to generate the final bill.")

def add(i):
    global total
    p_arr.append(prices[i])
    if names[i] not in items:
        items.update({names[i]: [1, prices[i], prices[i]]})
    else:
        val = items[names[i]][0]
        tot = (items[names[i]][0]+1)*items[names[i]][1]
        items.update({names[i]: [val+1, prices[i], tot]})
    total = sum(p_arr)

def delete(i):
    global total
    print(prices[i])
    total = sum(p_arr) - prices[i] 
    p_arr.remove(prices[i])
    if items[names[i]][0] == 1:
        items.pop(names[i])
    else:
        val = items[names[i]][0]
        tot = items[names[i]][2] - items[names[i]][1]
        items.update({names[i]: [val-1, prices[i], tot]})

def bill():
    print()
    print(" ".ljust(84, "_"))
    print("|".ljust(0), "|".rjust(83))
    print("|".ljust(0), "-- BILL --".center(77), "|".rjust(5))
    print("|".ljust(0), "|".rjust(83))
    print("|".ljust(3), "".center(77, "-"), "|".rjust(3))
    print("|    ", "Item".ljust(10), "Price".center(20), "Quantity".center(30), "Total".rjust(10), "    |")
    print("|".ljust(3), "".center(77, "-"), "|".rjust(3))
    print("|".ljust(0), "|".rjust(83))
    for i in items:
        print("|    ", str(i).ljust(10),  str(items[i][1]).center(20), str(items[i][0]).center(30), str(items[i][2]).rjust(10), "    |")
    print("|".ljust(3), "".center(77, "-"), "|".rjust(3))
    print("|    ", "".ljust(10), "".center(20), "".center(10), "Amount:".ljust(20), str(total).rjust(10), "   |", )
    print("|    ", "".ljust(10), "".center(20), "".center(10), "Tax:".ljust(20), str(round(0.18*total, 3)).rjust(10),"   |")
    print("|".ljust(47), "".center(33, "-"), "|".rjust(3))
    print("|    ", "".ljust(10), "".center(20), "".center(10), "Total Cost:".ljust(20), str(round(total+0.18*total, 3)).rjust(10),"   |")
    print("|".ljust(0), "|".rjust(83))
    # print("|".ljust(0), "|".rjust(83))
    print("|", "".center(81, "_"), "|")
    print()    

try:
    while conn:
        success, img = cam.read()
        for barcode in decode(img):
            # print(barcode.data)
            myData = barcode.data.decode('utf-8')
            print(myData)
            a = int(myData)
            for code in codes:
                if a == code:
                    ind = codes.index(code)
                    print("Item: ", names[ind])
                    print("Price: ", prices[ind])
            if int(myData) not in bar_arr:
                print('Do you want to add the item?')
                n = input()
                if n == 'Y' or n == 'y':
                    a = int(myData)
                    bar_arr.append(int(myData))
                    for code in codes:
                        if a == code:
                            add(codes.index(code))
                    bill() 
                            # print("for loop 1")
                            
            else:
                print('Want to repeat the item or delete it? (R/D)')
                n = input()
                if n == 'R' or n == 'r':
                    a = int(myData)
                    bar_arr.append(int(myData))
                    for code in codes:
                        if a == code:
                            add(codes.index(code))    
                    bill()
                            # print("For loop 2")    

                elif n == 'D' or n == 'd':    
                    a = int(myData)
                    bar_arr.remove(int(myData))
                    for code in codes:
                        if a == code:
                            delete(codes.index(code))
                    bill()
                
                else:
                    break

            # cv2.imshow('Result', img)
            cv2.waitKey(10)
            # print("Total before sendall", total)

            msg = str(round(total+total*0.18, 3))
            prevMsg = msg
                    
            conn.sendall(msg.encode())   # Sending the string using the socket connection
except KeyboardInterrupt:
    print("Final Bill:")
    bill()