import requests
import tkinter as tk
from tkinter import ttk, messagebox

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App - Ritik Jain")
        self.root.geometry("400x400")

        style = ttk.Style()
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5")
        style.configure("TEntry", fieldbackground="#fff", borderwidth=1, relief="solid")
        style.configure("TButton", background="#007bff", foreground="#007bff", padding=(10, 5), font=('Arial', 10, 'bold'))
        style.configure("TListbox", background="#fff", borderwidth=1, relief="solid")

        self.main_frame = ttk.Frame(root, style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.label = ttk.Label(self.main_frame, text="Enter City:", style="TLabel")
        self.label.pack(pady=10)

        self.city_entry = ttk.Entry(self.main_frame, style="TEntry")
        self.city_entry.pack(pady=10)

        self.autocomplete_results = tk.Listbox(self.main_frame, selectbackground="#007bff", selectforeground="#fff", borderwidth=1, relief="solid", exportselection=False)
        self.autocomplete_results.pack(pady=10)

        self.get_weather_button = ttk.Button(self.main_frame, text="Get Weather", command=self.get_weather, style="TButton")
        self.get_weather_button.pack(pady=10)

        self.root.bind('<KeyRelease>', self.autocomplete)

    def autocomplete(self, event):
        input_text = self.city_entry.get()

        if len(input_text) > 2:
            suggestions = self.fetch_autocomplete_suggestions(input_text)

            self.autocomplete_results.delete(0, tk.END)

            for suggestion in suggestions:
                self.autocomplete_results.insert(tk.END, suggestion)

    def fetch_autocomplete_suggestions(self, prefix):
        api_key = '8ab0c99327e85a3a42ce55eab49633cf'
        api_url = f'http://api.openweathermap.org/data/2.5/find?q={prefix}&type=like&mode=json&appid={api_key}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()

            cities_data = response.json().get('list', [])
            suggestions = [city['name'] for city in cities_data]

            return suggestions

        except requests.exceptions.RequestException as e:
            print(f"Error fetching autocomplete data: {e}")
            return []

    def get_weather(self):
        city = self.city_entry.get()
        weather_data = self.fetch_weather_data(city)

        if weather_data:
            messagebox.showinfo("Weather Result", f"Weather in {city}:\nMain Weather: {weather_data['main_weather']}\nDescription: {weather_data['description']}\nTemperature: {weather_data['temperature']:.2f} °C")
        else:
            messagebox.showerror("City Not Found", f"City {city} not found. Please try again.")

    def fetch_weather_data(self, city):
        api_key = '8ab0c99327e85a3a42ce55eab49633cf'
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()

            weather_data = response.json()

            if weather_data['cod'] == '404':
                return None

            main_weather = weather_data['weather'][0]['main']
            description = weather_data['weather'][0]['description']
            temperature_kelvin = weather_data['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15

            return {'main_weather': main_weather, 'description': description, 'temperature': temperature_celsius}

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
