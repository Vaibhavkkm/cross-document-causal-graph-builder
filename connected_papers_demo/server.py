from flask import Flask, jsonify, send_file
import json
from pathlib import Path

app = Flask(__name__)

# Load real historical event data
def load_real_data():
    """Load graph data and node details from JSON files"""
    base_dir = Path(__file__).parent
    
    # Load graph structure
    try:
        with open(base_dir / 'graph_data.json', 'r') as f:
            graph_data = json.load(f)
        print(f"✅ Loaded {len(graph_data['nodes'])} nodes and {len(graph_data['links'])} links")
    except FileNotFoundError:
        print("⚠️  graph_data.json not found - using dummy data")
        graph_data = None
    
    # Load node details
    try:
        with open(base_dir / 'nodes_detail.json', 'r') as f:
            nodes_detail = json.load(f)
        print(f"✅ Loaded details for {len(nodes_detail)} events")
    except FileNotFoundError:
        print("⚠️  nodes_detail.json not found - using dummy data")
        nodes_detail = None
    
    return graph_data, nodes_detail

# Load data at startup
GRAPH_DATA, PAPERS = load_real_data()

# Fallback to dummy data if real data not available
if PAPERS is None:
    # Dummy dataset - Papers on bibliometric analysis and science mapping
    PAPERS = {
        "p1": {
            "id": "p1",
            "title": "Bibliometric Methods in Management and Organization",
            "authors": "I. Zupic, T. Čater",
            "year": 2014,
            "citations": 4570,
            "journal": "Organizational Research Methods",
            "abstract": "This paper reviews bibliometric methods and their application in management and organizational research. It provides a comprehensive overview of citation analysis, co-citation analysis, bibliographic coupling, co-word analysis, and co-authorship analysis. The paper discusses how bibliometric methods can complement traditional literature reviews and meta-analysis.",
            "url": "https://journals.sagepub.com/doi/10.1177/1094428114562629"
        },
        "p2": {
            "id": "p2",
            "title": "Science Mapping Software Tools: Review, Analysis, and Cooperative Study",
            "authors": "N. J. Cobo, A. López-Herrera, E. Herrera-Viedma, F. Herrera",
            "year": 2011,
            "citations": 2234,
            "journal": "Journal of the American Society for Information Science and Technology",
            "abstract": "Science mapping analyzes the intellectual structure of scientific fields. This paper presents a comparative analysis of the main science mapping software tools currently available, including CiteSpace, VOSviewer, Sci2 Tool, and others. We analyze their features, capabilities, and use cases.",
            "url": "https://asistdl.onlinelibrary.wiley.com/doi/abs/10.1002/asi.21525"
        },
        "p3": {
            "id": "p3",
        "title": "Software Tools for Conducting Bibliometric Analysis in Science",
        "authors": "B. Moral-Muñoz, E. Herrera-Viedma, A. Santisteban-Espejo, M. Cobo",
        "year": 2020,
        "citations": 1543,
        "journal": "Journal of the Association for Information Science and Technology",
        "abstract": "This paper provides an updated review of software tools available for bibliometric analysis. It evaluates tools based on their functionality, ease of use, visualization capabilities, and analytical features. The paper includes hands-on examples using real scientific data.",
        "url": "https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24374"
    },
    "p4": {
        "id": "p4",
        "title": "Citation Analysis and Network Visualization",
        "authors": "M. Small",
        "year": 1973,
        "citations": 892,
        "journal": "Journal of the American Society for Information Science",
        "abstract": "One of the foundational papers in citation analysis, introducing the concept of co-citation and its use in mapping scientific literature. This paper laid the groundwork for modern bibliometric analysis and science mapping techniques.",
        "url": "https://onlinelibrary.wiley.com/doi/abs/10.1002/asi.4630240406"
    },
    "p5": {
        "id": "p5",
        "title": "Visualizing Knowledge Domains",
        "authors": "C. Chen",
        "year": 2003,
        "citations": 3456,
        "journal": "Annual Review of Information Science and Technology",
        "abstract": "This comprehensive review examines methods and tools for visualizing knowledge domains. It covers various visualization techniques including network analysis, spatial representations, and temporal dynamics. The paper discusses applications in library science, information science, and scientometrics.",
        "url": "https://asistdl.onlinelibrary.wiley.com/doi/10.1002/aris.1440370106"
    },
    "p6": {
        "id": "p6",
        "title": "VOSviewer: A Computer Program for Bibliometric Mapping",
        "authors": "N. J. van Eck, L. Waltman",
        "year": 2010,
        "citations": 8921,
        "journal": "Scientometrics",
        "abstract": "VOSviewer is a freely available computer program developed for constructing and visualizing bibliometric networks. This paper introduces the program and demonstrates its use for analyzing large bibliometric datasets. The software has become one of the most widely used tools in the field.",
        "url": "https://link.springer.com/article/10.1007/s11192-009-0146-3"
    },
    "p7": {
        "id": "p7",
        "title": "CiteSpace II: Detection and Visualization of Emerging Trends",
        "authors": "C. Chen",
        "year": 2006,
        "citations": 5234,
        "journal": "Journal of the American Society for Information Science and Technology",
        "abstract": "CiteSpace is designed to facilitate the detection and analysis of emerging trends in scientific literature. This paper describes the theoretical foundation and practical implementation of CiteSpace II, including its algorithms for identifying burst terms and pivotal points in scientific domains.",
        "url": "https://onlinelibrary.wiley.com/doi/abs/10.1002/asi.20317"
    },
    "p8": {
        "id": "p8",
        "title": "The Structure of Scientific Revolutions and Citation Networks",
        "authors": "E. Garfield",
        "year": 1979,
        "citations": 1876,
        "journal": "Current Contents",
        "abstract": "This paper explores how citation networks reveal the structure of scientific paradigms and revolutions. Building on Kuhn's work, it demonstrates how bibliometric methods can identify paradigm shifts and trace the evolution of scientific fields through citation patterns.",
        "url": "https://www.garfield.library.upenn.edu/essays/v4p467y1979-80.pdf"
    },
    "p9": {
        "id": "p9",
        "title": "Bibliographic Coupling and Network Analysis in Research Evaluation",
        "authors": "M. Kessler",
        "year": 1963,
        "citations": 2109,
        "journal": "American Documentation",
        "abstract": "This seminal paper introduces the concept of bibliographic coupling as a method for relating scientific papers. Two papers are bibliographically coupled if they both cite one or more papers in common. This concept has become fundamental to bibliometric analysis.",
        "url": "https://onlinelibrary.wiley.com/doi/abs/10.1002/asi.5090140103"
    },
    "p10": {
        "id": "p10",
        "title": "Co-word Analysis and Science Mapping of the Scientific Literature",
        "authors": "J. Callon, J. P. Courtial, W. A. Turner, S. Bauin",
        "year": 1983,
        "citations": 987,
        "journal": "Social Studies of Science",
        "abstract": "Co-word analysis examines the co-occurrence of keywords or terms in scientific literature to map the intellectual structure of research fields. This paper introduces the methodology and demonstrates its application in mapping emerging research areas.",
        "url": "https://journals.sagepub.com/doi/10.1177/030631283013003007"
    },
    "p11": {
        "id": "p11",
        "title": "The Leiden Manifesto for Research Metrics",
        "authors": "D. Hicks, P. Wouters, L. Waltman, S. de Rijcke, I. Rafols",
        "year": 2015,
        "citations": 3687,
        "journal": "Nature",
        "abstract": "This influential manifesto presents ten principles for the responsible use of bibliometric indicators in research evaluation. It addresses common pitfalls and provides guidance on how metrics should and should not be used in assessing research quality and impact.",
        "url": "https://www.nature.com/articles/520429a"
    },
    "p12": {
        "id": "p12",
        "title": "Mapping the Scientific Frontier: Identifying Emerging Research Topics",
        "authors": "H. D. White, K. W. McCain",
        "year": 1998,
        "citations": 654,
        "journal": "Journal of the American Society for Information Science",
        "abstract": "This paper presents methods for identifying research fronts and emerging topics in scientific fields using citation analysis. It demonstrates how bibliometric techniques can be used to predict future research directions and identify promising areas of investigation.",
        "url": "https://onlinelibrary.wiley.com/doi/abs/10.1002/(SICI)1097-4571(199809)49:11%3C1001::AID-ASI4%3E3.0.CO;2-I"
    }
}

