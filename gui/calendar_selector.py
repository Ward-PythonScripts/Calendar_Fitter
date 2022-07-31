import tkinter
from tkinter import *
import math


class Calendar_selector:
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
        temp_time = 0
        # first the interval labels will be generated
        for x in range(math.floor((24 * 60) / self.amount_of_minutes_in_between)):
            # then create the day label itself
            temp_time += self.amount_of_minutes_in_between
            MyIntervalLabel(begin_time=temp_time - self.amount_of_minutes_in_between, end_time=temp_time,
                            master=self.main_window, row_pos=x + 1)
        for day in range(0, 7):
            # first create the day header
            MyDayLabel(master=self.main_window, day=day)
            for x in range(math.floor((24 * 60) / self.amount_of_minutes_in_between)):
                # then create the day label itself
                temp_time += self.amount_of_minutes_in_between
                MyBox(day, start_time=temp_time - self.amount_of_minutes_in_between, end_time=temp_time,
                      master=self.main_window, row_pos=x + 1, col_pos=day + 1)


def minutes_to_hour_string(minutes: int) -> str:
    hours = math.floor(minutes / 60)
    minutes = minutes - hours * 60
    return pad_time(str(hours)) + ":" + pad_time(str(minutes))


def pad_time(original_time: str) -> str:
    if len(original_time) != 2:
        return "0" + original_time
    else:
        return original_time


def begin_and_end_to_string(begin_time: int, end_time: int) -> str:
    s1 = minutes_to_hour_string(begin_time)
    s2 = minutes_to_hour_string(end_time)
    return s1 + " - " + s2


class MyIntervalLabel:
    def __init__(self, begin_time: int, end_time: int, master, row_pos):
        label = tkinter.Label(text=(begin_and_end_to_string(begin_time, end_time)), master=master, justify="center")
        label.grid(row=row_pos, column=0)


class MyDayLabel:
    def __init__(self, day: int, master):
        days = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]
        label = tkinter.Label(text=days[day], master=master, justify="center")
        label.grid(row=0, column=day + 1)


class MyBox:
    def __init__(self, day: int, start_time: int, end_time: int, master, row_pos: int, col_pos: int):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.master = master
        self.row_pos = row_pos
        self.col_pos = col_pos
        self.label = self.create_Label()

    def create_Label(self):
        label = tkinter.Label(self.master, fg="green", height="2", width="4", text="      ", borderwidth=5,
                              relief="ridge",
                              background="white")
        label.grid(row=self.row_pos, column=self.col_pos)
        label.bind("<ButtonRelease-1>", lambda event,first_clicked_label=self: mouseReleasedOnLabel(event,
                                                                            first_clicked_label=first_clicked_label))
        return label


def mouseReleasedOnLabel(event: Event, first_clicked_label: MyBox):
    # sadly we will have to find the label itself
    # since the ButtonRelease-1 is already filled in when the mouse is pressed
    print("Was pressed on row ", first_clicked_label.day)
    #press the mouse again, and use that event to grab the second label.

