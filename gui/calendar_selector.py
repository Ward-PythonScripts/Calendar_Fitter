import tkinter
from tkinter import *
import math


class Calendar_selector():
    def __init__(self, amount_of_minutes_in_between: int):
        self.amount_of_minutes_in_between = amount_of_minutes_in_between
        self.master = Tk()
        self.main_window = self.get_window()
        self.create_window_content()
        self.main_window.pack()
        mainloop()

    def get_window(self):
        canvas_height = 600
        canvas_width = 900
        w = Canvas(self.master, width=canvas_width, height=canvas_height, background='gray75')
        return w

    def create_window_content(self):
        intervals = []
        temp_time = 0
        for day in range(0,7):
            # first create the day header

            for x in range(math.floor((24 * 60) / self.amount_of_minutes_in_between)):
                #then create the day label itself
                intervals.append(temp_time + self.amount_of_minutes_in_between)
                temp_time += self.amount_of_minutes_in_between
                MyBox(day,start_time=temp_time-self.amount_of_minutes_in_between,end_time=temp_time,
                      master=self.main_window,row_pos=x,col_pos=day)



class MyBox:
    def __init__(self, day: int, start_time: int, end_time: int, master,row_pos:int,col_pos:int):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.master = master
        self.row_pos = row_pos
        self.col_pos = col_pos
        self.label = self.create_Label()

    def create_Label(self):
        label = tkinter.Label(self.master,fg="green", height="2", width="4",text="hey")
        label.grid(row=self.row_pos,column=self.col_pos)
        return label

    def button_clicked(self):
        pass
