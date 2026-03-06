# Lab 4 Assignment Submission - Data Labs / Apache Beam labs

## Rhyming Pairs in Hamlet - Apache Beam

This project uses **Apache Beam's DirectRunner** to analyze Shakespeare's *Hamlet* and find rhyming pairs by grouping the last word of each line by their last 3 letters.

---

## Setup

### Prerequisites
- Python 3.10
- Homebrew (macOS)
- Google Cloud SDK (`gsutil`)

### Create Virtual Environment
```bash
# Install Python 3.10 if not already installed
brew install python@3.10

# Create and activate venv
/opt/homebrew/bin/python3.10 -m venv venv
source venv/bin/activate

# Verify Python version
python --version  # should show 3.10.x
```

### Install Dependencies
```bash
pip install --upgrade pip
pip install apache-beam pandas jupyter
```

---

## How to Run

```bash
# Activate the Python 3.10 venv first
source venv/bin/activate

jupyter notebook Try_Apache_Beam_Python.ipynb
```

Then run each cell top to bottom using `Shift+Enter`.

---

## What Are We Doing?

We build an Apache Beam pipeline that:

1. **Reads** every line from `hamlet.txt` pulled from Google Cloud Storage
2. **Extracts** the last word of each line using regex
3. **Lowercases** every word for clean comparison
4. **Filters** out words shorter than 4 letters
5. **Groups** words by their last 3 letters as the rhyme key
6. **Filters** out groups with only one unique word
7. **Writes** results to an output file

### Pipeline Structure
```
Read lines
  → Extract last word of each line
  → Lowercase
  → Filter words < 4 letters
  → Extract last 3 letters as rhyme key
  → Group by rhyme key
  → Filter groups with 1 unique word
  → Write results
```

---

## Data

Downloaded directly from Google Cloud Storage:
```bash
gsutil cp gs://dataflow-samples/shakespeare/hamlet.txt data/
```

No authentication required — this is a public GCS bucket provided by Google for Dataflow samples.

---

## Output

Results are written to `outputs/part-00000-of-*` and displayed in the notebook.

Each line shows a rhyme ending and all words in the play that share that ending:

```
('ight', ['delight', 'flight', 'light', 'might', 'night', 'right', 'sight'])
('ove',  ['above', 'dove', 'love', 'move', 'prove'])
('ell',  ['cell', 'farewell', 'fell', 'hell', 'tell', 'well'])
('een',  ['been', 'between', 'keen', 'queen', 'seen', 'sheen'])
('ear',  ['appear', 'dear', 'fear', 'hear', 'near', 'year'])
```

---

## Key Notes

- **Python 3.13 does not work** — Apache Beam and NumPy have C++ compilation issues on 3.13. Always use Python 3.10.
- **DirectRunner** runs the pipeline locally — no cloud infrastructure needed.
- Rhyme groups with only 1 unique word are filtered out to keep results meaningful.
- Words under 4 letters are excluded to avoid noise from common short words.
