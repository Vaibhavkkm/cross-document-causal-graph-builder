# 🎯 Action Plan: How to Proceed with Your Dataset

## ✅ What You Have Now

### **1. Dataset** ✓

- **1,600+ historical text files** in `final_dataset/`
- **Three main types**:
  - Personal diaries (diary_irving, diary_grover, etc.)
  - Military letters (Harold, James, british, etc.)
  - Battle narratives (battle, history, etc.)
- **WWI era** (1914-1919) content
- **~45,000 lines** of uncleaned text

### **2. Visualization Demo** ✓

- **Interactive graph** working perfectly
- **Click-to-fetch** functionality implemented
- **Ready to display your real data**

### **3. Processing Scripts** ✓

- `step1_preprocess.py` - Clean and analyze texts
- `step2_extract_events.py` - Extract events using NLP
- `step3_build_graph.py` - Build causal graph
- `setup.sh` - Quick setup automation

---

## 🚀 Recommended Workflow

### **Week 1: Exploration & Small-Scale Testing**

#### Day 1-2: Understand Your Data

```bash
# Run the preprocessing
python3 step1_preprocess.py
```

**Expected output:**

- `processed_texts.json` with structured data
- Statistics about your dataset
- Categories breakdown

**Action**: Review the output, understand the text structures

#### Day 3-4: Test Event Extraction (Small Sample)

```bash
# Extract events from 10 documents
python3 step2_extract_events.py
# (It's set to process 20 by default, which is fine)
```

**Expected output:**

- `extracted_events.json` with events and causal relations
- Statistics about events found

**Action**:

1. Open `extracted_events.json`
2. Review if events make sense
3. Note what's missing or wrong

#### Day 5: Build First Graph

```bash
# Build the graph
python3 step3_build_graph.py

# Start visualization
cd connected_papers_demo
python3 server.py
# Open: http://127.0.0.1:5001
```

**Action**: See your real historical events in the graph!

---

### **Week 2: Refinement & Scaling**

#### Day 1-2: Manual Review & Annotation

**Pick 5-10 representative documents and:**

1. Manually identify key events
2. Mark causal relationships
3. Create a "gold standard" sample

**Example annotation format** (create `manual_annotations.json`):

```json
{
  "diary_irving_001.txt": {
    "events": [
      {
        "text": "Were given rifles",
        "type": "military_action",
        "entities": ["rifles"],
        "date": "21 December 1917"
      },
      {
        "text": "Went to parade grounds armed with an imitation bomb",
        "type": "training",
        "entities": ["parade grounds", "bomb"],
        "date": "21 December 1917"
      }
    ],
    "causal_relations": [
      {
        "source": 0,
        "target": 1,
        "type": "temporal_sequence",
        "confidence": "high"
      }
    ]
  }
}
```

#### Day 3-4: Improve Extraction Rules

Based on manual review, edit `step2_extract_events.py`:

**Add domain-specific patterns:**

```python
# WWI-specific action verbs
military_verbs = [
    'attacked', 'defended', 'retreated', 'advanced',
    'marched', 'bombed', 'shelled', 'captured',
    'wounded', 'killed', 'evacuated', 'reinforced'
]

# WWI locations
known_locations = [
    'Somme', 'Verdun', 'Ypres', 'Gallipoli',
    'France', 'Belgium', 'Egypt', 'Mesopotamia'
]

# Causal keywords for military context
military_causal = [
    'as a result of', 'because of the', 'led to the',
    'caused by', 'due to', 'following the', 'after the'
]
```

#### Day 5: Scale Up Processing

```bash
# Process more documents (100+)
# Edit step2_extract_events.py, change sample_size to 100
python3 step2_extract_events.py

# Rebuild graph
python3 step3_build_graph.py

# View results
cd connected_papers_demo && python3 server.py
```

---

### **Week 3: Advanced Features**

#### Option A: Use ML Models (if you have time)

Install Hugging Face transformers:

```bash
pip install transformers torch
```

Use pre-trained models for:

1. **Better Entity Recognition**: `dslim/bert-base-NER`
2. **Causality Detection**: Fine-tune BERT on causal text

#### Option B: Manual Curation (more reliable for bachelor project)

1. Extract events automatically
2. Export to spreadsheet
3. Manually verify/correct
4. Import back into graph

#### Option C: Focus on Visualization

Enhance the graph interface:

- Add timeline slider
- Filter by person/location
- Search functionality
- Export options

---

## 📊 Expected Results at Each Stage

### **After Step 1 (Preprocessing)**

```
✅ ~1,600 documents loaded
✅ Categorized by type
✅ Metadata extracted
✅ Statistics generated
```

### **After Step 2 (Event Extraction)**

```
✅ 1,000+ events identified (from 20 docs)
✅ 50-100 causal relations found
✅ Entities extracted (people, places, dates)
✅ JSON file ready for graphing
```

