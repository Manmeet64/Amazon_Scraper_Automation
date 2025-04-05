import os 
from datetime import datetime 

def get_timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def save_screenshot(driver, folder="screenshots"):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)  # ✅ Fix

    timestamp = get_timestamp()
    path = os.path.join(folder, f"screenshot-{timestamp}.png")
    driver.save_screenshot(path)
    print(f"Screenshot saved: {path}")

def save_logs(driver, folder="logs"):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)  # ✅ Fix
    
    timestamp = get_timestamp()
    path = os.path.join(folder, f"logs-{timestamp}.txt")

    try:
        logs = driver.get_log("performance")
        with open(path, "w") as logfile:
            for entry in logs:
                logfile.write(f"{entry}\n")
        print(f"Logs saved: {path}")
    except Exception as e:
        print(f"Failed to save logs: {e}")
