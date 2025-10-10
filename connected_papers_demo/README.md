# Connected Papers Demo

An interactive visualization similar to Connected Papers that allows you to explore a network of academic papers. Click on any bubble to fetch and display detailed information about that paper.

## Features

- 🎨 **Interactive Force-Directed Graph**: Papers are represented as bubbles with size and color based on citation count
- 🔍 **Click to Explore**: Click any bubble to fetch and display detailed paper information
- 🎯 **Color-Coded by Citations**:
  - Red: High citations (1000+)
  - Orange: Medium citations (100-1000)
  - Blue: Low citations (<100)
- 🖱️ **Interactive Controls**: Drag nodes, zoom, and pan around the graph
- 📊 **Rich Paper Details**: View title, authors, year, citations, journal, and abstract

## Dataset

The demo includes 12 dummy papers about bibliometric analysis and science mapping:

- Papers from 1963 to 2020
- Citation counts ranging from 654 to 8,921
- Realistic metadata including authors, journals, and abstracts

## Setup & Installation

1. **Navigate to the project directory:**

   ```bash
   cd connected_papers_demo
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Demo

1. **Start the Flask server:**

   ```bash
   python server.py
   ```

2. **Open your browser:**
   Navigate to `http://127.0.0.1:5000`

3. **Explore the graph:**
   - Click on any bubble to see paper details in the sidebar
   - Drag bubbles to rearrange the layout
   - Scroll to zoom in/out
   - Pan by dragging the background

## Project Structure

```
connected_papers_demo/
│
├── index.html          # Frontend with D3.js visualization
├── server.py           # Flask backend serving data
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## API Endpoints

- `GET /` - Serves the main HTML page
- `GET /api/graph` - Returns the graph structure (nodes and links)
- `GET /api/paper/<paper_id>` - Returns detailed information for a specific paper
- `GET /api/papers` - Returns all papers (optional)

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript with D3.js v7
- **Backend**: Python Flask
- **Visualization**: D3.js force-directed graph layout

## Customization

### Adding Your Own Data

Edit `server.py` to add your own papers and connections:

1. **Add papers to the PAPERS dictionary:**

   ```python
   PAPERS = {
       "p1": {
           "id": "p1",
           "title": "Your Paper Title",
           "authors": "Author Names",
           "year": 2024,
           "citations": 100,
           "journal": "Journal Name",
           "abstract": "Your abstract here...",
           "url": "https://..."
       },
       # Add more papers...
   }
   ```

2. **Define connections in GRAPH_DATA:**
   ```python
   "links": [
       {"source": "p1", "target": "p2", "weight": 3},
       # Add more connections...
   ]
   ```

### Styling

Modify the `<style>` section in `index.html` to customize:

- Colors
- Font sizes
- Layout
- Sidebar width
- Node sizes

## Tips

- Larger bubbles = More citations
- Darker connections = Stronger relationships
- Year labels appear below each bubble
- Hover over bubbles to see full titles
- Selected nodes have a red outline

## Future Enhancements

- Search functionality
- Filter by year/citations
- Timeline slider
- Export graph as image
- Integration with real citation databases (Semantic Scholar, CrossRef, etc.)
- Clustering algorithms
- Path finding between papers

## License

MIT License - Feel free to use and modify for your projects!

## Credits

Inspired by [Connected Papers](https://www.connectedpapers.com/)

Built with:

- [D3.js](https://d3js.org/) - Data visualization library
- [Flask](https://flask.palletsprojects.com/) - Python web framework
