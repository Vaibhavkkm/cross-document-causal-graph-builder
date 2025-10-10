# 🎉 Your Connected Papers Demo is Ready!

## ✅ What I Built For You

A complete interactive graph visualization similar to Connected Papers where you can:

- **Click bubbles** to fetch and display paper details
- **Drag nodes** to rearrange the layout
- **Zoom and pan** to explore the graph
- **View rich metadata** including authors, citations, abstracts, and more

---

## 📁 Project Structure

```
connected_papers_demo/
├── index.html          # Frontend with D3.js visualization
├── server.py           # Flask backend (12 dummy papers + API)
├── requirements.txt    # Python dependencies
├── run.sh             # Quick start script
├── README.md          # Full documentation
├── QUICKSTART.md      # Quick start guide
└── PROJECT_SUMMARY.md # This file
```

---

## 🚀 The Server is Already Running!

**Open your browser now:** http://127.0.0.1:5001

You should see:

- An interactive force-directed graph with 12 bubbles
- Papers connected by relationship lines
- A sidebar ready to display details
- Color-coded bubbles (red=high citations, orange=medium, blue=low)

---

## 🎯 Quick Demo Actions

1. **Click the largest red bubble** → See details for "VOSviewer" (8,921 citations)
2. **Click any other bubble** → Details panel updates with paper info
3. **Drag bubbles around** → See the physics simulation in action
4. **Scroll to zoom** → Explore the graph at different scales
5. **Hover over bubbles** → See full paper titles in tooltips

---

## 📊 Dummy Dataset Details

### 12 Papers Included:

1. **Bibliometric Methods in Management** (2014, 4,570 citations)
2. **Science Mapping Software Tools** (2011, 2,234 citations)
3. **Software Tools for Bibliometric Analysis** (2020, 1,543 citations)
4. **Citation Analysis and Network Visualization** (1973, 892 citations)
5. **Visualizing Knowledge Domains** (2003, 3,456 citations)
6. **VOSviewer: Bibliometric Mapping** (2010, 8,921 citations) ⭐
7. **CiteSpace II** (2006, 5,234 citations)
8. **Citation Networks** (1979, 1,876 citations)
9. **Bibliographic Coupling** (1963, 2,109 citations)
10. **Co-word Analysis** (1983, 987 citations)
11. **Leiden Manifesto** (2015, 3,687 citations)
12. **Mapping Scientific Frontier** (1998, 654 citations)

### 24 Connections:

- Papers are linked based on citation relationships
- Line thickness indicates connection strength
- Forms a realistic citation network

---

## 🛠️ Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Visualization**: D3.js v7 (force-directed graph)
- **Backend**: Python Flask
- **Data**: JSON (easily replaceable)

---

## 🔧 How It Works

### When You Click a Bubble:

1. **Frontend (D3.js)** detects the click event
2. **AJAX Request** sent to Flask: `GET /api/paper/{paper_id}`
3. **Flask Server** looks up paper in PAPERS dictionary
4. **JSON Response** returned with full paper details
5. **JavaScript** renders the details in the sidebar
6. **Visual Feedback** - selected bubble gets red outline

### API Endpoints:

- `GET /` → Serves index.html
- `GET /api/graph` → Returns all nodes and links
- `GET /api/paper/<id>` → Returns specific paper details
- `GET /api/papers` → Returns all papers (optional)

---

## 🎨 Customization Guide

### Replace with Your Data:

#### Step 1: Edit `server.py` - Add Your Papers

```python
PAPERS = {
    "your_paper_id": {
        "id": "your_paper_id",
        "title": "Your Paper Title",
        "authors": "Author Names",
        "year": 2024,
        "citations": 100,
        "journal": "Journal Name",
        "abstract": "Your abstract...",
        "url": "https://..."
    }
}
```

#### Step 2: Define Graph Structure

```python
GRAPH_DATA = {
    "nodes": [
        {"id": "your_paper_id", "title": "Short Title", "citations": 100, "year": 2024}
    ],
    "links": [
        {"source": "paper1", "target": "paper2", "weight": 3}
    ]
}
```

#### Step 3: Restart the Server

```bash
Ctrl+C  # Stop current server
python3 server.py  # Restart
```

### Styling Changes:

Edit the `<style>` section in `index.html`:

- Node colors: `.node { fill: ... }`
- Sidebar width: `#sidebar { width: 400px; }`
- Fonts: `body { font-family: ... }`
- Colors: Change hex codes

---

## 📈 Future Enhancement Ideas

### Easy Additions:

- ✅ Search bar to find papers
- ✅ Filter by year/citations
- ✅ Export graph as PNG/SVG
- ✅ Show related papers section
- ✅ Add paper thumbnails

### Advanced Features:

- 🔄 Connect to real APIs (Semantic Scholar, CrossRef)
- 🔄 Automatic paper recommendations
- 🔄 Timeline visualization
- 🔄 Clustering algorithms
- 🔄 Path finding between papers
- 🔄 Import from BibTeX files

---

## 🐛 Troubleshooting

### Server Won't Start?

```bash
# Check if port is in use
lsof -i :5001

# Use different port
# Edit server.py: app.run(port=5002)
```

### Flask Not Found?

```bash
python3 -m pip install Flask
```

### Graph Not Loading?

1. Check browser console (F12) for errors
2. Verify server is running
3. Check API responses in Network tab

### Bubbles Too Small/Large?

Edit `getNodeSize()` function in `index.html`:

```javascript
function getNodeSize(citations) {
  return Math.sqrt(citations) * 0.8 + 15; // Adjust multiplier
}
```

---

## 📚 Learning Resources

### D3.js:

- Official Docs: https://d3js.org/
- Gallery: https://observablehq.com/@d3/gallery
- Force Layout: https://d3js.org/d3-force

### Flask:

- Quickstart: https://flask.palletsprojects.com/quickstart/
- API Tutorial: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

### Graph Visualization:

- Connected Papers: https://www.connectedpapers.com/
- Citation Networks: https://en.wikipedia.org/wiki/Citation_graph

---

## 🎓 Use Cases

This demo is perfect for:

- 📖 Literature review visualization
- 🔬 Research paper exploration
- 👥 Collaboration network mapping
- 📊 Citation analysis projects
- 🎓 Academic presentations
- 💼 Knowledge base visualization

---

## 📝 Next Steps

### To Stop the Server:

Press `Ctrl+C` in the terminal

### To Restart Later:

```bash
cd connected_papers_demo
./run.sh
# or
python3 server.py
```

### To Deploy Online:

Consider using:

- **Heroku** (free tier available)
- **PythonAnywhere**
- **Vercel** (with serverless functions)
- **GitHub Pages** + external API

---

## 💡 Pro Tips

1. **Keep citations realistic** - sqrt scaling makes differences visible
2. **Limit connections** - Too many lines = cluttered graph
3. **Use meaningful weights** - Affects line thickness
4. **Test with different screen sizes** - Graph is responsive
5. **Add keyboard shortcuts** - Enhance user experience

---

## ⚖️ License

This project is provided as-is for educational purposes.
Feel free to modify and use for your projects!

---

## 🙏 Credits

**Built with:**

- D3.js - Data visualization library
- Flask - Python web framework
- Inspired by Connected Papers

**Created for:** Academic research visualization
**Date:** October 2025

---

**🎉 Enjoy exploring your graph! If you have questions or want to add features, feel free to ask!**
