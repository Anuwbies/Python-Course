"""
================================================================================
Level 1: Beginner Python
Lesson 10: Object-Oriented Programming (OOP) Fundamentals
================================================================================
📝 Quick Exercise: Commercial Fleet Logistics & Telematics System

🏢 Real-Life Scenario:
You are developing the fleet tracking and telematics management engine for a
regional parcel logistics company. The company needs an Object-Oriented system
comprising a DeliveryVehicle class (modeling vehicle odometer, fuel capacity,
fuel consumption, trip tracking, and maintenance alerts) and a FleetManager class
(coordinating vehicles across the depot and producing executive fleet summaries).

📋 Requirements:
1. DeliveryVehicle class:
   - __init__(vehicle_id, model, max_payload_kg, fuel_capacity_l)
   - refuel(liters) -> float
   - record_trip(distance_km, fuel_consumed_l) -> bool (triggers maintenance_due if odo >= 500)
   - __str__() -> formatted vehicle status
2. FleetManager class:
   - __init__(depot_name)
   - add_vehicle(vehicle)
   - print_fleet_report() -> displays all vehicle statuses and fleet-wide totals
3. Test with 3 vehicles and print report.

⚠️ Strict Constraint:
Use ONLY concepts covered across Lessons 1-10 (variables, primitives, strings,
conditionals, loops, lists, dicts, functions, OOP classes, methods, __init__,
self, __str__, collections of objects, f-strings, and print()).
================================================================================
"""

class DeliveryVehicle:
    """Represents a commercial delivery vehicle tracking telemetry and maintenance."""
    
    def __init__(self, vehicle_id: str, model: str, max_payload_kg: float, fuel_capacity_l: float):
        self.vehicle_id = vehicle_id
        self.model = model
        self.max_payload_kg = float(max_payload_kg)
        self.fuel_capacity_l = float(fuel_capacity_l)
        self.current_fuel_l = float(fuel_capacity_l)
        self.odometer_km = 0.0
        self.trip_count = 0
        self.maintenance_due = False

    def refuel(self, liters: float) -> float:
        """Adds fuel to tank, capping at max capacity."""
        if liters <= 0:
            print("[ERROR] Refuel amount must be positive.")
            return self.current_fuel_l
        self.current_fuel_l = min(self.current_fuel_l + liters, self.fuel_capacity_l)
        return self.current_fuel_l

    def record_trip(self, distance_km: float, fuel_consumed_l: float) -> bool:
        """Validates and records a delivery route trip."""
        if distance_km <= 0 or fuel_consumed_l <= 0:
            print("[ERROR] Invalid trip metrics.")
            return False
            
        if fuel_consumed_l > self.current_fuel_l:
            print(f"[ERROR] Insufficient fuel in {self.vehicle_id} for requested trip!")
            return False

        self.current_fuel_l -= fuel_consumed_l
        self.odometer_km += distance_km
        self.trip_count += 1
        
        if self.odometer_km >= 500.0:
            self.maintenance_due = True
            
        return True

    def __str__(self) -> str:
        return (
            f"[{self.vehicle_id:<7}] {self.model:<19} | "
            f"Odo: {self.odometer_km:>6.1f} km | "
            f"Fuel: {self.current_fuel_l:>5.1f}/{self.fuel_capacity_l:.1f} L | "
            f"Trips: {self.trip_count} | "
            f"Maint Due: {self.maintenance_due}"
        )


class FleetManager:
    """Manages a collection of delivery vehicles for a regional logistics depot."""
    
    def __init__(self, depot_name: str):
        self.depot_name = depot_name
        self.vehicles = []

    def add_vehicle(self, vehicle: DeliveryVehicle) -> None:
        """Registers a delivery vehicle into the fleet."""
        self.vehicles.append(vehicle)

    def print_fleet_report(self) -> None:
        """Displays formatted operational status report across the entire fleet."""
        total_fleet_km = sum(v.odometer_km for v in self.vehicles)
        total_trips = sum(v.trip_count for v in self.vehicles)
        maint_list = [v.vehicle_id for v in self.vehicles if v.maintenance_due]

        print("================================================================================")
        print(f"           FLEET TELEMATICS REPORT - {self.depot_name}")
        print("================================================================================")
        print("VEHICLE STATUS LEDGER:")
        for v in self.vehicles:
            print(f"- {v}")
            
        print("--------------------------------------------------------------------------------")
        print("FLEET-WIDE AGGREGATES:")
        print(f"Total Fleet Vehicles:   {len(self.vehicles)} vans")
        print(f"Total Cumulative Range: {total_fleet_km:,.1f} km")
        print(f"Total Completed Trips:  {total_trips} trips")
        print(f"Maintenance Due List:   {maint_list}")
        print("================================================================================")


# Execution & Testing
depot = FleetManager("Northwest Regional Depot")

v1 = DeliveryVehicle("VAN-101", "Ford Transit High", 1500, 75.0)
v2 = DeliveryVehicle("VAN-102", "Mercedes Sprinter", 1800, 85.0)
v3 = DeliveryVehicle("EV-201", "Rivian Delivery Van", 1200, 100.0)

depot.add_vehicle(v1)
depot.add_vehicle(v2)
depot.add_vehicle(v3)

# Simulate trips
v1.record_trip(280.0, 25.0)
v1.record_trip(240.0, 25.0)  # Odometer reaches 520 km -> maintenance_due becomes True
v2.record_trip(310.5, 35.0)
v3.record_trip(180.0, 35.0)

# Display fleet summary
depot.print_fleet_report()