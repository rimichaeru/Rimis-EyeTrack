#!/usr/bin/env python
# coding: utf-8


from numpy.random import randint
from tkinter import *
from tkinter.ttk import *
import pkg_resources.py2_warn #needed for exe compile



class tr():
    
    grid = (27, 48)
    after_id_clear = None
    after_id_play = None
    speed = 500
    grid_colour = "white"
    grid_colour_outline = "white"
    target_colour = "red"
    target_colour_outline = "red"
    
    
    
    def __init__(self):
        return
    
    
    
    def set_speed(self):
        popup = Toplevel(root)
        popup.wm_title("Speed")
        popup.tkraise(root)
        
        def speed_button():
            
            try:
                self.speed = int(e.get())
                speed_entry.set("Speed set to {}ms".format(self.speed))
            except:
                self.speed = 500
                speed_entry.set("Error, enter number".format(self.speed))
                
        speed_entry = StringVar()       
        confirm_label = Label(popup, textvariable=speed_entry, foreground="red")
        confirm_label.grid(row=1, column=0)
            
        e = Entry(popup)
        e.grid(row=0, column=0)
        e_hover = CreateToolTip(e, text="Default: 500 (0.5s) \n Time between targets in ms")
        
        b_speed = Button(popup, text="Set Speed", command=speed_button)
        b_speed.grid(row=0, column=1)
        
        
        
    
    def start_game(self):
        #stop a running game
        if self.after_id_play:
            root.after_cancel(self.after_id_play)
            root.after_cancel(self.after_id_clear)
            self.after_id_play = None
            self.after_id_clear = None
        
        #get random location for the pointer (and also the reset)
        def random_loc():
            loc_y = randint(0, (self.grid[0]-1))
            loc_x = randint(0, (self.grid[1]-1))
            return (loc_y, loc_x)
        
        def clear_canvas():
            canvas.delete(target)

        loc = random_loc()

        try:
            target = canvas.create_rectangle(loc[1]*32, loc[0]*28, (loc[1]+1)*32, (loc[0]+1)*28, 
                                             fill=self.target_colour, outline=self.target_colour_outline)
            self.after_id_clear = root.after(self.speed, clear_canvas)
            self.after_id_play = root.after(self.speed, self.start_game)
        
        except:
            error_pop = Toplevel(root)
            error_pop.wm_title("Error")
            error_pop.tkraise(root)
            error = Label(error_pop, text="Incorrect Target Colour \n Please change settings")
            error.grid(row=0, column=0)
            
        
    
    

    def stop_game(self):
        #stop running game
        root.after_cancel(self.after_id_play)
        root.after_cancel(self.after_id_clear)
        self.after_id_play = None
        self.after_id_clear = None
        
        canvas.delete("all")
        for i in range(self.grid[1]):
            for j in range(self.grid[0]):
                canvas.create_rectangle(i*32, j*28, (i+1)*32, (j+1)*28, 
                                        fill=self.grid_colour, outline=self.grid_colour_outline)
        
        
        
        
    def settings_popup(self):
        popup = Toplevel(root)
        popup.wm_title("Settings")
        popup.tkraise(root)

        def reset_window():
            try:
                self.grid = (int(y.get()), int(x.get()))
            except:
                self.grid = self.grid
            
            if e_grid_colour.get() != "":
                self.grid_colour = str(e_grid_colour.get())
            if e_grid_colour.get() != "":
                self.grid_colour_outline = str(e_grid_colour.get())
            if e_target_colour.get() != "":
                self.target_colour = str(e_target_colour.get())
            if e_target_colour.get() != "":
                self.target_colour_outline = str(e_target_colour.get())
            
            try:
                canvas.delete("all")

                for i in range(self.grid[1]):
                    for j in range(self.grid[0]):
                        canvas.create_rectangle(i*32, j*28, (i+1)*32, (j+1)*28, 
                                                fill=self.grid_colour, outline=self.grid_colour_outline)
            except:
                canvas.delete("all")

                for i in range(self.grid[1]):
                    for j in range(self.grid[0]):
                        canvas.create_rectangle(i*32, j*28, (i+1)*32, (j+1)*28, 
                                                fill="white", outline="white")
                        
                error_pop = Toplevel(popup)
                error_pop.wm_title("Error")
                error_pop.tkraise(popup)
                error = Label(error_pop, text="Incorrect BG Colour \n Defaulting to white background")
                error.grid(row=0, column=0)
                

        
        info_label = Label(popup, text="Leave box blank to keep previous setting")
        info_label.grid(row=0, column=0)
        
        x = Entry(popup)
        x.grid(row=1, column=0)
        x_label = Label(popup, text="Enter Width")
        x_label.grid(row=1, column=1)
        x_hover = CreateToolTip(x, text="Default: 48 \n (48*40 = 1920)")

        y = Entry(popup)
        y.grid(row=2, column=0)
        y_label = Label(popup, text="Enter Height")
        y_label.grid(row=2, column=1)
        y_hover = CreateToolTip(y, text="Default: 27 \n (27*40 = 1080)")
        
        e_grid_colour = Entry(popup)
        e_grid_colour.grid(row=3, column=0)
        grid_label = Label(popup, text="Background Colour")
        grid_label.grid(row=3, column=1)
        e_grid_colour_hover = CreateToolTip(e_grid_colour, text="Default: white \n Colour string or HEX")
        
        e_target_colour = Entry(popup)
        e_target_colour.grid(row=4, column=0)
        target_label = Label(popup, text="Target Colour")
        target_label.grid(row=4, column=1)
        e_target_colour_hover = CreateToolTip(e_target_colour, text="Default: red \n Colour string or HEX")
        
        b_submit = Button(popup, text="Draw Grid", command=reset_window)
        b_submit.grid(row=5, column=1)
        


#hover info
#x, y; default location


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


# # GUI


root = Tk()
root.state('zoomed')

tr = tr()

game_frame = Frame(root, width=tr.grid[1]*40, height=(tr.grid[0]*40)-320)
game_frame.pack()
button_frame = Frame(root, width=tr.grid[1]*40, height=200)
button_frame.pack()


canvas = Canvas(game_frame, width=tr.grid[1]*40, height=(tr.grid[0]*40)-320)
canvas.grid(row=0, column=0)


for i in range(tr.grid[1]):
    for j in range(tr.grid[0]):
        canvas.create_rectangle(i*32, j*28, (i+1)*32, (j+1)*28, 
                                fill="white", outline="white")


b_set_grid = Button(button_frame, text="Settings", command=tr.settings_popup)
b_set_grid.grid(row=0, column=0)

test = Button(button_frame, text="Set Speed", command=tr.set_speed)
test.grid(row=0, column=1)
test = Button(button_frame, text="START", command=tr.start_game)
test.grid(row=0, column=10)
test = Button(button_frame, text="STOP", command=tr.stop_game)
test.grid(row=0, column=11)

root.mainloop()