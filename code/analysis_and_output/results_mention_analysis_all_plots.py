import json
import numpy as np
import matplotlib.pyplot as plt
import os

# CONFIGURATION

# Paths to your JSON exports
JSON_PATHS = {
    'Wired': 'wired_people_mentions_final.json',
    'New Scientist': 'NS_people_mentions_final.json',
    'Quanta': 'quanta_ner_people_final.json'
}

# Brand color palette
palette = {
    'Wired':        '#1F77B4',
    'New Scientist':'#2CA02C',
    'Quanta':       '#D62728'
}

# People to exclude
dead_scientists = {
    "Albert Einstein", "Einstein", "Isaac Newton", "Newton",
    "Stephen Hawking", "Hawking", "Richard Feynman", "Feynman",
    "Erwin Schrödinger", "Schrödinger", "Marie Curie",
    "Ada Lovelace", "Alan Turing", "Niels Bohr", "Bohr",
    "Max Planck", "Planck", "Galileo"
}
non_scientists = {"Donald Trump", "Elon Musk", "Joe Biden"}

# Output dir
OUT_DIR = 'Analysis_plots_final'
os.makedirs(OUT_DIR, exist_ok=True)


# LOAD & FILTER

def load_and_filter(path):
    counts = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    for art in data:
        for person, c in art.get('mention_counts', {}).items():
            if ' ' in person and person not in dead_scientists and person not in non_scientists:
                counts.append(c)
    return np.array(counts, dtype=int)

mention_data = {
    source: load_and_filter(path)
    for source, path in JSON_PATHS.items()
}

# Optional: Trim Wired outliers
wired_full = mention_data['Wired']
cutoff = np.percentile(wired_full, 99)
mention_data_vis = mention_data.copy()
mention_data_vis['Wired'] = wired_full[wired_full <= cutoff]


# PLOTS

# 1) Log–Log Histogram
# plt.figure(figsize=(6, 5))
# max_count = max(arr.max() for arr in mention_data_vis.values())
# bins = np.logspace(0, np.log10(max_count), 30)

# for src, arr in mention_data_vis.items():
#     plt.hist(arr, bins=bins, alpha=0.6, label=src, color=palette[src])

# plt.xscale('log'); plt.yscale('log')
# plt.xlabel('Mention Count')
# plt.ylabel('Number of Scientists')
# plt.title('Log–Log Histogram of Living Scientist Mentions')
# plt.legend()
# plt.tight_layout()
# plt.savefig(os.path.join(OUT_DIR, 'histogram.png'), dpi=300)
# plt.close()

# # 2) CDF (optional – not preferred by Hector)
# plt.figure(figsize=(6,5))
# for src, arr in mention_data_vis.items():
#     arr_sorted = np.sort(arr)
#     cdf = np.arange(1, len(arr_sorted)+1) / len(arr_sorted)
#     plt.step(arr_sorted, cdf, where='post', label=src, color=palette[src])

# plt.xscale('log')
# plt.xlabel('Mention Count')
# plt.ylabel('CDF')
# plt.title('CDF of Living Scientist Mentions')
# plt.legend()
# plt.tight_layout()
# plt.savefig(os.path.join(OUT_DIR, 'cdf.png'), dpi=300)
# plt.close()
# Clear side-by-side log–log histogram
plt.figure(figsize=(6, 5))

max_count = max(arr.max() for arr in mention_data_vis.values())
bins = np.logspace(0, np.log10(max_count), 30)

# Compute histogram data first (no plotting yet)
hist_data = {}
for src, arr in mention_data_vis.items():
    hist, bin_edges = np.histogram(arr, bins=bins)
    hist_data[src] = (hist, bin_edges)

# Plot side-by-side bars
width = (bin_edges[1] - bin_edges[0]) / 1.8  # narrow bars
offsets = {
    'Wired': -width,
    'New Scientist': 0,
    'Quanta': width
}

for src, (hist, bin_edges) in hist_data.items():
    plt.bar(bin_edges[:-1] + offsets[src], hist,
            width=width,
            label=src,
            color=palette[src],
            alpha=0.9,
            edgecolor='black')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Mention Count')
plt.ylabel('Number of Scientists')
plt.title('Log–Log Histogram of Living Scientist Mentions')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'histogram_clear.png'), dpi=300)
plt.close()


# Improved CDF Plot (Reverse CDF, trimmed top 0.5% outliers)
plt.figure(figsize=(6,5))

for src, arr in mention_data.items():
    # Trim top 0.5% of extreme outliers
    cutoff = np.percentile(arr, 99.5)
    arr_trimmed = arr[arr <= cutoff]
    arr_sorted = np.sort(arr_trimmed)
    cdf = np.arange(1, len(arr_sorted)+1) / len(arr_sorted)
    reverse_cdf = 1 - cdf
    plt.step(arr_sorted, reverse_cdf, where='post', label=src, color=palette[src])

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Mention Count')
plt.ylabel('1 - CDF (Reverse CDF)')
plt.title('Reverse CDF of Living Scientist Mentions (Top 0.5% Trimmed)')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'reverse_cdf_trimmed.png'), dpi=300)
plt.close()




#  4) Unique Living Scientists (Bar Plot)
unique_counts = {
    src: len(set(
        person for art in json.load(open(JSON_PATHS[src], encoding='utf-8'))
        for person in art.get('mention_counts', {})
        if ' ' in person and person not in dead_scientists and person not in non_scientists
    ))
    for src in JSON_PATHS
}

plt.figure(figsize=(6, 5))
plt.bar(unique_counts.keys(), unique_counts.values(), color=[palette[src] for src in unique_counts])
plt.ylabel("Number of Unique Living Scientists")
plt.title("Unique Living Scientists Mentioned per Outlet")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'unique_mentions_barplot.png'), dpi=300)
plt.close()


#  5) Total Mentions (Bar Plot)
total_mentions = {
    src: int(np.sum(arr))
    for src, arr in mention_data.items()
}

plt.figure(figsize=(6, 5))
plt.bar(total_mentions.keys(), total_mentions.values(), color=[palette[src] for src in total_mentions])
plt.ylabel("Total Mentions")
plt.title("Total Mentions of Living Scientists")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'total_mentions_barplot.png'), dpi=300)
plt.close()


#  6) Boxplot: Distribution of Mentions per Scientist
plt.figure(figsize=(6,5))
data_to_plot = [mention_data[src] for src in JSON_PATHS]
plt.boxplot(data_to_plot, labels=JSON_PATHS.keys(), patch_artist=True,
            boxprops=dict(facecolor='lightgray', color='black'),
            medianprops=dict(color='black'))

# Overlay legend colors
for i, src in enumerate(JSON_PATHS, start=1):
    plt.plot([], [], label=src, color=palette[src])

plt.ylabel("Mentions per Living Scientist")
plt.yscale("log")
plt.title("Distribution of Mentions per Scientist")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'boxplot_mentions.png'), dpi=300)
plt.close()


# —— Done —— #
print(" All plots saved to:", OUT_DIR)
