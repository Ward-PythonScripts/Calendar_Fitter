class Booking:
    def __init__(self,start_time:int,end_time:int,priority:int,day_of_the_week:int):
        #for now booked = priority 1
        #available = priority 0
        self.start_time = start_time
        self.end_time = end_time
        self.priority = priority
        self.day_of_the_week = day_of_the_week

class Dates_Container:
    def __init__(self):
        self.booked: list[list[Booking]] = self.innit_booking_days()

    def innit_booking_days(self) -> list[list[Booking]]:
        booked_l = []
        for day in range(7):
            day_booking = []
            booked_l.append(day_booking)
        return booked_l

    def add_booking(self, booking: Booking):
        booking_of_correct_day = self.booked[booking.day_of_the_week]
        booking_of_correct_day.append(booking)

