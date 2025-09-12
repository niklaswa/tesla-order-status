import sys
import re

def decode_tesla_vin(vin):
    if not vin or len(vin) != 17 or not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin):
        return "Error: Invalid VIN format. Must be 17 alphanumeric characters (excluding I, O, Q)."

    # Define decoding mappings
    manufacturer_codes = {
        "5YJ": "Tesla, Inc. (USA)",
        "7SA": "Tesla, Inc. (USA)",
        "SFZ": "Tesla, Inc. (UK)",
        "LRW": "Tesla, Inc. (China)"
    }
    
    model_codes = {
        "S": "Model S",
        "3": "Model 3",
        "X": "Model X",
        "Y": "Model Y",
        "R": "Roadster",
        "T": "Semi",
        "C": "Cybertruck"
    }
    
    body_type_codes = {
        "A": "Sedan, 4-door (Model S, 3)",
        "B": "SUV, 5-door (Model X, Y)",
        "C": "Truck (Semi, Cybertruck)",
        "E": "Hatchback, 5-door",
        "F": "Sedan, 4-door (Model 3, China)"  # Added for LRW VIN
    }
    
    restraint_codes = {
        "1": "Type 1 Manual Belts",
        "2": "Type 2 Active Belts",
        "3": "Type 2 Active Belts with Front Airbags",
        "4": "Type 2 Active Belts with Front and Side Airbags",
        "5": "Type 2 Active Belts with Front, Side, and Knee Airbags",
        "7": "Type 2 Active Belts with Advanced Airbags"  # Hypothetical for Model 3
    }
    
    battery_codes = {
        "E": "Electric",
        "H": "High-capacity Electric",
        "S": "Standard-range Electric",
        "L": "Long-range Electric",
        "F": "Standard-range Electric (China)"  # Added for Model 3
    }
    
    drive_unit_codes = {
        "1": "Single Motor",
        "2": "Dual Motor",
        "3": "Tri Motor",
        "P": "Performance Dual Motor",
        "T": "Tri Motor Performance",
        "S": "Single Motor (Rear-Wheel Drive)"  # Added for Model 3
    }
    
    year_codes = {
        "A": 2010, "B": 2011, "C": 2012, "D": 2013, "E": 2014, "F": 2015, "G": 2016,
        "H": 2017, "J": 2018, "K": 2019, "L": 2020, "M": 2021, "N": 2022, "P": 2023,
        "R": 2024, "S": 2025, "T": 2026
    }
    
    plant_codes = {
        "A": "Austin, TX, USA",
        "F": "Fremont, CA, USA",
        "G": "Giga Shanghai, China",
        "B": "Berlin, Germany",
        "N": "Reno, NV, USA",
        "C": "Giga Shanghai, China"  # Added for LRW VIN
    }

    # Decode each part of the VIN
    manufacturer = manufacturer_codes.get(vin[0:3], "Unknown Manufacturer")
    model = model_codes.get(vin[3], "Unknown Model")
    body_type = body_type_codes.get(vin[4], "Unknown Body Type")
    restraint = restraint_codes.get(vin[5], "Unknown Restraint System")
    battery = battery_codes.get(vin[6], "Unknown Battery Type")
    drive_unit = drive_unit_codes.get(vin[7], "Unknown Drive Unit")
    year = year_codes.get(vin[9], "Unknown Year")
    plant = plant_codes.get(vin[10], "Unknown Plant")
    serial = vin[11:17]
    check_digit = vin[8]

    # Format the output
    output = (
        f"VIN: {vin}\n"
        f"Manufacturer: {manufacturer}\n"
        f"Model: {model}\n"
        f"Body Type: {body_type}\n"
        f"Restraint System: {restraint}\n"
        f"Battery Type: {battery}\n"
        f"Drive Unit: {drive_unit}\n"
        f"Model Year: {year}\n"
        f"Manufacturing Plant: {plant}\n"
        f"Serial Number: {serial}\n"
        f"Check Digit: {check_digit}"
    )

    return output

def main():
    if len(sys.argv) != 2:
        print("Usage: python decode_vin.py <VIN>")
        sys.exit(1)

    vin = sys.argv[1].strip()
    decoded_output = decode_tesla_vin(vin)

    # Write to vin.txt
    try:
        with open("vin.txt", "w") as f:
            f.write(decoded_output)
        print(f"Decoded VIN details written to vin.txt")
    except Exception as e:
        print(f"Error writing to vin.txt: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()