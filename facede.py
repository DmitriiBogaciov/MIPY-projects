# Facade Design Pattern for Hotel Reservation System

# External Reservation Subsystem
class ExternalReservation:
    def reserve(self, customer_details, room_type, dates):
        # Simple mock implementation
        return f"External reservation for {customer_details['name']} in {room_type} from {dates['check_in']} to {dates['check_out']}"

    def cancel(self, reservation_id):
        # Simple mock implementation
        return f"External reservation {reservation_id} cancelled"

    def check_availability(self, room_type, dates):
        # Simple mock implementation
        return f"Availability for {room_type} from {dates['check_in']} to {dates['check_out']} (External)"

    def get_details(self, reservation_id):
        # Simple mock implementation
        return f"Details for external reservation {reservation_id}"

    def update(self, reservation_id, new_details):
        # Simple mock implementation
        return f"External reservation {reservation_id} updated with {new_details}"

    def send_request(self, reservation_id, request):
        # Simple mock implementation
        return f"Special request '{request}' sent for external reservation {reservation_id}"


# Internal Reservation Subsystem
class InternalReservation:
    def reserve(self, customer_details, room_type, dates):
        # Simple mock implementation
        return f"Internal reservation for {customer_details['name']} in {room_type} from {dates['check_in']} to {dates['check_out']}"

    def cancel(self, reservation_id):
        # Simple mock implementation
        return f"Internal reservation {reservation_id} cancelled"

    def check_availability(self, room_type, dates):
        # Simple mock implementation
        return f"Availability for {room_type} from {dates['check_in']} to {dates['check_out']} (Internal)"

    def get_details(self, reservation_id):
        # Simple mock implementation
        return f"Details for internal reservation {reservation_id}"

    def update(self, reservation_id, new_details):
        # Simple mock implementation
        return f"Internal reservation {reservation_id} updated with {new_details}"

    def send_request(self, reservation_id, request):
        # Simple mock implementation
        return f"Special request '{request}' sent for internal reservation {reservation_id}"


# Pricing Management Subsystem
class SpravaCenovychTarifu:
    def __init__(self):
        self.prices = {}

    def set_room_price(self, room_type, price):
        self.prices[room_type] = price

    def get_room_price(self, room_type):
        return self.prices.get(room_type, None)

    def update_room_price(self, room_type, new_price):
        self.prices[room_type] = new_price

    def apply_discount(self, room_type, discount):
        if room_type in self.prices:
            self.prices[room_type] -= discount

    def get_price_list(self):
        return self.prices


# Facade Class
class ReservationSystem:
    def __init__(self):
        self.external_reservation = ExternalReservation()
        self.internal_reservation = InternalReservation()
        self.pricing_management = SpravaCenovychTarifu()

    def make_reservation(self, customer_details, room_type, dates):
        external_result = self.external_reservation.reserve(customer_details, room_type, dates)
        if external_result:
            return external_result

        internal_result = self.internal_reservation.reserve(customer_details, room_type, dates)
        return internal_result

    def cancel_reservation(self, reservation_id):
        if self.external_reservation.cancel(reservation_id):
            return True
        return self.internal_reservation.cancel(reservation_id)

    def check_availability(self, room_type, dates):
        availability = []
        availability.append(self.external_reservation.check_availability(room_type, dates))
        availability.append(self.internal_reservation.check_availability(room_type, dates))
        return availability

    def get_reservation_details(self, reservation_id):
        details = self.external_reservation.get_details(reservation_id)
        if details:
            return details

        return self.internal_reservation.get_details(reservation_id)

    def update_reservation(self, reservation_id, new_details):
        if self.external_reservation.update(reservation_id, new_details):
            return True
        return self.internal_reservation.update(reservation_id, new_details)

    def send_special_request(self, reservation_id, request):
        if self.external_reservation.send_request(reservation_id, request):
            return True
        return self.internal_reservation.send_request(reservation_id, request)

    def set_room_price(self, room_type, price):
        self.pricing_management.set_room_price(room_type, price)

    def get_room_price(self, room_type):
        return self.pricing_management.get_room_price(room_type)

    def update_room_price(self, room_type, new_price):
        self.pricing_management.update_room_price(room_type, new_price)

    def apply_discount(self, room_type, discount):
        self.pricing_management.apply_discount(room_type, discount)

    def get_price_list(self):
        return self.pricing_management.get_price_list()


# Example usage
if __name__ == "__main__":
    reservation_system = ReservationSystem()
    customer_details = {"name": "John Doe", "email": "john@example.com"}
    room_type = "Deluxe"
    dates = {"check_in": "2024-07-01", "check_out": "2024-07-10"}

    # Make a reservation
    reservation_result = reservation_system.make_reservation(customer_details, room_type, dates)
    print("Reservation result:", reservation_result)

    # Check room availability
    availability = reservation_system.check_availability(room_type, dates)
    print("Room availability:", availability)

    # Set room price
    reservation_system.set_room_price(room_type, 150)

    # Get room price
    room_price = reservation_system.get_room_price(room_type)
    print("Room price:", room_price)

    # Apply discount
    reservation_system.apply_discount(room_type, 10)
    updated_price = reservation_system.get_room_price(room_type)
    print("Updated room price after discount:", updated_price)
