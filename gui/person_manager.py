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
        for person in self.persons:
            if person.get_name() == person_name:
                self.activePerson = person
                return
