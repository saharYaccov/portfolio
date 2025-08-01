
"""
CPU Monitoring and Temperature Utilities for macOS

This module provides a set of functions to monitor and retrieve CPU-related metrics on macOS systems.
It includes capabilities to:
- Read CPU temperature via external tools (osx-cpu-temp, powermetrics)
- Monitor CPU usage per core over time with live printouts and graphical visualization
- Detect CPU core counts (physical and logical)
- Check if the system is running Apple Silicon (arm64 architecture)
- Read fan speed using 'istats'
- Parse CPU status from the 'top' command output and convert it into a pandas DataFrame
- Continuously monitor CPU temperature until it cools below a given threshold

The module leverages external command line tools (osx-cpu-temp, powermetrics, istats) and Python packages
(psutil, pandas, matplotlib, seaborn) to provide both textual and graphical insights about CPU performance and health.

Usage example:
    python cpu_monitoring.py

Requirements:
- macOS system
- External tools installed: osx-cpu-temp, istats, powermetrics (requires sudo)
- Python packages: psutil, pandas, matplotlib, seaborn
"""



import os
import psutil
import subprocess
import time
import re
import pandas as pd
import matplotlib.pyplot as plt
def get_cpu_temp_mac():
    print("🌡️ Getting CPU temperature via osx-cpu-temp...")
    try:
        output = subprocess.check_output(["osx-cpu-temp"]).decode("utf-8").strip()
        match = re.search(r"([\d.]+)", output)
        if match:
            temp_c = float(match.group(1))
            print(f"✅ CPU temperature found: {temp_c}°C")
            return temp_c
        else:
            print("⚠️ Unable to parse temperature output.")
            return None
    except Exception as e:
        print(f"❌ Error getting CPU temperature: {e}")
        return None

def monitor_until_cool(threshold=20.0, interval=5):
    print(f"⏳ Monitoring CPU temperature until below {threshold}°C...")
    while True:
        temp = get_cpu_temp_mac()
        if temp is not None:
            print(f"🌡️ Current CPU temperature: {temp}°C")
            if temp < threshold:
                print("✅ Temperature is below threshold. Stopping monitoring.")
                break
        else:
            print("⚠️ Failed to get temperature. Retrying...")
        time.sleep(interval)

def monitor_cpu_usage(duration_seconds=10, interval_seconds=1):
    print(f"⚙️ Monitoring CPU usage per core for {duration_seconds} seconds...")
    start_time = time.time()
    while (time.time() - start_time) < duration_seconds:
        cpu_usage = psutil.cpu_percent(percpu=True)
        usage_str = " | ".join([f"Core {i+1}: {usage}%" for i, usage in enumerate(cpu_usage)])
        print(f"🖥️ CPU Usage: {usage_str}")
        time.sleep(interval_seconds)

def count_cpu_cores():
    print("💡 Detecting CPU cores...")
    physical = psutil.cpu_count(logical=False)
    logical = psutil.cpu_count(logical=True)
    total = os.cpu_count()
    print(f"🧮 Total CPU cores (os.cpu_count()): {total}")
    print(f"🔧 Physical cores (psutil): {physical}")
    print(f"🔧 Logical cores (psutil): {logical}")

def is_apple_silicon():
    print("🍎 Checking if machine is Apple Silicon (arm64)...")
    try:
        arch = subprocess.check_output(['uname', '-m']).decode().strip()
        print(f"🖥️ Architecture: {arch}")
        return arch == 'arm64'
    except Exception as e:
        print(f"❌ Error detecting architecture: {e}")
        return False

def get_fan_speed_mac():
    print("🌬️ Getting fan speed...")
    try:
        result = subprocess.check_output(['istats', 'fan', '--value-only']).decode().strip()
        rpm = int(result.split()[0])
        print(f"✅ Fan speed: {rpm} RPM")
        return rpm
    except Exception as e:
        print(f"❌ Failed to get fan speed: {e}")
        return None

