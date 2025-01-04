import streamlit as st
import random
import requests
from PIL import Image

# Clé API OpenWeatherMap
API_KEY = '0dfa745bce9027a692ecac8a8d9f1c2a'

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=fr"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
    return None

def choisir_vetements_par_meteo(meteo, categories):
    temperature = meteo['temperature']
    description = meteo['description'].lower()
    look = []

    if temperature < 10:
        look.append(random.choice(categories['vestes et monteaux']))
        look.append(random.choice(categories['pentalons']))
        look.append(random.choice(categories['chaussures']))
    elif 10 <= temperature < 20:
        look.append(random.choice(categories['blouses']))
        look.append(random.choice(categories['pentalons']))
        look.append(random.choice(categories['chaussures']))
    else:
        look.append(random.choice(categories['tops']))
        look.append(random.choice(categories['jupes']))
        look.append(random.choice(categories['chaussures']))

    look.append(random.choice(categories['accessoires']))
    return look

# Interface utilisateur Streamlit
st.title("Look du jour")

city = st.text_input("Entrez la ville", "Algérie")

if city:
    meteo = get_weather(city)
    if not meteo:
        st.error("❌ Impossible de récupérer la météo.")
    else:
        st.write(f"Météo à {city} : {meteo['description'].capitalize()} - {meteo['temperature']}°C")
        
        categories = {
            "blouses": ["blouse1.jpg", "blouse2.jpg"],
            "pentalons": ["pantalon1.jpg", "pantalon2.jpg"],
            "vestes et monteaux": ["veste1.jpg", "veste2.jpg"],
            "chaussures": ["chaussure1.jpg", "chaussure2.jpg"],
            "tops": ["top1.jpg", "top2.jpg"],
            "jupes": ["jupe1.jpg", "jupe2.jpg"],
            "accessoires": ["accessoire1.jpg", "accessoire2.jpg"]
        }

        look = choisir_vetements_par_meteo(meteo, categories)
        st.write("Voici votre look du jour :")
        
        for i, vetement in enumerate(look):
            st.image(vetement, caption=f"Vêtement {i+1}", width=300)
