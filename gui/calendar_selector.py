import math
import time
import tkinter
from tkinter import *

import pyautogui

from gui.dates_container import *
from ErrorHandler.SmashAndDash import SmashAndDash



class MyBox:
    def __init__(self, day: int, start_time: int, end_time: int, master, row_pos: int, col_pos: int):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.master = master
        self.row_pos = row_pos
        self.col_pos = col_pos
        self.label = self.create_Label()
        self.priority = 0

    def create_Label(self):
        label = tkinter.Label(self.master, fg="green", height="1", width="4", text="      ", borderwidth=5,
                              relief="ridge",
                              background="white")
        label.grid(row=self.row_pos, column=self.col_pos)
        label.bind("<ButtonRelease-1>",
                   lambda event, first_clicked_label=self: leftMouseReleasedOnLabel(event, first_clicked_label))
        label.bind("<ButtonRelease-3>",
                   lambda event, label_clicked=self: rightMouseReleasedOnLabel(event, label_clicked))
        return label

    def label_selected(self, priority: int):
        if self.priority != priority:
            # something changed
            self.change_color(priority)
            self.priority = priority

    def change_color(self, priority: int):
        if priority == 0:
            self.label.configure(background="white")
        elif priority == 1:
            self.label.configure(background="green")
        elif priority == 2:
            self.label.configure(background="orange")
        elif priority == 3:
            self.label.configure(background="red")
        else:
            self.label.configure(background="pink")

class Person:
    def __init__(self,name):
        self.bookings:Dates_Container = Dates_Container()
        self.name:str = name

    def save_bookings(self,dates:Dates_Container):
        self.bookings = dates

    def save_bookings_from_labels(self,labels:list[list[MyBox]]):
        self.bookings = Dates_Container()
        for day in range(len(labels)):
            begin_time = -1
            begin_priority = -1
            for interval in range(len(labels[day])):
                #if begin time is -1, it isn't yet set and needs to be set by the next label
                if begin_time == -1:
                    begin_time = labels[day][interval].start_time
                #same with the begin priority
                if begin_priority == -1:
                    begin_priority = labels[day][interval].priority
                if labels[day][interval].priority != begin_priority:
                    #end of planning event
                    self.bookings.add_booking(Booking(start_time=begin_time,
                                                      end_time=labels[day][interval].end_time,
                                                      priority=begin_priority,
                                                      day_of_the_week=day))
                    #update parameters which we use to check the events
                    begin_time = -1
                    begin_priority = -1
            #the last element will always be the end
            self.bookings.add_booking(Booking(start_time=begin_time,
                                              end_time=labels[day][len(labels[day])-1].end_time,
                                              priority=begin_priority,
                                              day_of_the_week=day))

    def get_name(self) -> str:
        return self.name

    def get_bookings_as_labels(self) -> list[list[MyBox]]:
        print("Still need to implement this my dog")


class Person_Manager:
    def __init__(self):
        self.persons:list[Person] = []
        self.activePerson:Person = None

    def add_Person(self,person_name:str,set_active:bool):
        new_p = Person(person_name)
        self.persons.append(new_p)
        if set_active:
            self.activePerson = new_p

    def get_person_names(self) -> list[str]:
        name_lst:list[str] = []
        for person in self.persons:
            name_lst.append(person.get_name())
        return name_lst

    def set_person_active(self,person:Person):
        self.activePerson = person

    def set_person_active_name(self,person_name:str):
        person = self.get_person_from_name(person_name)
        self.activePerson = person

    def get_person_from_name(self,person_name:str) -> Person:
        for person in self.persons:
            if person.get_name() == person_name:
                return person

    def save_persons_bookings(self,person,labels:list[list[MyBox]]):
        if person is None:
            person=self.activePerson
        person.save_bookings_from_labels(labels)

    def load_persons_bookings(self,person_par) -> list[list[MyBox]]:
        #verify input
        person = None
        if type(person_par) == str:
            person = self.get_person_from_name(person_par)
        elif type(person_par) == Person:
            person = person_par
        else:
            SmashAndDash("Didn't receive a Person or a str object")

        #actual function


