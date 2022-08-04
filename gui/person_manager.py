from gui.dates_container import *

class Person:
    def __init__(self,name):
        self.bookings:Dates_Container = Dates_Container()
        self.name:str = name

    def save_bookings(self,dates:Dates_Container):
        self.bookings = dates

    def get_name(self) -> str:
        return self.name

class Person_Manager:
    def __init__(self):
        self.persons:list[Person] = []

    def add_Person(self,person_name:str):
        self.persons.append(Person(person_name))

    def get_person_names(self) -> list[str]:
        name_lst:list[str] = []
        for person in self.persons:
            name_lst.append(person.get_name())
        return name_lst
