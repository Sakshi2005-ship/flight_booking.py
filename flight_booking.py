from abc import ABC, abstractmethod


# Class 1: Flight
class Flight:
    def __init__(self, code, airline, source, destination, seats, base_fare):
        self.__code = code
        self.__airline = airline
        self.__source = source
        self.__destination = destination
        self.__available_seats = seats
        self.__base_fare = base_fare

    @property
    def code(self):
        return self.__code

    @property
    def airline(self):
        return self.__airline

    @property
    def source(self):
        return self.__source

    @property
    def destination(self):
        return self.__destination

    @property
    def available_seats(self):
        return self.__available_seats

    @property
    def base_fare(self):
        return self.__base_fare

    def has_seats(self, count):
        return count <= self.__available_seats

    def reserve_seats(self, count):
        if count <= 0 or not self.has_seats(count):
            return False

        self.__available_seats -= count
        return True

    def display(self):
        print(
            f"{self.code:<8} {self.airline:<15} "
            f"{self.source:<12} {self.destination:<12} "
            f"{self.available_seats:<8} Rs.{self.base_fare}"
        )


# Class 2: Abstract Passenger
class Passenger(ABC):
    def __init__(self, name, age):
        self.name = name.strip()
        self.age = age

    @abstractmethod
    def get_discount(self):
        pass

    @abstractmethod
    def passenger_type(self):
        pass


# Class 3: Regular Passenger
class RegularPassenger(Passenger):
    def get_discount(self):
        return 0.0

    def passenger_type(self):
        return "Regular"


# Class 4: Student Passenger
class StudentPassenger(Passenger):
    def get_discount(self):
        return 0.10

    def passenger_type(self):
        return "Student"


# Class 5: Booking
class Booking:
    def __init__(
        self, booking_id, flight, passenger,
        ticket_count, subtotal, discount, total
    ):
        self.booking_id = booking_id
        self.flight = flight
        self.passenger = passenger
        self.ticket_count = ticket_count
        self.subtotal = subtotal
        self.discount = discount
        self.total = total

    def display_summary(self):
        print("\n========== BOOKING SUMMARY ==========")
        print(f"Booking ID: {self.booking_id}")
        print(
            f"Flight: {self.flight.code} | "
            f"{self.flight.source} to {self.flight.destination}"
        )
        print(f"Airline: {self.flight.airline}")
        print(f"Passenger: {self.passenger.name}")
        print(f"Age: {self.passenger.age}")
        print(f"Passenger type: {self.passenger.passenger_type()}")
        print(f"Tickets: {self.ticket_count}")
        print(f"Base fare per ticket: Rs.{self.flight.base_fare:.2f}")
        print(f"Subtotal: Rs.{self.subtotal:.2f}")
        print(
            f"Discount ({self.passenger.get_discount() * 100:.0f}%): "
            f"Rs.{self.discount:.2f}"
        )
        print(f"Final amount: Rs.{self.total:.2f}")
        print("=====================================")


# Class 6: Flight Booking System
class FlightBookingSystem:
    def __init__(self):
        self.flights = [
            Flight("PN101", "Kiran Air", "Pune", "Delhi", 20, 4000),
            Flight("MB202", "Sky India", "Mumbai", "Bengaluru", 15, 3500),
            Flight("PN303", "Air Connect", "Pune", "Hyderabad", 18, 3000)
        ]

        self.bookings = []
        self.next_booking_number = 1001

    # Display all flights
    def display_flights(self):
        print("\n================ AVAILABLE FLIGHTS ================")
        print(
            f"{'Code':<8} {'Airline':<15} {'Source':<12} "
            f"{'Destination':<12} {'Seats':<8} Base Fare"
        )
        print("-" * 75)

        for flight in self.flights:
            flight.display()

        print("-" * 75)

    # Find flight using flight code
    def find_flight(self, code):
        for flight in self.flights:
            if flight.code.lower() == code.strip().lower():
                return flight

        return None

    # Validate booking details
    def validate_booking_details(
        self, flight, name, age, passenger_type, ticket_count
    ):
        if flight is None:
            return "Invalid flight code."

        if not name.strip():
            return "Passenger name cannot be blank."

        if age <= 0:
            return "Age must be greater than zero."

        if passenger_type.lower() not in ("regular", "student"):
            return "Passenger type must be Regular or Student."

        if ticket_count <= 0:
            return "Number of tickets must be greater than zero."

        if not flight.has_seats(ticket_count):
            return "Not enough seats available."

        return None

    # Calculate ticket fare
    def calculate_fare(self, flight, passenger, ticket_count):
        subtotal = flight.base_fare * ticket_count
        discount = subtotal * passenger.get_discount()
        total = subtotal - discount

        return subtotal, discount, total

    # Confirm booking
    def confirm_booking(self, flight, passenger, ticket_count):
        if not flight.has_seats(ticket_count):
            print("Booking failed: Not enough seats available.")
            return

        subtotal, discount, total = self.calculate_fare(
            flight, passenger, ticket_count
        )

        # Reduce seats only after validation succeeds
        if not flight.reserve_seats(ticket_count):
            print("Booking failed: Could not reserve seats.")
            return

        booking = Booking(
            f"BK{self.next_booking_number}",
            flight,
            passenger,
            ticket_count,
            subtotal,
            discount,
            total
        )

        self.next_booking_number += 1
        self.bookings.append(booking)

        print("\nBooking confirmed!")
        booking.display_summary()

    # Book a flight
    def book_flight(self):
        self.display_flights()

        code = input("Enter flight code: ").strip()
        flight = self.find_flight(code)

        name = input("Enter passenger name: ").strip()

        try:
            age = int(input("Enter age: "))
            passenger_type = input(
                "Passenger type (Regular/Student): "
            ).strip()
            ticket_count = int(input("Enter number of tickets: "))

        except ValueError:
            print("Invalid input: age and ticket count must be whole numbers.")
            print("No booking was created.")
            return

        error = self.validate_booking_details(
            flight, name, age, passenger_type, ticket_count
        )

        if error:
            print(f"Booking failed: {error}")
            print("No booking was created; seat counts remain unchanged.")
            return

        if passenger_type.lower() == "student":
            passenger = StudentPassenger(name, age)
        else:
            passenger = RegularPassenger(name, age)

        self.confirm_booking(flight, passenger, ticket_count)

    # View latest booking
    def view_booking(self):
        if not self.bookings:
            print("\nNo confirmed bookings yet. Please book a flight first.")
            return

        self.bookings[-1].display_summary()

    # Main menu
    def run(self):
        print("Welcome to Kiran Air Booking")

        while True:
            print("\n1. View Flights")
            print("2. Book Flight")
            print("3. View Booking")
            print("4. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.display_flights()

            elif choice == "2":
                self.book_flight()

            elif choice == "3":
                self.view_booking()

            elif choice == "4":
                print("Thank you for using Kiran Air Booking!")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 4.")


# Main program
if __name__ == "__main__":
    app = FlightBookingSystem()
    app.run()