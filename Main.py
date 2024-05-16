import tkinter as tk
from PIL import ImageGrab, Image, ImageTk
import os

import pytesseract
import easyocr

from pystray import MenuItem as item
import pystray
import json

import threading
import time

import pyautogui

from Server.libs.VariableMgr import VariableMgr
from Server.libs.MyVariable import MyVariable
from Server.libs.LinkServer import LinkServer
from SettingsWindow import SettingsWindow

####################################################### GLOBAL VAR
intervalMarker = False
app = None
varDB = None
general_refresh_interval = 1000
general_pick_res = None
server = None


class SoftMapper:
    def __init__(self, root):

        self.root = root
        self.root.title("Image Editor")
        self.rect_start = None
        self.rect_end = None
        self.img_ref = None  # Image reference
        self.reader = easyocr.Reader(['en'])

        self.temp_dir = os.path.join(os.path.expanduser('~'), 'temp')
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

    def parseMsgNew(self, msg):
        try:
            print("Msg to parse: " + msg)
            res = "-1"
            msg_arr = msg.split(":")
            msgFunction = msg_arr[0]
            msgData = msg_arr[1]
            if(msgFunction == "GetValueOf"): #todo tutaj skonczylem, tesseract nie dziala, nie wiem czemu
                for tmpVar in varDB:
                    if(tmpVar.Name == msgData):
                        #res = self.extractTextTesseract(os.path.join(self.temp_dir, tmpVar.Name + ".jpg"))
                        res = self.extractTextEasyocr(os.path.join(self.temp_dir, tmpVar.Name + ".jpg"))

                        #res = str(tmpVar.getValue())
                        if res == "":
                            res = "Found empty"
                        break
            elif(msgFunction == "ClickOn"):
                for tmpVar in varDB:
                    if(tmpVar.Name == msgData):
                        clickOnMiddle(tmpVar.X, tmpVar.Y, tmpVar.Width, tmpVar.Height)
                        res = "Clicked on: " + tmpVar.Name
                        break
            else:
                print("Function not found: " + msgFunction)
            server.sendServer(res)
        except Exception as e:
            print("Parser Error1:", e)


    def parseMsg(self, msg):
        loadVariablesDB()
        res = "-1"
        msg_arr = msg.split(":")
        print("parser " + str(len(msg_arr)) + " varDb size: " + str(len(varDB)))
        if len(msg_arr) > 1:
            sel_function = msg_arr[0]
            sel_data = msg_arr[1]
            if sel_function == "GetVariable":
                try:
                    varNo = int(sel_data)
                    res = varDB[varNo].getValue()
                    print("uu:" + str(varNo) )
                except:
                    res = "Error in command: " + msg
            elif sel_function == "GetVariableByName":
                varName = sel_data
                for singleVar in varDB:
                    if(singleVar.Name == varName):
                        res = singleVar.getValue()
                        if res == "":
                            print("found empty")
                            #res = "Variable found but empty"
                            res = " "
                            printAllVarDB()
                        else:
                            print("Found: " + res)
                        break
                    else:
                        res = "Error: Variable not found: " + msg
            elif sel_function == "ClickButton":
                try:
                    buttonNo = int(sel_data)
                    clickOnMiddle(varDB[buttonNo].X, varDB[buttonNo].Y, varDB[buttonNo].Width, varDB[buttonNo].Height)
                    res = "Button " + str(buttonNo) + " clicked"
                except:
                    res = "Error in command: " + msg
            elif sel_function == "ClickButtonByName":
                buttonName = sel_data
                i = 0
                while i < len(varDB):
                    if(varDB[i].Name == buttonName):
                        buttonNo = i
                        clickOnMiddle(varDB[buttonNo].X, varDB[buttonNo].Y, varDB[buttonNo].Width,
                                      varDB[buttonNo].Height)
                        res = "Button " + str(buttonNo) + " clicked"
                    i = i + 1
            else:
                print("else")
                res = "-1"
        print("ress: " + res)
        server.sendServer(res)

    def printAllVarDB(self):
        for tmpvar in varDB:
            print(tmpvar)

    def draw_rectangle(self, event):
        if self.rect_start is None:
            self.rect_start = (event.x, event.y)
        else:
            self.rect_end = (event.x, event.y)
            cut_rectangle_path = os.path.join(self.temp_dir, "cut_rectangle.jpg")
            screenshot = ImageGrab.grab()
            screenshot.crop((self.rect_start[0], self.rect_start[1], self.rect_end[0], self.rect_end[1])).save(
                cut_rectangle_path)
            self.label.config(text="Rectangle cropped and saved at " + cut_rectangle_path)
            self.rect_start = None
            self.rect_end = None

    def take_full_screen_screenshot(self):
        screenshot = ImageGrab.grab()
        temp_path = os.path.join(os.path.expanduser('~'), 'temp')
        screenshot_path = os.path.join(temp_path, "screenshot.jpg")
        screenshot.save(screenshot_path)
        #icon.update_menu()
        # showLastScreenshot()
        extractPieces(varDB)
        self.load_cut_rectangle(temp_path, varDB)
        #print("takeScreen")

    def extractTextEasyocr(self, imgpath):
        res = "-1"
        try:
            img = Image.open(imgpath)
            result = self.reader.readtext(img)
            print("raw Res: " + str(result))
            if not(str(result) == "[]"):
                print("Result: " + str(result[0][1]))
                res = "easy:" + str(result[0][1])
            else:
                res = "tes:" + self.extractTextTesseract(imgpath)
                #if(res == ""):
                #    res = "Nothing detected in: " + imgpath
        except Exception as e:
            print("Extraction Error: " + str(e))
        return res

    def extractTextTesseract(self, imgpath):
        res = "-1"
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        print("imgpath: " + imgpath)
        try:
            res = pytesseract.image_to_string(Image.open(imgpath))
            if (res == ""):
                img = Image.open(imgpath)
                img.convert("L")
                width, height = img.size
                img = img.resize((width * 3, height * 3))
                res = pytesseract.image_to_string(img)
        except Exception as e:
            print("Extracting Text error: " + e)
        print("return: " + res)



    def load_cut_rectangle(self, temp_path, varDB):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

        i = 0
        while i < len(varDB):
            cut_rectangle_path = os.path.join(temp_path, varDB[i].Name + ".jpg")
            try:
                extracted_text = pytesseract.image_to_string(Image.open(cut_rectangle_path))
                #print("Extracted[" + str(i) + "]=" + extracted_text)
                varDB[i].setValue(extracted_text)
            except FileNotFoundError:
                print("Cut Rectangle not found." + cut_rectangle_path)
            i = i + 1
        VariableMgr.setVarDB(self, varDB)


