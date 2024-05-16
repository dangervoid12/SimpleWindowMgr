import tkinter as tk
from tkinter import ttk, simpledialog
import json
import os
from PIL import Image, ImageTk, ImageGrab
import time

class SettingsWindow:
    def __init__(self, root, app):
        self.scrollbar = None
        self.height_entry = None
        self.width_entry = None
        self.y_entry = None
        self.x_entry = None
        self.name_entry = None
        self.right_frame = None
        self.add_window = None
        self.rect_y = None
        self.rect_height = None
        self.rect_x = None
        self.rect_width = None
        self.start_y = None
        self.start_x = None
        self.cancel_button = None
        self.select_button = None
        self.combo = None
        self.combo_var = None
        self.canvas = None
        self.img_window = None
        self.tree = None
        self.img = None
        self.screenshot_path = None
        self.root = root
        self.root.title("Settings")
        self.root.geometry("700x400")  # Set window size
        self.temp_dir = os.path.join(os.path.expanduser('~'), 'temp')
        self.app = app

        with open('Server/config.json') as json_file:  # Updated path to config.json
            config = json.load(json_file)
            self.general_options = config['General']
            self.variable_db = config['VariableDB']

        self.create_ui()

    def create_ui(self):
        # Left side with a list of settings groups
        left_frame = tk.Frame(self.root, width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        groups_list = tk.Listbox(left_frame)
        groups_list.pack(fill=tk.BOTH, expand=1)
        groups_list.insert(tk.END, "General")
        groups_list.insert(tk.END, "VariableDB")

        # Right side for displaying settings
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Function to display settings based on the selected group
        def display_settings(event):
            selection = groups_list.curselection()
            if not selection:
                selected = 1
            else:
                selected = groups_list.get(selection)

            if selected == "General":
                self.display_general_settings()
            elif selected == "VariableDB":
                self.display_variable_db_settings()

        groups_list.bind('<<ListboxSelect>>', display_settings)

    def display_general_settings(self):
        # Clear existing widgets
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Iterate over General settings and display them
        row = 0
        for setting, value in self.general_options.items():
            label = tk.Label(self.right_frame, text=setting + ":")
            label.grid(row=row, column=0, sticky="e")

            entry = tk.Entry(self.right_frame)
            entry.insert(0, value)
            entry.grid(row=row, column=1)

            row += 1

    def display_variable_db_settings(self):
        # Clear existing widgets
        for widget in self.right_frame.winfo_children():
            widget.destroy()


        tree_frame = tk.Frame(self.right_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)


        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Type", "X", "Y", "Width", "Height"), show="headings")
        self.tree.heading("Name", text="Name" )
        self.tree.heading("Type", text="Type")
        self.tree.heading("X", text="X")
        self.tree.heading("Y", text="Y")
        self.tree.heading("Width", text="Width")
        self.tree.heading("Height", text="Height")

        for i in range(6):
            tmpW = 50
            if( i == 0):
                tmpW = 120
            self.tree.column(i, stretch=True, width=tmpW, minwidth=40)  # Adjust column width

        self.populate_treeview()


        
        self.scrollbar = tk.Scrollbar(tree_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        # Add "Add" and "Delete" buttons below the Treeview
        # add_button = tk.Button(tree_frame, text="Add", command=self.add_variable_window)
        add_button = tk.Button(self.right_frame, text="Add", command=self.pick_rectangle)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self.right_frame, text="Delete", command=self.delete_variable)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

    def populate_treeview(self):
        for var in self.variable_db:
            self.tree.insert("", tk.END, values=(var['Name'], var['Type'], var['X'], var['Y'], var['Width'], var['Height']))

        # Select the first row after populating the tree
        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[0])

    # Inside the SettingsWindow class:

    def showLastScreenshot(self):
        self.screenshot_path = os.path.join(os.path.expanduser('~'), 'temp', "screenshot.jpg")

        def transformX(valX):
            #valX = valX * 1.78 #for res 1920x1080
            return valX

        def transformY(valY):
            #valY = valY * 1.78
            return valY

        def add_new_variable(newname):
            selected_type = self.combo_var.get()
            new_variable = {'Name': newname, 'Type': selected_type,
                            'X': transformX(self.rect_x), 'Y': transformY(self.rect_y),
                            'Width': transformX(self.rect_width),
                            'Height': transformY(self.rect_height)}
            self.variable_db.append(new_variable)
            self.update_variable_db_json()  # Save changes to the JSON file
            self.update_treeview()
            self.img_window.destroy()

        def prompt_for_name():
            name = simpledialog.askstring("Input", "Enter variable name:")
            if name:
                add_new_variable(name)

        def start_fullscreen(self):
            self.state = True  # Just toggling the boolean
            self.img_window.attributes("-fullscreen", self.state)
            return "break"

        def end_fullscreen(self):
            self.state = False
            self.img_window.attributes("-fullscreen", False)
            return "break"

        img = ImageGrab.grab()
        #img.thumbnail((1920, 1080))  # Resize the image to fit within the window
        self.img = ImageTk.PhotoImage(img)

        self.img_window = tk.Toplevel()
        self.img_window.title("Screenshot")
        self.state = True
        self.img_window.bind("<Escape>", lambda event: self.img_window.attributes("-fullscreen", False))  # Press Escape to exit fullscreen

        self.canvas = tk.Canvas(self.img_window, width=self.img.width(), height=self.img.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.start_rect)
        self.canvas.bind("<B1-Motion>", self.draw_rect)

        self.combo_var = tk.StringVar()
        self.combo = ttk.Combobox(self.img_window, textvariable=self.combo_var, values=["1-Input", "2-Button"])
        self.combo.current(0)  # Set default selection
        self.combo.pack(side=tk.LEFT, padx=5, pady=5)
        self.combo.place(relx=0.43, rely=0.1, anchor="center")

        self.select_button = tk.Button(self.img_window, text="Select", command=prompt_for_name)
        #self.select_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.select_button.place(relx=0.5, rely=0.1, anchor="center")

        self.cancel_button = tk.Button(self.img_window, text="Cancel", command=self.img_window.destroy)
        #self.cancel_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.cancel_button.place(relx=0.53, rely=0.1, anchor="center")
        start_fullscreen(self)

    def start_rect(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def draw_rect(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        self.canvas.delete("rect")  # Clear previous rectangles
        self.canvas.create_rectangle(self.start_x, self.start_y, x, y, outline="red", tags="rect")

        # Print rectangle positions
        if self.start_x and self.start_y:
            self.rect_x = self.start_x
            self.rect_y = self.start_y
            self.rect_width = 0
            if self.rect_x < x:
                self.rect_width = x - self.rect_x
            else:
                self.rect_width = self.rect_x - x
                self.rect_x = x
            if self.rect_y < y:
                self.rect_height = y - self.rect_y
            else:
                self.rect_height = self.rect_y - y
                self.rect_y = y

            #print("Rectangle Coordinates:", (self.start_x, self.start_y, x, y))
            #print("Rec: x: " + str(self.rect_x) + " y: " + str(self.rect_y) + " w: " + str(self.rect_width) + " h: " + str(self.rect_height))

    def pick_rectangle(self):
        self.root.iconify()
        time.sleep(1)
        self.showLastScreenshot()

    def add_variable_window(self):
        self.add_window = tk.Toplevel()
        self.add_window.title("Add Variable")

        tk.Label(self.add_window, text="Name:").grid(row=0, column=0)
        tk.Label(self.add_window, text="X:").grid(row=1, column=0)
        tk.Label(self.add_window, text="Y:").grid(row=2, column=0)
        tk.Label(self.add_window, text="Width:").grid(row=3, column=0)
        tk.Label(self.add_window, text="Height:").grid(row=4, column=0)

        self.name_entry = tk.Entry(self.add_window)
        self.name_entry.grid(row=0, column=1)
        self.x_entry = tk.Entry(self.add_window)
        self.x_entry.grid(row=1, column=1)
        self.y_entry = tk.Entry(self.add_window)
        self.y_entry.grid(row=2, column=1)
        self.width_entry = tk.Entry(self.add_window)
        self.width_entry.grid(row=3, column=1)
        self.height_entry = tk.Entry(self.add_window)
        self.height_entry.grid(row=4, column=1)

        submit_button = tk.Button(self.add_window, text="Submit", command=self.add_variable_submit)
        submit_button.grid(row=5, column=0, columnspan=2)

    def add_variable_submit(self):
        name = self.name_entry.get()
        x = self.x_entry.get()
        y = self.y_entry.get()
        width = self.width_entry.get()
        height = self.height_entry.get()

        self.add_variable(name, x, y, width, height)
        self.add_window.destroy()

    def add_variable(self, name, x, y, width, height):
        new_variable = {'Name': name, 'X': x, 'Y': y, 'Width': width, 'Height': height}
        self.variable_db.append(new_variable)
        self.update_treeview()
        self.update_variable_db_json()  # Save changes to the JSON file

    def delete_variable(self):
        selected_item = self.tree.selection()[0]
        for var in self.variable_db:
            if var['Name'] == self.tree.item(selected_item, 'values')[0]:
                self.variable_db.remove(var)
                self.update_treeview()
                self.update_variable_db_json()  # Save changes to the JSON file
                break

    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_treeview()

    def update_variable_db_json(self):
        with open('Server/config.json', 'w') as json_file:
            json.dump({'General': self.general_options, 'VariableDB': self.variable_db}, json_file, indent=4)

    def cutPiece(self, name, x, y, width, height):
        img = Image.open(self.screenshot_path)
        piece = img.crop((x, y, x + width, y + height))
        piece_path = os.path.join(self.temp_dir, name + ".jpg")
        piece.save(piece_path)


def main():
    root = tk.Tk()
    app = SettingsWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
