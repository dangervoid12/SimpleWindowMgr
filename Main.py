from SimpleWindowMgr import SimpleWindowMgr
import sys

version = "1.0"


def display_help():
    print("Simple Window Manager")
    print(version)
    print("lpkkk")
    print("")
    print("###################################################################################")
    print("####                                                                           ####")
    print("####     This program work as a simple window manager                          ####")
    print("####                 for Windows operating systems                             ####")
    print("####                                                                           ####")
    print("####         Usage:                                                            ####")
    print("####     python simpleWindowMgr.py function windowName param1 param2           ####")
    print("####                                                                           ####")
    print("####     Functions:                                                            ####")
    print("####         min-name    : minimize window with given name                     ####")
    print("####         max-name    : maximize window with given name                     ####")
    print("####         rest-name   : restore window with given name                      ####")
    print("####         res-name    : resize window with given name                       ####")
    print("####         move-name   : move window with given name                         ####")
    print("####                                                                           ####")
    print("####         min-prefix  : minimize window where name starts with prefix       ####")
    print("####         max-prefix  : maximize window where name starts with prefix       ####")
    print("####         rest-prefix : restore window where name starts with prefix        ####")
    print("####         res-prefix  : resize window where name starts with prefix         ####")
    print("####         move-prefix : move window where name starts with prefix           ####")
    print("####                                                                           ####")
    print("###################################################################################")


if __name__ == '__main__':
    app = SimpleWindowMgr()
    func = None
    try:
        func = sys.argv[1]
        name = sys.argv[2]
    except:
        print("Not enough arguments found")

    print("length: " + str(len(sys.argv)))
    if(len(sys.argv) > 3):
        if sys.argv[3] is not None:
            first_param = sys.argv[3]
        if sys.argv[4] is not None:
            second_param = sys.argv[4]

    if(func is not None):
        if(func == "min-name"):
            app.minimize_full_name(name)
        elif(func == "max-name"):
            app.maximize_full_name(name)
        elif(func == "rest-name"):
            app.restore_full_name(name)
        elif(func == "res-name"):
            app.resize_full_name(name, first_param, second_param)
        elif(func == "move-name"):
            app.move_full_name(name, first_param, second_param)
        elif(func == "min-prefix"):
            app.minimize_startswith_name(name)
        elif(func == "max-prefix"):
            app.maximize_startswith_name(name)
        elif(func == "rest-prefix"):
            app.restore_startswith_name(name)
        elif(func == "move-prefix"):
            app.move_startswith_name(name, first_param, second_param)
        elif (func == "help"):
            display_help()




    #minimize_full_name("Untitled - Notepad")
    #maximize_full_name("Untitled - Notepad")
    #restore_full_name("Untitled - Notepad")
    #resize_full_name("Untitled - Notepad", 500,500)
    #move_full_name("Untitled - Notepad", 500, 500)


    #minimize_startswith_name("Untitled")
    #maximize_startswith_name("Untitled")
    #restore_startswith_name("Untitled")
    #resize_startswith_name("Untitled", 500, 500)
    #move_startswith_name("Untitled", 500, 500)

