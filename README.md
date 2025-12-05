# WWI Historical Documents - Cross-File Cause-Effect Extraction

This project extracts causal relationships from World War I historical documents (letters, diaries, battle reports) using NLP techniques. The focus is on finding cause-effect pairs that span across different source files.

## Project Structure

```
├── data/
│   └── processed_data.json      # preprocessed text data from historical documents
├── src/
│   ├── advanced_cause_effect_ml.py   # main extraction script
│   └── generate_cause_effect_network.py  # visualization script
├── output/
│   ├── cause_effect_results_final.json  # extracted relationships
│   ├── cause_effect_mapping.txt         # human-readable event labels
│   └── events.png                       # network visualization
├── requirements.txt
└── README.md
```

## How It Works

The extraction process has several stages:

### 1. Text Preprocessing
The raw historical documents (soldier letters, war diaries, battle reports) are split into sentences and stored in `processed_data.json`. Each entry has:
- `file_id`: source document name
- `sentences`: list of sentences from that document
- `date`: document date (if available)

### 2. Cause-Effect Detection

The main script (`advanced_cause_effect_ml.py`) looks for causal relationships between sentences from *different* files. It uses:

**Causal Language Detection**
- Looks for explicit phrases like "resulted in", "led to", "because of", "due to"
- Both forward ("X caused Y") and reverse ("Y because of X") patterns

**Entity Extraction**
- Extracts meaningful entities: battle names (Somme, Gallipoli), locations (France, Egypt), dates, military units
- Filters out generic words (battle, war, soldier) that would create false positives

**Semantic Similarity (TF-IDF)**
- Computes similarity between cause and effect text
- Rejects pairs that are too similar (likely duplicates) or too different (unrelated)
- Sweet spot is 0.15-0.65 similarity

**Validation Criteria**
For a pair to be accepted:
- Must be from different source files
- Must have explicit causal language in at least one text
- Must share at least 2 meaningful entities
- Semantic similarity in valid range
- Minimum confidence score of 0.85

### 3. Network Visualization

The visualization script creates a network graph showing:
- **Light blue nodes (C1, C2, ...)**: Cause events
- **Light green nodes (E1, E2, ...)**: Effect events  
- **Red dashed edges**: Causal relationships

## Usage

### Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Run Extraction
```bash
cd src
python advanced_cause_effect_ml.py
```

You can adjust the confidence threshold:
```bash
python advanced_cause_effect_ml.py 0.90  # stricter
python advanced_cause_effect_ml.py 0.75  # more permissive
```

### Generate Visualization
```bash
cd src
python generate_cause_effect_network.py
```

Output goes to `output/events.png`

## Output Format

### cause_effect_results_final.json
```json
[
  {
    "type": "cross_file",
    "cause_file": "survivor_008.txt",
    "cause_text": "When German infantry advanced...",
    "effect_file": "survivor_042.txt", 
    "effect_text": "Intense fighting led to heavy British losses...",
    "confidence": 1.0
  }
]
```

### cause_effect_mapping.txt
Human-readable list mapping event IDs to their source text:
```
C1 [survivor_008.txt]: When German infantry advanced...
E1 [survivor_042.txt]: Intense fighting led to heavy...
```

## Example Results

Some high-quality relationships found:

| Cause | Effect | Shared Context |
|-------|--------|----------------|
| Germany's sinking of the Lusitania (1915) | Germany abandoning submarine warfare | Germany, 1915 |
| Germany declared war on Russia | France entered the war | Germany, France, Russia |
| British attacks in the north | Germans forced to withdraw | Germans, British, Allied |

## Requirements

- Python 3.7+
- networkx
- matplotlib

See `requirements.txt` for full list.

## Notes

- The extraction prioritizes quality over quantity. Better to have 100 accurate pairs than 5000 questionable ones
- Cross-file requirement ensures we find connections between different sources, not just within a single document
- The confidence threshold of 0.85 is tuned for high precision