def get_cpu_temperature_powermetrics():
    print("🌡️ Getting CPU temperature using powermetrics (requires sudo)...")
    try:
        output = subprocess.check_output(
            ['sudo', 'powermetrics', '--samplers', 'smc', '-n', '1'],
            stderr=subprocess.STDOUT
        ).decode()

        match = re.search(r'CPU die temperature:\s+([0-9.]+) C', output)
        if match:
            temp = float(match.group(1))
            print(f"✅ CPU temperature from powermetrics: {temp}°C")
            return temp
        else:
            print("⚠️ CPU temperature not found in powermetrics output.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running powermetrics: {e.output.decode()}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def os_get_cpu():
    print("🖥️ Getting CPU status via 'top' command...")
    output = subprocess.getoutput("top -l 1 | head -n 10")  # macOS specific
    print(output)
    return output

def os_get_cpu_df():
    print("📊 Parsing 'top' output to DataFrame...")
    output = subprocess.getoutput("top -l 1 | head -n 10")
    lines = output.split('\n')
    data = {}

    for line in lines:
        if ':' in line:
            key, values = line.split(':', 1)
            key = key.strip()
            split_values = [v.strip() for v in values.split(',') if v.strip()]

            for item in split_values:
                match = re.match(r'([0-9.]+)([A-Za-z%]*)\s*(.*)', item)
                if match:
                    num = match.group(1)
                    unit = match.group(2)
                    desc = match.group(3).strip()
                    label = f"{key} - {desc}" if desc else key
                    value = f"{num}{unit}" if unit else num
                    data[label] = value
                else:
                    data[f"{key} - raw"] = item

    df = pd.DataFrame([data])
    print("✅ DataFrame created from top output:")
    print(df)
    return df

def monitor_cpu_usage_plt_multiple_runs(num_runs=5, interval_seconds=1,plot=False):
    """
    מבצעת מדידה של שימוש המעבד לכל הליבות במספר ריצות רצופות,
    מחזירה DataFrame ומציירת גרף שטח (area plot) של השימוש לאורך הריצות.

    :param num_runs: מספר המדידות (מספר ריצות רצופות).
    :param interval_seconds: מרווח בין כל מדידה בשניות.
    :return: DataFrame עם שימוש CPU לכל ליבה בכל מדידה.
    """
    print(f"⚙️ Starting CPU usage monitoring for {num_runs} runs with {interval_seconds} sec interval...")
    all_usage = []

    for run in range(num_runs):
        cpu_usage = psutil.cpu_percent(percpu=True)
        usage_str = " | ".join([f"Core {i+1}: {usage}%" for i, usage in enumerate(cpu_usage)])
        print(f"Run {run+1}/{num_runs}: {usage_str}")
        all_usage.append(cpu_usage)
        time.sleep(interval_seconds)

    # יצירת DataFrame מהתוצאות
    df = pd.DataFrame(all_usage, columns=[f"Core {i+1}" for i in range(len(all_usage[0]))])
    print("✅ CPU usage DataFrame created:")
    print(df)

    # ציור גרף שטח
    plt.figure(figsize=(12, 6))
    df.plot.area(alpha=0.5)
    plt.title(f'CPU Usage per Core Over {num_runs} Runs')
    plt.xlabel('Run Number')
    plt.ylabel('CPU Usage (%)')
    plt.legend(loc='upper right', title='CPU Cores')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    return df
import seaborn as sns
import matplotlib.pyplot as plt

def monitor_cpu_multiple_charts(num_runs=15, interval_seconds=1):
    """
    מדידת שימוש CPU לכל הליבות במשך מספר ריצות,
    יצירת 3 גרפים באותה חלונית:
    1. גרף שטח מוערם (stacked area)
    2. גרף קווי (line plot)
    3. גרף עמודות ממוצע שימוש לכל ליבה
    """
    print(f"⚙️ Monitoring CPU usage for {num_runs} runs, interval {interval_seconds}s...")
    all_usage = []

    for run in range(num_runs):
        cpu_usage = psutil.cpu_percent(percpu=True)
        print(f"Run {run+1}/{num_runs}: " + " | ".join([f"Core {i+1}: {usage}%" for i, usage in enumerate(cpu_usage)]))
        all_usage.append(cpu_usage)
        time.sleep(interval_seconds)

    df = pd.DataFrame(all_usage, columns=[f"Core {i+1}" for i in range(len(all_usage[0]))])

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(3, 1, figsize=(14, 15), sharex=True)

    # 1. גרף שטח מוערם
    axes[0].stackplot(df.index, df.T, labels=df.columns, alpha=0.7)
    axes[0].set_title("Stacked Area Chart of CPU Usage per Core")
    axes[0].set_ylabel("CPU Usage (%)")
    axes[0].legend(loc="upper left")

    # 2. גרף קווי לכל ליבה
    sns.lineplot(data=df, ax=axes[1])
    axes[1].set_title("Line Plot of CPU Usage per Core")
    axes[1].set_ylabel("CPU Usage (%)")

    # 3. גרף עמודות ממוצע שימוש לכל ליבה
    mean_usage = df.mean()
    sns.barplot(x=mean_usage.index, y=mean_usage.values, ax=axes[2], palette="viridis")
    axes[2].set_title("Average CPU Usage per Core")
    axes[2].set_ylabel("Average CPU Usage (%)")
    axes[2].set_xlabel("CPU Core")

    plt.tight_layout()
    plt.show()

    return df
def main():
    # בדיקת סוג המעבד
    apple_silicon = is_apple_silicon()
    print(f"Apple Silicon? {apple_silicon}")

    # ספירת ליבות
    count_cpu_cores()

    # מדידת טמפרטורה עם osx-cpu-temp
    temp = get_cpu_temp_mac()
    print(f"CPU Temperature (osx-cpu-temp): {temp}")

    # מדידת טמפרטורה עם powermetrics (דורש סודו)
    temp_powermetrics = get_cpu_temperature_powermetrics()
    print(f"CPU Temperature (powermetrics): {temp_powermetrics}")

    # מדידת מהירות מאוורר
    fan_speed = get_fan_speed_mac()
    print(f"Fan Speed: {fan_speed} RPM")

    # מדידת שימוש CPU ל-10 שניות (הדפסת לייב)
    monitor_cpu_usage(duration_seconds=10, interval_seconds=1)

    # מדידת שימוש CPU במספר ריצות ויצירת גרף
    df_usage = monitor_cpu_usage_plt_multiple_runs(num_runs=5, interval_seconds=1)

    # מדידת שימוש CPU עם שלושה גרפים

    # קריאת סטטוס CPU מ-top
    top_output = os_get_cpu()

    # יצירת DataFrame מ-top
    df_top = os_get_cpu_df()

    # ניטור טמפרטורה עד לקרר מ-20 מעלות (זה יכול לקחת זמן, תשחרר או תשנה את הסף)
    # monitor_until_cool(threshold=20.0, interval=5)

if __name__ == "__main__":
    main()
