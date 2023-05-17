import serial

DATA_AMOUNT = 1

global mainlist
mainlist = []
for i in range(0, DATA_AMOUNT):
    mainlist.append(i)

def main():

    arduinoMega = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

    while True:
        try:
            tempdata = arduinoMega.readline().decode('utf-8').split()
            mainlist = tempdata
            if not mainlist:
                pass
            else:
                print(f"Main List: {mainlist} | Filtered Distance: {mainlist[1]}")
        except Exception as e:
            print(f"Error: {e}")

    
if __name__ == '__main__': 
    main() 