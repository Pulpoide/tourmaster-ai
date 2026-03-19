from langchain_core.tools import tool

@tool
def calculate_travel_costs(distance_km: float, consumption_per_100km: float = 10.0, fuel_price: float = 1100.0):
    """
    Calcula el costo estimado de combustible para un viaje.
    distance_km: Distancia total del viaje en kilómetros.
    consumption_per_100km: Litros que consume el vehículo cada 100km (defecto 10.0 para una Partner/Kangoo).
    fuel_price: Precio actual del litro de nafta en Argentina.
    """
    liters_needed = (distance_km / 100) * consumption_per_100km
    total_cost = liters_needed * fuel_price
    
    return {
        "liters_needed": round(liters_needed, 2),
        "estimated_cost_ars": round(total_cost, 2),
        "notes": "Cálculo basado en consumo promedio y precios actuales."
    }

@tool
def get_weather_forecast(city: str):
    """Simula el pronóstico del tiempo para una ciudad."""
    # Aquí voy a conectar una API real como OpenWeatherMap en el futuro
    return f"El pronóstico para {city} es de 24°C, despejado. Ideal para cargar instrumentos o tocar al aire libre."