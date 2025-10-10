# Causal Graph Builder for Historical Texts 📚➡️📊

**Extract events from historical texts and visualize causal relationships in an interactive graph**

---

## 🎯 Project Overview

This project implements a **Causal Graph Builder** that:

1. Processes historical text documents (letters, diaries, battle reports)
2. Extracts key events and entities using NLP
3. Identifies causal relationships between events
4. Visualizes them in an interactive force-directed graph (like Connected Papers)

### Your Dataset

- **~1,600 text files** from WWI era
- **Categories**: Personal diaries, letters, battle descriptions
- **~45,000 lines** of historical content
- **Sources**: Irving, Harold, James, British soldiers, battle narratives

---

## 📁 Project Structure

```
cgb_historical_texts/
│
├── final_dataset/              # Your 1,600+ text files
│   ├── diary_irving_*.txt
│   ├── diary_grover_*.txt
│   ├── Harold*.txt
│   ├── battle_*.txt
│   └── ... (1,600+ files)
│
├── connected_papers_demo/      # Interactive visualization
│   ├── index.html             # D3.js graph interface
│   ├── server.py              # Flask API server
│   ├── graph_data.json        # Graph structure (nodes + links)
│   └── nodes_detail.json      # Event details for click
│
├── step1_preprocess.py        # Clean and analyze texts
├── step2_extract_events.py    # Extract events using NLP
├── step3_build_graph.py       # Build causal graph
│
├── processed_texts.json       # Output: cleaned texts
├── extracted_events.json      # Output: extracted events
│
├── requirements_full.txt      # Python dependencies
└── README.md                  # This file
```

---

## 🚀 Quick Start

### **Step 1: Install Dependencies**

```bash
# Navigate to project
cd /Users/vaibhavmangroliya/Documents/PY_CODES/SEM_3_PROJECTS/cgb_historical_texts

# Install basic requirements
pip install Flask

# For NLP features (optional but recommended)
pip install spacy
python -m spacy download en_core_web_sm

# Install all dependencies
pip install -r requirements_full.txt
```

### **Step 2: Process Your Dataset**

```bash
# Run preprocessing
python step1_preprocess.py
```

**Output**: `processed_texts.json` with structured data

**What it does:**

- Loads all 1,600+ text files
- Extracts metadata (author, date, location)
- Categorizes documents
- Provides statistics

### **Step 3: Extract Events**

```bash
# Run event extraction
python step2_extract_events.py
```

**Output**: `extracted_events.json` with events and causal relations

**What it does:**

- Identifies key events (actions, battles, movements)
- Extracts entities (people, places, dates)
- Finds causal patterns (because, led to, caused)
- Creates temporal sequences

### **Step 4: Build the Graph**

```bash
# Run graph builder
python step3_build_graph.py
```

**Output**:

- `connected_papers_demo/graph_data.json`
- `connected_papers_demo/nodes_detail.json`

**What it does:**

- Converts events → nodes
- Converts causal relations → links
- Prepares data for visualization

### **Step 5: Run the Visualization**

```bash
# Start the web server
cd connected_papers_demo
python server.py
```

**Open browser**: http://127.0.0.1:5001

**What you'll see:**

- Interactive graph with historical events as bubbles
- Click any bubble → See event details
- Arrows show causal relationships
- Drag, zoom, and explore!

---

## 📊 Data Flow

```
Raw Texts (1,600 files)
        ↓
  [step1_preprocess.py]
        ↓
  processed_texts.json
        ↓
  [step2_extract_events.py]
        ↓
  extracted_events.json
        ↓
  [step3_build_graph.py]
        ↓
  graph_data.json + nodes_detail.json
        ↓
  [Flask Server + D3.js]
        ↓
  Interactive Visualization 🎉
```

---

## 🎨 Visualization Features

### **Current Features:**

✅ Force-directed graph layout  
✅ Click bubbles → Fetch event details  
✅ Color-coded by importance  
✅ Draggable nodes  
✅ Zoom and pan  
✅ Responsive sidebar with metadata

### **Customizations You Can Make:**

**1. Update Server to Use Real Data:**

Edit `connected_papers_demo/server.py`:

```python
import json

# Load real graph data
with open('graph_data.json', 'r') as f:
    GRAPH_DATA = json.load(f)

# Load real node details
with open('nodes_detail.json', 'r') as f:
    PAPERS = json.load(f)
```

**2. Add More Event Types:**

Edit `step2_extract_events.py` to recognize:

- Military actions
- Diplomatic events
- Personal experiences
- Weather conditions

**3. Improve Causal Detection:**

Add domain-specific causal keywords:

```python
military_causal = ['retreat caused', 'attack led to', 'defense resulted in']
temporal_markers = ['after', 'before', 'following', 'preceded by']
```

---

## 🔧 Advanced Features (Future)

### **Phase 2: Semi-Automated Extraction**

- [ ] Train classifier on manually annotated events
- [ ] Use Hugging Face models for causality detection
- [ ] Add entity linking (recognize same person across documents)

### **Phase 3: Intelligent Reasoning**

- [ ] Implement reasoning layer (if A caused B, and B caused C...)
- [ ] Add confidence scores for causal links
- [ ] Cluster related events

### **Phase 4: Enhanced Visualization**

- [ ] Timeline view
- [ ] Filter by person/location/date
- [ ] Search functionality
- [ ] Export to different formats
- [ ] Shortest path between events

