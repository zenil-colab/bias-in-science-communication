import json
import pandas as pd
from collections import Counter

# === CONFIG === #
JSON_PATHS = {
    "Wired": "wired_people_mentions_final.json",
    "New Scientist": "NS_people_mentions_final.json",
    "Quanta": "quanta_ner_people_final.json",
}

dead_scientists = {
    "Albert Einstein","Einstein","Isaac Newton","Newton","Stephen Hawking","Hawking",
    "Richard Feynman","Feynman","Erwin Schrödinger","Schrödinger","Marie Curie",
    "Ada Lovelace","Alan Turing","Niels Bohr","Bohr","Max Planck","Planck","Galileo"
}

non_scientists = {
    "Bill Nelson","Lo Presti","Robert F","Jared Isaacman","Gutiérrez Alvarado","RFK Jr.","RFK Jr",
    "Donald Trump","Elon Musk","Joe Biden","Robert F. Kennedy Jr.","Lauren Goode","Gideon Lichfield",
    "Katie Drummond","Michael Calore","Jamie Beard","De Bruyne","Zach Weinersmith","Karmela Padavic-Callaghan",
    "Leah Crane","Alex Wilkins","Matthew Sparkes","Michael Brooks","Richard Webb","Anil Ananthaswamy",
    "Chelsea Whyte","Thomas Lewton","Stuart Clark","ByKarmela Padavic-Callaghan","Donna Lu","Joshua Howgego",
    "Daniel Cossins","Timothy Revell","Lucy Reading-Ikkanda","Samuel Velasco","Merrill Sherman",
    "Olena Shmahalo","Kristina Armitage","Contributing Writer","Thomas Lin","John Rennie",
    "Steve Strogatz","Charles Michelet","Puzzle Columnist","Merrill Sherman/Quanta Magazine",
    "Merrill Sherman","Contributing Correspondent","Philipp Ammon","Matt Carlstrom","Dana Bialek",
    "Emily Buder","Susan Valot","Lucy Reading-Ikkandafor","Math Editor","Stockton Rush","Robert F. Kennedy Jr",
    "Edwin Hubble","Ali Zaidi","Suni Williams","Ron DeSantis","Matthew Kacsmaryk","Gavin Newsom","ByLeah Crane",
    "Daniel Cossins","de Rham","James Clerk Maxwell","Enrico Sacchetti","Werner Heisenberg","Paul Dirac",
    "ByAlex Wilkins","David Bennett","Boris Johnson","Ben Smith","Paul Erdős","Ellen Horne","David Hilbert",
    "Dan Pagefor","Richie Johnson","Polly Stryker","Kurt Gödel","Jaki King","Bertrand Odom-Reed","Philip Ball",
    "Peter Higgs","Dan Hooper","Sabine Hossenfelder","David Stock","Eugene Wigner","van Steenbergen","Jeanne Calment"
}


# === FUNCTIONS === #
def aggregate_mentions(path):
    counter = Counter()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for article in data:
        for name, count in article.get("mention_counts", {}).items():
            if (
                isinstance(name, str)
                and " " in name.strip()
                and name not in dead_scientists
                and name not in non_scientists
            ):
                counter[name.strip()] += count
    return counter


def merge_lastname_variants(counter):
    merged = Counter(counter)
    for name in list(counter.keys()):
        parts = name.split()
        if len(parts) == 1:
            for candidate in counter:
                if parts[0] in candidate.split() and candidate != name:
                    merged[candidate] += counter[name]
                    merged.pop(name, None)
                    break
    return merged


def get_top10_percent(path, outlet):
    """Compute top-10 living scientists per outlet, with percentages."""
    counts = aggregate_mentions(path)
    merged = merge_lastname_variants(counts)
    df = pd.DataFrame(merged.items(), columns=["Scientist", "Mentions"])
    df = df.sort_values("Mentions", ascending=False).head(10).reset_index(drop=True)

    # Convert to percentage of total Top-10 mentions
    total_mentions_top10 = df["Mentions"].sum()
    df["Percentage"] = (df["Mentions"] / total_mentions_top10 * 100).round(2)
    df["Outlet"] = outlet
    return df


# === PROCESS === #
wired_top = get_top10_percent(JSON_PATHS["Wired"], "Wired")
ns_top = get_top10_percent(JSON_PATHS["New Scientist"], "New Scientist")
quanta_top = get_top10_percent(JSON_PATHS["Quanta"], "Quanta")

# === Combined Table === #
table = pd.DataFrame({
    "#": list(range(1, 11)),
    "Wired": wired_top["Scientist"].tolist(),
    "% (Wired)": wired_top["Percentage"].tolist(),
    "New Scientist": ns_top["Scientist"].tolist(),
    "% (NS)": ns_top["Percentage"].tolist(),
    "Quanta": quanta_top["Scientist"].tolist(),
    "% (Quanta)": quanta_top["Percentage"].tolist(),
})

print(table.to_markdown(index=False))
table.to_csv("top10_scientists_percentages.csv", index=False)
print("\nSaved: top10_scientists_percentages.csv")
