import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import time

# Page Configuration
st.set_page_config(
    page_title="Apple Weather",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Apple-style design
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }

    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 20px;
    }

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Header Styling */
    .header-section {
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }

    .header-section h1 {
        font-size: 3em;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .header-section p {
        font-size: 1.1em;
        opacity: 0.9;
    }

    /* Current Weather Card */
    .weather-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 40px;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        text-align: center;
        margin-bottom: 30px;
    }

    .weather-card h2 {
        font-size: 2.5em;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .weather-card p {
        font-size: 1.2em;
        opacity: 0.95;
        margin: 5px 0;
    }

    .temperature {
        font-size: 5em;
        font-weight: 300;
        margin: 20px 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    .condition-desc {
        font-size: 1.5em;
        opacity: 0.9;
        margin-bottom: 20px;
    }

    .details-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 15px;
        margin-top: 25px;
        padding-top: 25px;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
    }

    .detail-item {
        text-align: center;
    }

    .detail-label {
        font-size: 0.9em;
        opacity: 0.8;
        margin-bottom: 8px;
    }

    .detail-value {
        font-size: 1.4em;
        font-weight: 600;
    }

    /* Forecast Cards */
    .forecast-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin-top: 25px;
    }

    .forecast-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        transition: all 0.3s ease;
    }

    .forecast-card:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-5px);
    }

    .forecast-card h4 {
        font-size: 1.1em;
        margin-bottom: 10px;
        opacity: 0.9;
    }

    .forecast-card .temp {
        font-size: 1.8em;
        font-weight: 600;
        margin: 10px 0;
    }

    .forecast-card .condition {
        font-size: 0.9em;
        opacity: 0.8;
    }

    /* Input Section */
    .input-section {
        display: grid;
        grid-template-columns: 1fr 1fr auto;
        gap: 15px;
        margin-bottom: 30px;
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.25) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }

    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.35) !important;
        transform: translateY(-2px) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* Error and Success Messages */
    .stAlert {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# API Key
API_KEY = "caa4bac5ba668511b0df8fae783309f4"

# State-City Data
india_states_cities = {
    "Uttar Pradesh": ["Lucknow", "Varanasi", "Jaunpur", "Kanpur", "Agra", "Prayagraj", "Noida"],
    "Delhi": ["New Delhi"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jodhpur", "Ajmer"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur"],
    "West Bengal": ["Kolkata", "Darjeeling", "Siliguri"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangalore"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
    "Punjab": ["Amritsar", "Ludhiana", "Chandigarh"],
    "Telangana": ["Hyderabad", "Warangal"],
    "Goa": ["Panaji"]
}


def get_weather_data(city, state):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},{state},IN&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("cod") != "200":
            return None

        return data
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None


def display_current_weather(data):
    """Display current weather information"""
    if not data:
        return

    current = data['list'][0]
    city_name = data['city']['name']
    country = data['city']['country']

    temp = current['main']['temp']
    feels_like = current['main']['feels_like']
    desc = current['weather'][0]['description'].title()
    humidity = current['main']['humidity']
    wind = current['wind']['speed']
    pressure = current['main']['pressure']
    visibility = current.get('visibility', 10000) / 1000

    # Display Current Weather Card
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
        <div class="weather-card">
            <h2>{city_name}, {country}</h2>
            <div class="temperature">{int(temp)}°</div>
            <div class="condition-desc">{desc}</div>
            <p>Feels like <strong>{int(feels_like)}°C</strong></p>

            <div class="details-grid">
                <div class="detail-item">
                    <div class="detail-label">💧 Humidity</div>
                    <div class="detail-value">{humidity}%</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">💨 Wind Speed</div>
                    <div class="detail-value">{wind:.1f} m/s</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">🔼 Pressure</div>
                    <div class="detail-value">{pressure} mb</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">👁️ Visibility</div>
                    <div class="detail-value">{visibility:.1f} km</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">⬆️ Max Temp</div>
                    <div class="detail-value">{int(current['main']['temp_max'])}°C</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">⬇️ Min Temp</div>
                    <div class="detail-value">{int(current['main']['temp_min'])}°C</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def display_forecast(data):
    """Display 5-day forecast"""
    if not data:
        return

    st.markdown("""
    <div style="margin-top: 40px;">
        <h3 style="color: white; font-size: 1.5em; margin-bottom: 20px;">📅 5-Day Forecast</h3>
    </div>
    """, unsafe_allow_html=True)

    # Create forecast data
    forecast_data = []
    for i in range(0, 40, 8):  # Every 8th forecast (daily)
        day = data['list'][i]
        date_str = day['dt_txt'].split(" ")[0]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%a, %b %d")

        temp = int(day['main']['temp'])
        max_temp = int(day['main']['temp_max'])
        min_temp = int(day['main']['temp_min'])
        condition = day['weather'][0]['main']

        forecast_data.append({
            'date': formatted_date,
            'temp': temp,
            'max': max_temp,
            'min': min_temp,
            'condition': condition
        })

    # Display forecast cards
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            if idx < len(forecast_data):
                day = forecast_data[idx]
                st.markdown(f"""
                <div class="forecast-card">
                    <h4>{day['date']}</h4>
                    <div class="temp">{day['temp']}°</div>
                    <div class="condition">{day['condition']}</div>
                    <p style="font-size: 0.8em; margin-top: 8px; opacity: 0.8;">
                        ⬆️ {day['max']}° ⬇️ {day['min']}°
                    </p>
                </div>
                """, unsafe_allow_html=True)


def main():
    # Header
    st.markdown("""
    <div class="header-section">
        <h1>🌤️ Apple Weather</h1>
        <p>Beautiful weather forecasting for India</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for settings
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        theme = st.radio("Theme", ["Light", "Dark"], label_visibility="collapsed")

    # Input Section
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        state = st.selectbox("📍 Select State", list(india_states_cities.keys()))

    with col2:
        cities = india_states_cities.get(state, [])
        city = st.selectbox("🏙️ Select City", cities)

    with col3:
        search_button = st.button("🔍 Get Weather", use_container_width=True)

    # Get and display weather
    if search_button or 'weather_data' in st.session_state:
        if search_button:
            st.session_state.weather_data = get_weather_data(city, state)

        if 'weather_data' in st.session_state and st.session_state.weather_data:
            # Display current weather
            display_current_weather(st.session_state.weather_data)

            # Display forecast
            display_forecast(st.session_state.weather_data)

            # Footer
            st.markdown("""
            <div style="text-align: center; margin-top: 50px; color: rgba(255,255,255,0.6); font-size: 0.9em;">
                <p>Data from OpenWeatherMap | © 2024 Apple Weather</p>
            </div>
            """, unsafe_allow_html=True)
        elif search_button:
            st.error("❌ Weather data not available for this location. Please try another city.")


if __name__ == "__main__":
    main()