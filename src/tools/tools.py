import os
import requests
from langchain_core.tools import tool


@tool
def calculate_travel_costs(
    distance_km: float, consumption_per_100km: float = 10.0, fuel_price: float = 1100.0
):
    """
    Calcula el costo estimado de combustible para un viaje.
    distance_km: Distancia total del viaje en kilómetros.
    consumption_per_100km: Litros que consume el vehículo cada 100km (defecto 10.0).
    fuel_price: Precio actual del litro de nafta.
    """
    liters_needed = (distance_km / 100) * consumption_per_100km
    total_cost = liters_needed * fuel_price

    return {
        "liters_needed": round(liters_needed, 2),
        "estimated_cost_ars": round(total_cost, 2),
        "notes": "Cálculo basado en consumo promedio y precios actuales.",
    }


@tool
def get_weather_forecast(city: str):
    """
    Obtiene el clima actual de una ciudad para evaluar si un evento al aire libre es viable.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY no configurada en el entorno."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        advice = (
            "Ideal para tocar al aire libre."
            if temp > 18 and "lluvia" not in desc.lower()
            else "Considerar lugar techado o contingencia por clima."
        )

        return (
            f"Clima en {city} (vía OpenWeather): {temp}°C, {desc}. Sugerencia: {advice}"
        )

    except Exception:
        return (
            f"No se pudo obtener el clima para {city}. Verifica el nombre de la ciudad."
        )
