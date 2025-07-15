import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io
import os

# API Setup
API_KEY = "9e65e8d21bc6755035eef6a1c6977407"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
is_celsius = True

# Mapping weather conditions to theme
weather_theme = {
    'Clear': {
        'bg': '#87CEEB',
        'image': 'images/sunny.png'
    },
    'Rain': {
        'bg': '#3f2b4f',
        'image': 'images/rainy.png'
    },
    'Thunderstorm': {
        'bg': '#2c2c2c',
        'image': 'images/thunderstorm.png'
    },
    'Clouds': {
        'bg': '#d3d3d3',
        'image': 'images/cloudy.png'
    },
    'Drizzle': {
        'bg': '#5f4f64',
        'image': 'images/rainy.png'
    },
    'Mist': {
        'bg': '#aab9c8',
        'image': 'images/cloudy.png'
    },
    'Haze': {
        'bg': '#9e9e9e',
        'image': 'images/cloudy.png'
    },
    'Wind': {
        'bg': '#a0d6ff',
        'image': 'images/windy.png'
    }
}

# Function to fetch weather and update UI
def get_weather():
    global is_celsius

    zipcode = city_entry.get()
    country_code = "IN"

    if not zipcode:
        messagebox.showwarning("Input Error", "Please enter a valid pincode.")
        return

    params = {
        'zip': f"{zipcode},{country_code}",
        'appid': API_KEY,
        'units': 'metric' if is_celsius else 'imperial'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data['cod'] != 200:
            messagebox.showerror("Error", f"{data['message'].capitalize()}")
            return

        condition = data['weather'][0]['main']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        desc = data['weather'][0]['description']

        # Set visuals
        theme = weather_theme.get(condition, weather_theme['Clear'])
        app.configure(bg=theme['bg'])
        main_frame.configure(bg=theme['bg'])
        result_label.configure(bg=theme['bg'])
        city_label.configure(bg=theme['bg'])
        weather_icon.configure(bg=theme['bg'])

        # Load weather image (FIX: use Resampling.LANCZOS instead of ANTIALIAS)
        icon_path = theme['image']
        if os.path.exists(icon_path):
            image = Image.open(icon_path)
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            icon_img = ImageTk.PhotoImage(image)
            weather_icon.config(image=icon_img)
            weather_icon.image = icon_img

        # Update result text
        temp_unit = "°C" if is_celsius else "°F"
        wind_unit = "m/s" if is_celsius else "mph"

        result = (
            f"Condition: {desc.title()}\n"
            f"Temperature: {temperature}{temp_unit}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} {wind_unit}"
        )
        result_label.config(text=result)

    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch weather.\n\n{str(e)}")

# Toggle Celsius/Fahrenheit
def toggle_unit():
    global is_celsius
    is_celsius = not is_celsius
    get_weather()

# GUI Setup
app = tk.Tk()
app.title("Dynamic Weather App 🌤️")
app.geometry("460x520")
app.resizable(False, False)

main_frame = tk.Frame(app, bg="#f0f0f0")
main_frame.pack(fill="both", expand=True)

city_label = tk.Label(main_frame, text="Enter Pincode:", font=("Arial", 12), bg="#f0f0f0")
city_label.pack(pady=10)

city_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
city_entry.pack(pady=5)

weather_icon = tk.Label(main_frame, bg="#f0f0f0")
weather_icon.pack(pady=10)

result_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="#f0f0f0", justify="left")
result_label.pack()

button_frame = tk.Frame(main_frame, bg="#f0f0f0")
button_frame.pack(pady=15)

tk.Button(button_frame, text="Get Weather", command=get_weather).pack(side="left", padx=10)
tk.Button(button_frame, text="Switch °C/°F", command=toggle_unit).pack(side="left", padx=10)

app.mainloop()
