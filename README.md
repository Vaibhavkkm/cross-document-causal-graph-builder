# Cross-Document Causal Graph Builder

Extracts causal relationships from WWI historical documents using both **rule-based NLP** and **ML-based (Hugging Face)** approaches.

## Project Structure

```
├── data/
│   └── processed_data.json         # Preprocessed text from historical documents
├── src/
│   ├── extract_rulebased.py        # Rule-based NLP extraction
│   ├── extract_ml.py               # ML-based extraction (Hugging Face)
│   └── generate_cause_effect_network.py  # Visualization generator
├── output/
│   ├── cause_effect_rulebased.json # Rule-based results
│   ├── cause_effect_ml.json        # ML-based results
│   ├── network_rulebased.png       # Rule-based network visualization
│   ├── network_ml.png              # ML-based network visualization
│   ├── mapping_rulebased.txt       # Rule-based event labels
│   └── mapping_ml.txt              # ML-based event labels
├── requirements.txt
└── README.md
```

## Two Approaches

### 1. Rule-Based NLP (`advanced_cause_effect_ml.py`)
Uses pattern matching and TF-IDF similarity:
- Explicit causal phrases ("led to", "resulted in", "because of")
- Entity extraction (battles, locations, dates)
- Semantic similarity scoring
- Shared context validation

**Output:** `cause_effect_rulebased.json` (149 pairs)

### 2. ML-Based Hybrid (`ml_cause_effect.py`)
Uses Hugging Face transformer + rule-based filtering:
- **Model:** `valhalla/distilbart-mnli-12-3` (Natural Language Inference)
- Rule-based candidate filtering
- ML entailment validation
- Combined scoring (rule + ML)

**Output:** `cause_effect_ml.json` (312 pairs)

## Usage

### Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Rule-Based Extraction
```bash
cd src
python3 extract_rulebased.py
```

### Run ML-Based Extraction
```bash
cd src
python3 extract_ml.py
```

### Generate Visualizations
```bash
cd src
python3 generate_cause_effect_network.py both      # Both visualizations
python3 generate_cause_effect_network.py rulebased # Rule-based only
python3 generate_cause_effect_network.py ml        # ML-based only
```

## Output Format

### Rule-Based JSON
```json
{
  "type": "cross_file",
  "cause_file": "survivor_008.txt",
  "cause_text": "When German infantry advanced...",
  "effect_file": "survivor_042.txt",
  "effect_text": "Intense fighting led to heavy British losses...",
  "confidence": 1.0
}
```

### ML-Based JSON
```json
{
  "cause_file": "survivor_044.txt",
  "cause_text": "Walter Greenwood remembered the anger...",
  "effect_file": "history_015.txt",
  "effect_text": "Britain fearing German domination...",
  "rule_score": 0.95,
  "ml_score": 0.98,
  "combined_score": 0.97,
  "shared_context": ["german", "britain", "germany"]
}
```

## Example Results

| Approach | Cause | Effect | Score |
|----------|-------|--------|-------|
| Rule-based | German infantry advanced → rifle fire | Intense fighting → heavy losses | 1.00 |
| ML-based | Germany attack → anger in Britain | Britain fearing German domination | 0.97 |
| ML-based | Germany mobilised against Russia | France entered war | 0.95 |

## Requirements

- Python 3.7+
- networkx
- matplotlib
- transformers (for ML approach)
- torch (for ML approach)

## Notes

- Rule-based approach is faster, ML approach has more pairs
- ML approach includes explainable scores (rule + ML)
- Both require cross-file pairs (different source documents)
- Minimum confidence threshold: 0.85
