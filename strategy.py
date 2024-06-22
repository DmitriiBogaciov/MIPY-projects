from abc import ABC, abstractmethod

# Definice rozhraní Strategie
class ParkingStrategy(ABC):
    @abstractmethod
    def check_availability(self) -> bool:
        pass
    
    @abstractmethod
    def calculate_cost(self, hours: int) -> float:
        pass
    
    @abstractmethod
    def reserve(self, vehicle_info: str) -> str:
        pass

# Implementace konkrétních strategií
class CarParkingStrategy(ParkingStrategy):
    def check_availability(self) -> bool:
        # Example logic to check car parking availability
        return True  # Assume always available for simplicity

    def calculate_cost(self, hours: int) -> float:
        # Example cost calculation for cars
        return hours * 25

    def reserve(self, vehicle_info: str) -> str:
        if not self.check_availability():
            return "Parkovací místo pro automobil není dostupné."
        cost = self.calculate_cost(2)  # Example: reservation for 2 hours
        return f"Rezervace parkovacího místa pro automobil: {vehicle_info}. Cena: {cost} CZK"


class MotorcycleParkingStrategy(ParkingStrategy):
    def check_availability(self) -> bool:
        # Example logic to check motorcycle parking availability
        return True  # Assume always available for simplicity

    def calculate_cost(self, hours: int) -> float:
        # Example cost calculation for motorcycles
        return hours * 15.0

    def reserve(self, vehicle_info: str) -> str:
        if not self.check_availability():
            return "Parkovací místo pro motocykl není dostupné."
        cost = self.calculate_cost(2)  # Example: reservation for 2 hours
        return f"Rezervace parkovacího místa pro motocykl: {vehicle_info}. Cena: {cost} CZK"


class ElectricCarParkingStrategy(ParkingStrategy):
    def check_availability(self) -> bool:
        return True  # Assume always available for simplicity

    def calculate_cost(self, hours: int) -> float:
        return hours * 20.0  # Assume lower cost for electric cars

    def reserve(self, vehicle_info: str) -> str:
        if not self.check_availability():
            return "Parkovací místo pro elektromobil není dostupné."
        cost = self.calculate_cost(2)  # Example: reservation for 2 hours
        return f"Rezervace parkovacího místa pro elektromobil: {vehicle_info}. Cena: {cost} CZK"

# Třída pro správu rezervací parkování
class ParkingReservationSystem:
    def __init__(self, strategy: ParkingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ParkingStrategy):
        self._strategy = strategy

    def reserve_parking(self, vehicle_info: str) -> str:
        return self._strategy.reserve(vehicle_info)

    def check_availability(self) -> bool:
        return self._strategy.check_availability()

    def calculate_cost(self, hours: int) -> float:
        return self._strategy.calculate_cost(hours)

# Příklad použití
if __name__ == "__main__":
    car_info = "Škoda Octavia, SPZ 1A2 3456"
    motorcycle_info = "Honda CBR, SPZ 7B8 9101"
    electric_car_info = "Tesla Model 3, SPZ 2C3 4567"

    car_strategy = CarParkingStrategy()
    motorcycle_strategy = MotorcycleParkingStrategy()
    electric_car_strategy = ElectricCarParkingStrategy()

    parking_system = ParkingReservationSystem(car_strategy)
    print(parking_system.reserve_parking(car_info))

    parking_system.set_strategy(motorcycle_strategy)
    print(parking_system.reserve_parking(motorcycle_info))

    parking_system.set_strategy(electric_car_strategy)
    print(parking_system.reserve_parking(electric_car_info))