# Graph structure - nodes and links (fallback if real data not loaded)
if GRAPH_DATA is None:
    GRAPH_DATA = {
        "nodes": [
            {"id": "p1", "title": "Bibliometric Methods in Management", "citations": 4570, "year": 2014},
            {"id": "p2", "title": "Science Mapping Software Tools", "citations": 2234, "year": 2011},
            {"id": "p3", "title": "Software Tools for Bibliometric Analysis", "citations": 1543, "year": 2020},
            {"id": "p4", "title": "Citation Analysis and Network Visualization", "citations": 892, "year": 1973},
            {"id": "p5", "title": "Visualizing Knowledge Domains", "citations": 3456, "year": 2003},
            {"id": "p6", "title": "VOSviewer: Bibliometric Mapping", "citations": 8921, "year": 2010},
            {"id": "p7", "title": "CiteSpace II", "citations": 5234, "year": 2006},
            {"id": "p8", "title": "Citation Networks", "citations": 1876, "year": 1979},
            {"id": "p9", "title": "Bibliographic Coupling", "citations": 2109, "year": 1963},
            {"id": "p10", "title": "Co-word Analysis", "citations": 987, "year": 1983},
            {"id": "p11", "title": "Leiden Manifesto", "citations": 3687, "year": 2015},
            {"id": "p12", "title": "Mapping Scientific Frontier", "citations": 654, "year": 1998}
        ],
        "links": [
            {"source": "p1", "target": "p2", "weight": 3},
            {"source": "p1", "target": "p3", "weight": 2},
            {"source": "p1", "target": "p11", "weight": 2},
            {"source": "p2", "target": "p6", "weight": 4},
            {"source": "p2", "target": "p7", "weight": 3},
            {"source": "p2", "target": "p5", "weight": 2},
            {"source": "p3", "target": "p6", "weight": 3},
            {"source": "p3", "target": "p2", "weight": 2},
            {"source": "p4", "target": "p8", "weight": 2},
            {"source": "p4", "target": "p9", "weight": 3},
            {"source": "p5", "target": "p7", "weight": 4},
            {"source": "p5", "target": "p6", "weight": 3},
            {"source": "p5", "target": "p4", "weight": 2},
            {"source": "p6", "target": "p7", "weight": 3},
            {"source": "p6", "target": "p11", "weight": 2},
            {"source": "p7", "target": "p5", "weight": 3},
            {"source": "p8", "target": "p9", "weight": 2},
            {"source": "p8", "target": "p4", "weight": 3},
            {"source": "p9", "target": "p4", "weight": 4},
            {"source": "p10", "target": "p5", "weight": 2},
            {"source": "p10", "target": "p1", "weight": 1},
            {"source": "p11", "target": "p1", "weight": 2},
            {"source": "p12", "target": "p5", "weight": 2},
            {"source": "p12", "target": "p8", "weight": 1}
        ]
    }

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_file('index_enhanced.html')

@app.route('/api/graph')
def get_graph():
    """Return the graph structure (nodes and links)"""
    return jsonify(GRAPH_DATA)

@app.route('/api/paper/<paper_id>')
def get_paper(paper_id):
    """Return detailed information for a specific paper"""
    if paper_id in PAPERS:
        return jsonify(PAPERS[paper_id])
    else:
        return jsonify({"error": "Paper not found"}), 404

@app.route('/api/papers')
def get_all_papers():
    """Return all papers (optional endpoint)"""
    return jsonify(list(PAPERS.values()))

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Connected Papers Demo Server")
    print("="*60)
    print(f"\n📊 Loaded {len(PAPERS)} papers")
    print(f"🔗 Loaded {len(GRAPH_DATA['links'])} connections")
    print(f"\n🌐 Open your browser to: http://127.0.0.1:5001")
    print("\n💡 Click on any bubble to see paper details!")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5001, host='0.0.0.0')
