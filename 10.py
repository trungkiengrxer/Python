class Vehicle:
    def __init__(self, vehicle_id, name, brand, color, price):
        self.vehicle_id = vehicle_id
        self.name = name
        self.brand = brand
        self.color = color
        self.price = price
    
    def print_info(self):
        pass

    def is_car(self):
        pass

class Motorcycle(Vehicle):
    def __init__(self, vehicle_id, name, brand, color, max_speed, price):
        super().__init__(vehicle_id, name, brand, color, price)
        self.max_speed = max_speed
    
    # In thông tin xe máy
    def print_info(self):
        print(f'{self.vehicle_id} {self.name} {self.brand} {self.color} {self.max_speed} {self.price}')
    
    # Đánh dấu là xe máy
    def is_car(self):
        return False

class Car(Vehicle):
    def __init__(self, vehicle_id, name, brand, color, horsepower, price):
        super().__init__(vehicle_id, name, brand, color, price)
        self.horsepower = horsepower
    
    # In thông tin ô tô
    def print_info(self):
        print(f'{self.vehicle_id} {self.name} {self.brand} {self.color} {self.horsepower} {self.price}')
    
    # Đánh dấu là ô tô
    def is_car(self):
        return True

def main():
    vehicles = []
    
    # Đọc số lượng phương tiện
    N = int(input())
    
    # Đọc thông tin các phương tiện
    for _ in range(N):
        vehicle_id = input().strip()
        name = input().strip()
        brand = input().strip()
        color = input().strip()
        
        if vehicle_id.startswith("XM"):  # Xe máy
            max_speed = float(input().strip())
            price = float(input().strip())
            vehicles.append(Motorcycle(vehicle_id, name, brand, color, max_speed, price))
        elif vehicle_id.startswith("OTO"):  # Ô tô
            horsepower = float(input().strip())
            price = float(input().strip())
            vehicles.append(Car(vehicle_id, name, brand, color, horsepower, price))
    
    # Tên xe cần tìm
    search_name = input().strip()
    
    # Liệt kê các ô tô trước
    for vehicle in vehicles:
        if vehicle.is_car() and vehicle.name == search_name:
            vehicle.print_info()
    
    # Liệt kê các xe máy sau
    for vehicle in vehicles:
        if not vehicle.is_car() and vehicle.name == search_name:
            vehicle.print_info()

if __name__ == "__main__":
    main()
