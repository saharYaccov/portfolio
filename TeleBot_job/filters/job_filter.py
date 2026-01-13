KEYWORDS = [
    "data",
    "analyst",
    "scientist",
    "machine learning",
    "ml",
    "bi",
    "data labeling",
    "data tagging",

]

EXCLUDE = [
    "senior",
    "lead",
    "principal"
]

def is_relevant(job: dict) -> bool:
    title = job["title"].lower()

    if any(word in title for word in EXCLUDE):
        return False

    return any(word in title for word in KEYWORDS)
