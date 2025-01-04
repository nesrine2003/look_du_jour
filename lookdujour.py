import os
import random
import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Clé API OpenWeatherMap
API_KEY = '0dfa745bce9027a692ecac8a8d9f1c2a'

# Dictionnaire des catégories de vêtements
categories = {  
    "blouses": ["ARMOIRE/blouses/bl (1).jpg"],
    "pentalons": ["ARMOIRE/pentalons/pen (1).jpg"],
    "vestes et monteaux": ["ARMOIRE/vestes et monteaux/v&m (1).jpg"],
    "chaussures": ["ARMOIRE/chaussures/ch (1).jpg"],
    "tops": ["ARMOIRE/tops/top (1).jpg"],
    "jupes": ["ARMOIRE/jupes/ju (1).jpg"],
    "accessoires": ["ARMOIRE/accessoires/ac (1).jpg"]
}

def get_weather(city):
    """ Récupère la météo d'une ville via l'API OpenWeatherMap. """
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
    """ Sélectionne des vêtements en fonction de la météo. """
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

# Interface utilisateur avec Streamlit
st.title("Look du Jour 👗👔")

city = st.text_input("Entrez le nom de votre ville :", "Alger")

if st.button("Générer Look"):
    meteo = get_weather(city)
    
    if not meteo:
        st.error("❌ Impossible de récupérer la météo.")
    else:
        st.subheader(f"Météo à {city}")
        st.write(f"🌤 {meteo['description'].capitalize()} - 🌡 {meteo['temperature']}°C")

        look = choisir_vetements_par_meteo(meteo, categories)

        st.subheader("🛍 Votre look du jour :")
        for i, vetement in enumerate(look):
            if os.path.exists(vetement):
                st.image(vetement, caption=f"Vêtement {i+1}", width=300)
            else:
                st.warning(f"⚠ Image introuvable : {vetement}")