### **After Step 3 (Graph Building)**

```
✅ Graph with 1,000+ nodes
✅ Connections showing relationships
✅ Ready for visualization
✅ Click-able events with details
```

---

## 🎯 Two Approaches: Choose One

### **Approach 1: Breadth (Process Everything)**

**Goal**: Show the system works at scale

**Steps**:

1. Process all 1,600 documents
2. Extract events automatically
3. Accept ~60-70% accuracy
4. Focus on visualization quality
5. Manually fix key events only

**Pros**: Impressive scale, complete coverage  
**Cons**: Lower accuracy, more noise

**Best for**: Demonstrating automation, big-picture view

---

### **Approach 2: Depth (Perfect a Subset)**

**Goal**: Show high-quality causality extraction

**Steps**:

1. Pick 50-100 representative documents
2. Extract events carefully
3. Manually verify all causal links
4. Achieve 90%+ accuracy
5. Document methodology thoroughly

**Pros**: High quality, defensible results  
**Cons**: Smaller dataset, more manual work

**Best for**: Academic rigor, methodological focus

---

## 🔍 What to Focus On for Bachelor Project

### **Must Have** (Core Requirements):

1. ✅ Working visualization (you have this!)
2. ✅ Event extraction from texts
3. ✅ Some causal relationships identified
4. ✅ Interactive exploration

### **Should Have** (Good to have):

- Comparison of manual vs automatic extraction
- Precision/Recall metrics
- Different text types handled
- Clear documentation

### **Nice to Have** (If time permits):

- ML-based causality detection
- Advanced filtering
- Export functionality
- User study

---

## 💡 Pro Tips

### **1. Start with the easiest texts**

- Battle descriptions are structured → easier
- Personal diaries are narrative → harder
- Pick your battles (literally!)

### **2. Use the 80/20 rule**

- 80% of value from 20% of features
- Get something working quickly
- Refine iteratively

### **3. Document everything**

- Take screenshots at each stage
- Keep notes on what works/doesn't
- Track accuracy metrics

### **4. Prepare for presentation**

- Have 5-6 really good examples
- Show before/after
- Explain challenges honestly

---

## 🚧 Common Pitfalls & Solutions

### **Pitfall 1: Trying to be 100% accurate**

**Solution**: Accept 70% is fine for proof-of-concept

### **Pitfall 2: Processing everything at once**

**Solution**: Start with 10 docs, scale gradually

### **Pitfall 3: Over-engineering**

**Solution**: Simple rules often beat complex ML

### **Pitfall 4: Ignoring manual work**

**Solution**: Manual annotation is valuable data!

---

## 📅 Sample 3-Week Timeline

### **Week 1: Foundation**

- Day 1-2: Run preprocessing, understand data
- Day 3-4: Test event extraction on 20 docs
- Day 5: First visualization with real data

### **Week 2: Refinement**

- Day 1-2: Manual annotation of 10 docs
- Day 3-4: Improve extraction rules
- Day 5: Process 100 docs, evaluate

### **Week 3: Polish**

- Day 1-2: Choose approach (breadth vs depth)
- Day 3-4: Final processing & visualization
- Day 5: Documentation & screenshots

---

## ✅ Success Checklist

At the end, you should have:

- [ ] Processed dataset (processed_texts.json)
- [ ] Extracted events (extracted_events.json)
- [ ] Working visualization
- [ ] 5-10 manually verified examples
- [ ] Screenshots of the system
- [ ] Documentation of methodology
- [ ] Accuracy metrics (even if informal)
- [ ] List of challenges & solutions

---

## 🎓 For Your Report/Presentation

### **Include:**

1. **Dataset description** (1,600 WWI texts)
2. **Methodology** (NLP pipeline)
3. **Sample extractions** (before/after)
4. **Visualization screenshots**
5. **Accuracy analysis** (manual vs auto)
6. **Challenges faced** (be honest!)
7. **Future improvements**

### **Good talking points:**

- "Processing 1,600 historical documents"
- "Automated event extraction achieved X% accuracy"
- "Interactive graph enables exploration of causal chains"
- "Manual annotation provided ground truth"
- "Future work: ML models, larger datasets"

---

## 🚀 Ready to Start?

```bash
# Quick start
cd /Users/vaibhavmangroliya/Documents/PY_CODES/SEM_3_PROJECTS/cgb_historical_texts

# Run setup
./setup.sh

# OR manually:
python3 step1_preprocess.py
python3 step2_extract_events.py
python3 step3_build_graph.py

# Start visualization
cd connected_papers_demo
python3 server.py
```

**Open**: http://127.0.0.1:5001

---

**You've got this! 🎉**

Remember: The goal is to show you understand the problem and can build a working system. Perfect accuracy is not required for a bachelor project!
