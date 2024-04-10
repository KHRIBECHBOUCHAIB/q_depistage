import streamlit as st
# Load your logo image
logo = "images/logo.jpg"
st.image(logo, width=100)
# Titre de l'application
st.title("Questionnaire de Dépistage du Spectre de l'Autisme de Haut Niveau de Fonctionnement (ASSQ)")

# Collecte des informations sur l'enfant
nom_enfant = st.text_input("Nom de l'enfant :")
date_naissance_enfant = st.text_input("Date de naissance de l'enfant :")

# Collecte des informations sur l'observateur
nom_observateur = st.text_input("Nom de l'observateur :")
date_observation = st.text_input("Date de l'observation :")

st.write("Cet enfant se distingue des autres enfants de son âge de la manière suivante :")

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

# Réponses possibles
reponses = ["Non", "Un peu", "Oui"]

# Initialisation de la chaîne de caractères pour les réponses
reponses_texte = f"Nom de l'enfant : {nom_enfant}\nDate de naissance de l'enfant : {date_naissance_enfant}\nNom de l'observateur : {nom_observateur}\nDate de l'observation : {date_observation}\n\nRéponses au questionnaire :\n"

# Génération des questions et des sélecteurs de réponses
for question in questions:
    reponse = st.select_slider(question, options=reponses)
    reponses_texte += f"{question}: {reponse}\n"

# Bouton pour soumettre les réponses
if st.button('Envoyer les réponses'):
    st.success("Merci pour vos réponses. Vous pouvez désormais télécharger le document contenant vos réponses et nous le faire parvenir.")
    # Lien de téléchargement pour le texte des réponses
    st.download_button(label="Télécharger les réponses", data=reponses_texte, file_name="reponses_assq.txt", mime='text/plain')