def extractPieces(varDB):
    for rect in varDB:
        cutPiece(rect.Name, rect.X, rect.Y, rect.Width, rect.Height)


def loadVariablesDB():
    global general_refresh_interval
    global general_pick_res
    global varDB
    with open('Server/config.json', 'r') as file:
        data = json.load(file)
    general_refresh_interval = data["General"]["Refresh interval"]
    general_pick_res = data["General"]["Pick resolution"]

    # Create an array of MyVariable objects using the data from the JSON
    my_variable_objects = []
    for var_data in data.get('VariableDB', []):
        my_var = MyVariable(var_data['Name'], var_data['Type'], var_data['X'], var_data['Y'], var_data['Width'],
                            var_data['Height'])
        my_variable_objects.append(my_var)
    varDB = my_variable_objects
    return my_variable_objects


def cutPiece(name, x, y, width, height):
    temp_path = os.path.join(os.path.expanduser('~'), 'temp')
    screenshot_path = os.path.join(temp_path, "screenshot.jpg")
    img = Image.open(screenshot_path)
    piece = img.crop((x, y, x + width, y + height))
    piecePath = os.path.join(temp_path, name + ".jpg")
    piece.save(piecePath)


def showLastScreenshot():
    screenshot_path = os.path.join(os.path.expanduser('~'), 'temp', "screenshot.jpg")
    img_window = tk.Toplevel()
    img_window.title("Screenshot")

    img = Image.open(screenshot_path)
    img.thumbnail((1080, 720))  # Resize the image to fit within the window
    img = ImageTk.PhotoImage(img)
    label = tk.Label(img_window, image=img)
    label.image = img  # Keep a reference to the image
    label.pack()
    # app.img_ref = img  # Set the reference in the class instance
    img_window.mainloop()


def startBackground():
    global intervalMarker
    print("Start Bg")
    intervalMarker = True


def stopBackground():
    global intervalMarker
    print("Stop Bg")
    intervalMarker = False


def startServer():
    global server
    server = LinkServer(app, "FirstServ", "192.168.0.2", "5055")
    #server = LinkServer(app, "FirstServ", "127.0.0.1", "5055")
    server.createServer()
    server.listenServer()


def stopServer():
    server.stopListeningServer()




def open_settings(icon, item):
    # Add code to open the settings window
    settings_root = tk.Tk()  # Create a new Tk() instance for settings window
    settings_app = SettingsWindow(settings_root, app)  # Initialize the SettingsWindow
    settings_root.mainloop()  # Start the main loop for settings window


def runAtInterval():
    while True:
        if (intervalMarker == True):
            loadVariablesDB()
            app.take_full_screen_screenshot()
        time.sleep(general_refresh_interval/1000)


def clickOnMiddle(x, y, width, height):
    newX = x + (width / 2)
    newY = y + (height /2)
    pyautogui.moveTo(newX, newY, duration=0)
    pyautogui.click()


def clickOn(x, y):
    pyautogui.moveTo(x, y, duration=0)
    pyautogui.click()


def main():
    global app
    global intervalMarker
    global varDB
    intervalMarker = True
    varDB = loadVariablesDB()
    print("int:" + str(general_refresh_interval))
    root = tk.Tk()
    app = SoftMapper(root)
    root.withdraw()  # Hide the main window initially
    startThreads()
    menu = (item('Take Screenshot', app.take_full_screen_screenshot),
            item('Start', startBackground),
            item('Stop', stopBackground),
            item('Start server', startServer),
            item('Stop server', stopServer),
            item('Settings', open_settings))
    icon = pystray.Icon("name", Image.open("Server/img/icon.png"), "SoftMapper", menu)  # Update icon path here
    icon.run()

    root.mainloop()


def startThreads():
    grabThread = threading.Thread(target=runAtInterval)
    grabThread.start()
    serverThread = threading.Thread(target=startServer)
    serverThread.start()


if __name__ == "__main__":
    main()
