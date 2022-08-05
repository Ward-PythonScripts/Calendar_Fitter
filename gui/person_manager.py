from gui.dates_container import *
from gui.calendar_selector import *
from ErrorHandler.SmashAndDash import *
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



