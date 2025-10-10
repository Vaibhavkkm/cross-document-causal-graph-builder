# Quick Start Guide

## 🚀 Running the Demo

Your Connected Papers demo is **already running**!

### Open in Browser:

```
http://127.0.0.1:5001
```

---

## ✨ Features You'll See

### 1️⃣ **Interactive Graph Visualization**

- 12 academic papers displayed as colored bubbles
- Connections showing relationships between papers
- Colors indicate citation count:
  - 🔴 Red = High citations (1000+)
  - 🟠 Orange = Medium citations (100-1000)
  - 🔵 Blue = Low citations (<100)

### 2️⃣ **Click to Explore**

- Click any bubble to fetch paper details
- View full information in the right sidebar:
  - Title
  - Authors
  - Year
  - Citations count
  - Journal name
  - Abstract
  - Link to paper

### 3️⃣ **Interactive Controls**

- 🖱️ **Drag** bubbles to rearrange
- 🔍 **Scroll** to zoom in/out
- 👆 **Pan** by dragging the background
- 💡 **Hover** over bubbles to see titles

---

## 🎯 Try These Actions

1. **Click the large red bubble** (VOSviewer paper - 8,921 citations)
2. **Drag some bubbles around** to see the force simulation
3. **Zoom in** to see year labels more clearly
4. **Click different papers** to compare their details

---

## 🛠️ For Next Time

To start the server again, you have 3 options:

### Option 1: Quick Script

```bash
cd connected_papers_demo
./run.sh
```

### Option 2: Direct Python

```bash
cd connected_papers_demo
python3 server.py
```

### Option 3: With Virtual Environment

```bash
cd connected_papers_demo
python3 -m venv venv
source venv/bin/activate
pip install Flask
python3 server.py
```

---

## 📝 Customizing Your Graph

### Add Your Own Papers

Edit `server.py` and add to the `PAPERS` dictionary:

```python
"p13": {
    "id": "p13",
    "title": "Your Paper Title Here",
    "authors": "John Doe, Jane Smith",
    "year": 2024,
    "citations": 500,
    "journal": "Your Journal Name",
    "abstract": "Your abstract text...",
    "url": "https://example.com/paper"
}
```

### Add Connections

In `GRAPH_DATA["links"]`:

```python
{"source": "p1", "target": "p13", "weight": 3}
```

Higher weight = thicker connection line

---

## 🎨 Customization Ideas

1. **Change colors**: Edit CSS in `index.html`
2. **Adjust bubble sizes**: Modify `getNodeSize()` function
3. **Add search**: Implement a search bar
4. **Filter by year**: Add year range slider
5. **Export image**: Add screenshot functionality
6. **More metadata**: Add DOI, keywords, etc.

---

## 📊 Current Dataset

The demo includes 12 papers about:

- Bibliometric analysis methods
- Science mapping tools
- Citation network visualization
- Co-citation analysis
- Research evaluation metrics

Papers span from **1963 to 2020** with citations ranging from **654 to 8,921**.

---

## 🆘 Troubleshooting

### Port Already in Use?

Change the port in `server.py`:

```python
app.run(debug=True, port=5002, host='0.0.0.0')
```

### Flask Not Installed?

```bash
python3 -m pip install Flask
```

### Page Not Loading?

- Check the server is running in terminal
- Try `http://localhost:5001` instead
- Check firewall settings

---

## 📚 Resources

- **D3.js Documentation**: https://d3js.org/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Connected Papers**: https://www.connectedpapers.com/

---

**Enjoy exploring your graph! 🎉**