---

## 📖 Example Workflow

### **Sample: Analyzing Battle of Amiens**

**1. Input Text** (`battle_001.txt`):

```
Battle of Amiens (8-11 August 1918) heralded the start of the Hundred Days campaign.
The BEF made gains of seven miles. German General Ludendorff described it as the
'black day' of the German Army.
```

**2. Extracted Events**:

- Event 1: "Battle of Amiens started" (Aug 8, 1918)
- Event 2: "BEF made gains of seven miles"
- Event 3: "Ludendorff called it 'black day'"

**3. Causal Relations**:

- Event 1 → Event 2 (temporal: battle led to gains)
- Event 2 → Event 3 (causal: gains caused description)

**4. Visualization**:

- 3 bubbles connected by arrows
- Click "Battle of Amiens" → See full description
- Follow arrows to see consequences

---

## 🧪 Testing with Sample Data

### **Quick Test (5 documents)**

```bash
# Process just 5 files for testing
python -c "
from step2_extract_events import process_sample_documents
process_sample_documents('processed_texts.json', 'test_events.json', sample_size=5)
"
```

### **Verify Results**

```bash
# Check what was extracted
python -c "
import json
with open('extracted_events.json', 'r') as f:
    data = json.load(f)
    print(f'Documents: {len(data)}')
    print(f'Total events: {sum(d[\"num_events\"] for d in data)}')
"
```

---

## 🐛 Troubleshooting

### **Problem: spaCy model not found**

```bash
python -m spacy download en_core_web_sm
```

### **Problem: Memory error with large files**

Edit scripts to process in batches:

```python
# In step2_extract_events.py
process_sample_documents(input_file, output_file, sample_size=50)  # Reduce size
```

### **Problem: No causal relations found**

The texts might need manual annotation first. Start with:

1. Pick 10-20 documents
2. Manually identify events
3. Mark causal relationships
4. Use as training data

### **Problem: Visualization not showing data**

Check:

```bash
# Verify files exist
ls connected_papers_demo/graph_data.json
ls connected_papers_demo/nodes_detail.json

# Check if server loaded them
# Look for console output when server starts
```

---

## 📚 Dataset Statistics

After running `step1_preprocess.py`, you should see:

```
📊 DATASET ANALYSIS
==============================================================
📁 Total Documents: 1,600+

📚 Categories:
   • diary: ~500 files (Personal diaries)
   • letter_british: ~300 files (Military letters)
   • battle: ~50 files (Battle descriptions)
   • letter_personal: ~200 files (Personal letters)
   • history: ~50 files (Historical narratives)
   • other: ~500 files

✍️  Unique Authors: 50+
📍 Unique Locations: 200+ (France, Belgium, Egypt, etc.)
📅 Date Range: 1914-1919
==============================================================
```

---

## 💡 Tips for Success

### **1. Start Small**

- Process 10-20 documents first
- Manually verify event extraction
- Refine your extraction rules
- Then scale up

### **2. Manual Annotation**

- Pick 5 representative documents
- Manually mark events and causal links
- Use this as "ground truth"
- Compare with automated extraction

### **3. Iterative Refinement**

```
Extract → Review → Refine → Repeat
```

### **4. Domain Knowledge**

Add WWI-specific patterns:

- Military actions: "attack", "retreat", "advance"
- Casualties: "killed", "wounded", "captured"
- Locations: Recognize battle sites
- Military units: Regiment numbers, battalions

---

## 🎓 Academic Context

**Project Type**: Bachelor-level NLP + Visualization  
**Key Concepts**:

- Cause-and-Effect Extraction from Narratives
- Graph structures for causal chains
- Simple NLP and visualization
- Semi-automated annotation

**Relevant Techniques**:

- Named Entity Recognition (NER)
- Temporal ordering
- Dependency parsing
- Pattern matching

---

## 📞 Getting Help

### **If event extraction seems wrong:**

1. Check the text format (metadata vs content)
2. Adjust sentence splitting
3. Add domain-specific verb patterns

### **If causality detection is poor:**

1. Start with manual annotation
2. Look for explicit markers first
3. Temporal relationships are easier than causal

### **If visualization is empty:**

1. Check file paths in scripts
2. Verify JSON files are created
3. Look at browser console for errors

---

## 🎉 Success Criteria

You'll know it's working when:

- ✅ All texts are loaded and categorized
- ✅ Events are extracted (even if imperfect)
- ✅ Some causal relations are identified
- ✅ Graph visualization displays bubbles
- ✅ Clicking bubbles shows event details
- ✅ You can explore connections

**Don't expect perfection!** This is a research project - iterative improvement is the goal.

---

## 🚀 Next Steps After Basic Demo

1. **Improve Extraction**:

   - Add more causal patterns
   - Use ML models (BERT for causality)
   - Manual correction interface

2. **Enhanced Visualization**:

   - Add filters (by date, person, location)
   - Timeline slider
   - Export functionality

3. **Evaluation**:

   - Precision/Recall of event extraction
   - Accuracy of causal relationships
   - User study on visualization

4. **Paper Writing**:
   - Document your methodology
   - Show examples
   - Discuss challenges and solutions

---

## 📄 License

MIT License - Feel free to use for your bachelor project!

---

**Good luck with your project! 🎓✨**

Remember: Perfect is the enemy of good. Get something working first, then refine!
