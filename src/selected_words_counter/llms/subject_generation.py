import random

# Define categories and themes for generating diverse essay topics
themes = [
    "Maatschappij",
    "Politiek",
    "Technologie",
    "Milieu",
    "Gezondheid",
    "Wetenschap",
    "Onderwijs",
    "Kunst",
    "Cultuur",
    "Geschiedenis",
    "Psychologie",
    "Sport",
    "Economie",
    "Filosofie",
    "Reizen",
    "Literatuur",
    "Relaties",
    "Sociale media",
    "Dierenwelzijn",
    "Toekomst",
]

questions = [
    r"Hoe verandert {} ons dagelijks leven?",
    r"Wat is de rol van {} in de moderne samenleving?",
    r"De toekomst van {}: hoe ziet die eruit?",
    r"Hoe beïnvloedt {} de jeugd van tegenwoordig?",
    r"Wat zijn de voordelen en nadelen van {}?",
    r"Hoe kunnen we {} verbeteren?",
    r"Waarom is {} belangrijk voor ons?",
    r"De ethiek van {}: waar ligt de grens?",
    r"Hoe kunnen we de negatieve effecten van {} beperken?",
    r"Wat zijn de uitdagingen van {} in de komende jaren?",
    r"Is {} goed of slecht voor onze samenleving?",
    r"De geschiedenis van {}: hoe heeft het zich ontwikkeld?",
    r"Hoe kan {} ons helpen om duurzamer te leven?",
    r"De invloed van {} op onze cultuur",
    r"Wat kunnen we leren van {}?",
    r"Is {} noodzakelijk in het onderwijs?",
    r"Hoe beïnvloedt {} onze mentale gezondheid?",
    r"De relatie tussen {} en geluk",
    r"Hoe verandert {} de manier waarop we werken?",
    r"Welke rol speelt {} in internationale betrekkingen?",
]


def sample_dutch_subject():
    return random.choice(questions).format(random.choices(themes)[0])
