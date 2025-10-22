# bias-in-science-communication

# A Quantitative Framework for Detecting Bias and Distortion in Scientific Journalism

**Authors:**  
- Hector Zenil
- Raghavendra Koushik

---

## Overview
This repository contains the data, code, and visualizations supporting the paper:


We quantitatively analyzed 5,000+ science communication articles published between 2014–2024 in **Wired**, **New Scientist**, and **Quanta Magazine** to estimate **bias**, **favouritism**, and **distortion** in modern science journalism.

The methodology combines **Named Entity Recognition (NER)**, **mention frequency distributions**, **Gini inequality metrics**, and **linguistic sentiment/topic profiling** to quantify bias towards specific scientists or topics.

---

## Repository Structure

data/ → Raw and processed article datasets
code/ → Python analysis scripts (scraping, cleaning, NER, plotting)
figures/ → Plots and visualizations used in the paper
outputs/ → Summary tables and logs
docs/ → Reproducibility notes and paper overview



## Methods Summary

1. **Article Extraction** – Automated scraping of science sections from major media outlets (2014–2024).  
2. **NER-based Mention Detection** – Extracted and counted person names from article text.  
3. **Filtering & Anonymization** – Removed non-scientists and anonymized journalists.  
4. **Bias Metrics** – Computed Gini coefficients and rank–frequency distributions.  
5. **Linguistic Analysis** – Analyzed topics and sentiment polarity of article titles.


## Key Outputs

- `gini_summary.csv` – Inequality of mentions across outlets  
- `top_mentions.csv` – Top 10 living scientists per outlet  
- `reverse_cdf.png` – Reverse cumulative distribution of mentions  
- `rankfreq.png` – Zipf rank-frequency distribution  
- `sentiment_titles.png` – Sentiment analysis of article titles


## ⚙️ Reproducibility

To replicate the analysis:

```bash
git clone https://github.com/zenil-colab/bias-in-science-communication
cd bias-in-science-communication
pip install -r requirements.txt
python code/03_analysis/compute_gini.py


Python version: >=3.10
Main dependencies: pandas, numpy, matplotlib, scikit-learn, nltk, spacy, tqdm
