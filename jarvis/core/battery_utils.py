import psutil

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery is None:
        return None, None
    battery_level = battery.percent
    battery_status = "Charging" if battery.power_plugged else "Discharging"
    return battery_level, battery_status

def main():
    battery_level, battery_status = get_battery_info()
    
    if battery_level is None:
        print("Не вдалося отримати інформацію про батарею.")
        return
    
    if battery_level <= 5 and battery_status == "Discharging":
        print(f"Критичний рівень заряду батареї ({battery_level}%)! Немедленно підключіть зарядний пристрій.")
    elif battery_level <= 20 and battery_status == "Discharging":
        print(f"Увага: рівень заряду батареї низький ({battery_level}%)! Підключіть зарядний пристрій.")
    else:
        print(f"Рівень заряду батареї: {battery_level}%. Статус: {battery_status}.")

if __name__ == "__main__":
    main()