class Calendar_selector:
    def __init__(self, amount_of_minutes_in_between: int):
        self.person_manager = Person_Manager()
        self.amount_of_minutes_in_between = amount_of_minutes_in_between
        self.master = Tk()
        self.master.title("Use the left mouse button to select and use the right mouse button to deselect")
        self.calendar_frame = Frame(master=self.master)
        self.calendar_frame.pack(side=LEFT)
        self.main_window:tkinter.Canvas = self.create_hours_selection_widget()
        self.person_selector_frame = self.add_person_selector()
        mainloop()

    def create_hours_selection_widget(self) -> tkinter.Canvas:
        main_window = self.get_window()
        self.create_window_content(main_window)
        main_window.pack()
        return main_window

    def get_window(self):
        canvas_height = 600
        canvas_width = 900
        w = Canvas(self.calendar_frame, width=canvas_width, height=canvas_height, background='gray75')
        return w

    def add_person_selector(self) -> Frame:
        starting_row_pos = 3
        options_frame = Frame(master=self.master)
        options_frame.pack(side=RIGHT)
        label = Label(master=options_frame, text="participants")
        label.grid(row=starting_row_pos, column=0)
        starting_row_pos += 1
        # add new person button for each person in the person manager
        for name in self.person_manager.get_person_names():
            b = Button(master=options_frame,
                   text=name,
                   command=lambda person=self.person_manager.activePerson,
                                  cur_button=b:self.person_button_clicked(person,cur_button)).\
                grid(row=starting_row_pos, column=0)
            starting_row_pos += 1
        add_person_button = Button(master=options_frame,
                                   text="Add participant",
                                   command=lambda: EnterNameWindow(options_frame,
                                                                   self.person_manager, self.refresh_person_selector))
        add_person_button.grid(row=starting_row_pos, column=0)
        return options_frame

    def person_button_clicked(self,person:Person,button_pressed:Button):
        global day_labels
        button_pressed.configure(background="green")
        day_labels = self.person_manager.load



    def refresh_person_selector(self):
        self.person_selector_frame.destroy()
        self.person_selector_frame = self.add_person_selector()

    def create_window_content(self,main_window:tkinter.Canvas):
        self.add_interval_labels(main_window)
        self.add_selector_labels(main_window)

    def add_selector_labels(self,main_window:tkinter.Canvas):
        global day_labels
        temp_time = 0
        for day in range(0, 7):
            row_of_labels = []
            # first create the day header
            MyDayLabel(master=main_window, day=day)
            for x in range(math.floor((24 * 60) / self.amount_of_minutes_in_between)):
                # then create the day label itself
                temp_time += self.amount_of_minutes_in_between
                row_of_labels.append(
                    MyBox(day, start_time=temp_time - self.amount_of_minutes_in_between, end_time=temp_time,
                          master=main_window, row_pos=x + 1, col_pos=day + 1))
            day_labels.append(row_of_labels)

    def add_interval_labels(self,main_window:tkinter.Canvas):
        temp_time = 0
        # first the interval labels will be generated
        for x in range(math.floor((24 * 60) / self.amount_of_minutes_in_between)):
            # then create the day label itself
            temp_time += self.amount_of_minutes_in_between
            MyIntervalLabel(begin_time=temp_time - self.amount_of_minutes_in_between, end_time=temp_time,
                            master=main_window, row_pos=x + 1)
        return temp_time

    def save_current_persons_schedule(self):
        self.person_manager.save_persons_bookings(day_labels)




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


