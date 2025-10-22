import json
import numpy as np
import pandas as pd

# Paths to your JSON exports
JSON_PATHS = {
    'Wired': 'wired_people_mentions_final.json',
    'Quanta': 'quanta_ner_people_final.json',
    'NewScientist': 'NS_people_mentions_final.json'
}

# Lists of names to exclude
dead_scientists = {
    "Albert Einstein","Einstein","Isaac Newton","Newton","Stephen Hawking",
    "Hawking","Richard Feynman","Feynman","Erwin Schrödinger","Schrödinger",
    "Marie Curie","Ada Lovelace","Alan Turing","Niels Bohr","Bohr",
    "Max Planck","Planck","Galileo"
}
non_scientists = {"Donald Trump","Elon Musk","Joe Biden"}

def load_counts(path):
    counts = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    for art in data:
        for person, c in art.get('mention_counts', {}).items():
            if ' ' in person and person not in dead_scientists and person not in non_scientists:
                counts.append(c)
    return np.array(counts, dtype=float)

# Gini coefficient function
def gini(arr):
    arr = np.sort(arr)
    n = len(arr)
    index = np.arange(1, n+1)
    return (2 * np.sum(index * arr) / (n * np.sum(arr)) - (n+1)/n)

# Build the summary table
rows = []
for source, path in JSON_PATHS.items():
    arr = load_counts(path)
    p50 = np.percentile(arr, 50)
    p90 = np.percentile(arr, 90)
    g  = gini(arr)
    rows.append((source, p50, p90, g))

df = pd.DataFrame(rows, columns=['Source','P50','P90','Gini'])
df = df.set_index('Source').loc[['Wired','Quanta','NewScientist']]
print(df)
