
import streamlit as st
import pymongo
import hmac
import hashlib
from datetime import datetime, time

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")  # Ensure this path matches where you've saved your CSS file

# Initialize connection to MongoDB
def init_connection():
    client = pymongo.MongoClient(st.secrets["mongo_uri"])
    return client

client = init_connection()
db = client[st.secrets["mongo"]["database_name"]]

def check_password():
    """Check the password and store the state in session if correct."""
    if 'password_verified' not in st.session_state or not st.session_state['password_verified']:
        with st.sidebar.form(key='Password_form'):
            password_input = st.text_input("Entrez votre mot de passe :", type="password", placeholder="Tapez votre mot de passe ici")
            submit_button = st.form_submit_button("Soumettre")
            if submit_button and password_input:
                hashed_input = hmac.new(
                    key=st.secrets["secret_key"].encode(),
                    msg=password_input.encode(),
                    digestmod=hashlib.sha256
                ).hexdigest()
                if hmac.compare_digest(hashed_input, st.secrets["password_hash"]):
                    st.session_state['password_verified'] = True
                else:
                    st.error("Mot de passe incorrect. Veuillez réessayer.")
                    return False
    return st.session_state.get('password_verified', False)

if not check_password():
    st.stop()

st.image("images/logo.jpg", width=100)
st.title("Questionnaire de Dépistage du Spectre de l'Autisme de Haut Niveau de Fonctionnement (ASSQ)")

nom_enfant = st.sidebar.text_input("Nom de l'enfant :")
date_naissance_enfant = st.sidebar.date_input("Date de naissance de l'enfant :", datetime.now())
nom_observateur = st.sidebar.text_input("Nom de l'observateur :")
date_observation = st.sidebar.date_input("Date de l'observation :", datetime.now())

st.write("Cet enfant se distingue des autres enfants de son âge de la manière suivante :")

# Liste des questions
# Liste des questions
questions = [
    "Est vieux jeu ou précoce",
    "Est considéré comme un 'professeur excentrique' par les autres enfants",
    "Vit quelque peu dans son propre monde avec des intérêts intellectuels idiosyncrasiques restreints",
    "Accumule des faits sur certains sujets (bonne mémoire factuelle) mais ne comprend pas vraiment leur sens",
    "Comprend littéralement le langage ambigu et métaphorique",
    "A un style de communication déviant avec un langage formel, pointilleux, vieux jeu ou 'robotique'",
    "Invente des mots et expressions idiosyncrasiques",
    "A une voix ou une parole différente",
    "Exprime des sons involontairement ; se racle la gorge, grogne, claque, pleure ou crie",
    "Est étonnamment bon dans certains domaines et étonnamment mauvais dans d'autres",
    "Utilise librement le langage mais échoue à s'ajuster pour s'adapter aux contextes sociaux ou aux besoins des différents auditeurs",
    "Manque d'empathie",
    "Fait des remarques naïves et embarrassantes",
    "A un style de regard déviant",
    "Souhaite être sociable mais échoue à établir des relations avec les pairs",
    "Peut être avec d'autres enfants mais seulement selon ses propres termes",
    "Manque de meilleur ami",
    "Manque de bon sens",
    "Est mauvais dans les jeux : n'a aucune idée de la coopération en équipe, marque des 'buts contre son camp'",
    "A des mouvements ou des gestes maladroits, mal coordonnés, gauches, embarrassants",
    "A des mouvements involontaires du visage ou du corps",
    "A des difficultés à compléter des activités quotidiennes simples à cause de la répétition compulsive de certaines actions ou pensées",
    "A des routines spéciales : insiste sur l'absence de changement",
    "Montre un attachement idiosyncrasique aux objets",
    "Est intimidé par les autres enfants",
    "A une expression faciale remarquablement inhabituelle",
    "A une posture remarquablement inhabituelle"
]
reponses = ["Jamais", "Parfois", "Tout le temps"]

answers = {question: st.select_slider(question, options=reponses) for question in questions}

if st.sidebar.button('Envoyer les réponses'):
    # Convert date to datetime for MongoDB operations
    date_naissance_enfant_dt = datetime.combine(date_naissance_enfant, time.min)
    date_observation_dt = datetime.combine(date_observation, time.min)
    
    existing_entry = db.responses.find_one({
        "nom_enfant": nom_enfant,
        "date_observation": date_observation_dt
    })

    if existing_entry:
        st.warning("Un enregistrement pour cet enfant et cette observation existe déjà.")
    else:
        responses_collection = db.responses
        response_data = {
            "nom_enfant": nom_enfant,
            "date_naissance_enfant": date_naissance_enfant_dt,
            "nom_observateur": nom_observateur,
            "date_observation": date_observation_dt,
            "answers": answers
        }
        responses_collection.insert_one(response_data)
        st.success("Merci pour vos réponses.")
        if 'password_verified' in st.session_state:
            del st.session_state['password_verified']  # Clear the password session state after successful submission

if st.sidebar.button("Réinitialiser"):
    if 'password_verified' in st.session_state:
        del st.session_state['password_verified']
    st.experimental_rerun()