class EnterNameWindow(object):
    def __init__(self, master, pm: Person_Manager, cb):
        self.person_manager = pm
        top = self.top = Toplevel(master)
        self.lab = Label(top, text="Enter the name of the participant")
        self.lab.pack()
        self.e = Entry(top)
        self.e.pack()
        self.b = Button(top, text='Add', command=self.cleanup)
        self.b.pack()
        self.cb = cb

    def cleanup(self):
        self.person_manager.add_Person(self.e.get(),set_active=True)
        self.top.destroy()
        self.cb()


class MyIntervalLabel:
    def __init__(self, begin_time: int, end_time: int, master, row_pos):
        label = tkinter.Label(text=(begin_and_end_to_string(begin_time, end_time)), master=master, justify="center")
        label.grid(row=row_pos, column=0)


class MyDayLabel:
    def __init__(self, day: int, master):
        days = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]
        label = tkinter.Label(text=days[day], master=master, justify="center")
        label.grid(row=0, column=day + 1)




def leftMouseReleasedOnLabel(event: Event, label: MyBox):
    mouseReleasedOnLabel(event=event, first_clicked_label=label, selected=True)


def rightMouseReleasedOnLabel(event: Event, label: MyBox):
    mouseReleasedOnLabel(event, label, False)


def mouseReleasedOnLabel(event: Event, first_clicked_label: MyBox, selected: bool):
    global mouse_event_handler
    # sadly we will have to find the label itself
    # since the ButtonRelease-1 is already filled in when the mouse is pressed, and doesn't return the label on which
    # was released
    was_first = mouse_event_handler.add_event(first_clicked_label, selected)
    # press the mouse again, and use that event to grab the second label. But we need to make sure we click the right
    # mouse button of course
    if was_first:
        # if selected = true, left mouse. else right mouse was clicked
        if selected:
            left_click_again_to_get_release()
        else:
            right_click_again_to_get_release()


def make_ascending(a1: int, b1: int) -> tuple[int, int]:
    if a1 > b1:
        # swap around
        c1 = a1
        a1 = b1
        b1 = c1
    return a1, b1


def complete_selection(start_label: MyBox, end_label: MyBox, selected: bool):
    # get the enclosed labels in between these two and trigger them as well, indexes in the MyBox object are starting
    # at 1
    x1 = start_label.row_pos - 1
    x2 = end_label.row_pos - 1
    y1 = start_label.col_pos - 1
    y2 = end_label.col_pos - 1
    # first we need to check if we are trying to go from small to big, otherwise won't work
    x1, x2 = make_ascending(x1, x2)
    y1, y2 = make_ascending(y1, y2)
    for y in range(len(day_labels)):
        for x in range(len(day_labels[y])):
            # if we are in between x1,x2 and in between y1,y2. The selection is to have effect
            if y1 <= y <= y2 and x1 <= x <= x2:
                day_labels[y][x].label_selected(selected)


def left_click_again_to_get_release():
    pyautogui.mouseDown()
    # sleep as a safeguard to make sure the click gets registered
    time.sleep(0.004)
    pyautogui.mouseUp()


def right_click_again_to_get_release():
    pyautogui.mouseDown(button="right")
    # sleep as a safeguard to make sure the click gets registered
    time.sleep(0.004)
    pyautogui.mouseUp(button="right")


class Mouse_Event_Handler:
    def __init__(self):
        self.first: bool = True
        self.First_Label: MyBox = None
        self.Second_Label: MyBox = None
        self.selected: bool = False

    def add_event(self, label: MyBox, selected: bool) -> bool:
        self.selected = selected
        if self.first:
            self.first = False
            self.First_Label = label
            return True
        else:
            self.Second_Label = label
            self.mouse_event_complete()
            return False

    def mouse_event_complete(self):
        complete_selection(self.First_Label, self.Second_Label, self.selected)
        self.First_Label = None
        self.Second_Label = None
        self.first = True







###Globals
mouse_event_handler = Mouse_Event_Handler()
day_labels: list[list[MyBox]] = []
