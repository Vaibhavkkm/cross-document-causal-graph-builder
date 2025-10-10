"""
Causal Graph Builder - Visualization Integration
Phase 3: Convert extracted events into graph visualization format

This connects your event extraction to the Connected Papers demo
"""

import json
from pathlib import Path
from collections import defaultdict
import hashlib


class GraphBuilder:
    def __init__(self):
        self.nodes = []
        self.links = []
        self.node_id_map = {}
    
    def create_graph_from_events(self, events_file):
        """Convert extracted events into graph format"""
        
        with open(events_file, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        
        print(f"📊 Building graph from {len(documents)} documents...")
        
        for doc in documents:
            # Create nodes for each significant event
            for i, event in enumerate(doc['events']):
                node_id = self._generate_node_id(doc['filename'], i)
                
                # Extract event summary
                event_text = event['text'][:100]  # First 100 chars
                
                # Get entities
                entities = event.get('entities', {})
                persons = entities.get('PERSON', [])
                locations = entities.get('GPE', []) + entities.get('LOC', [])
                dates = entities.get('DATE', [])
                
                node = {
                    'id': node_id,
                    'title': event_text,
                    'full_text': event['text'],
                    'document': doc['filename'],
                    'author': doc.get('author', 'Unknown'),
                    'date': dates[0] if dates else doc.get('date', 'Unknown'),
                    'location': locations[0] if locations else doc.get('location', 'Unknown'),
                    'persons': persons,
                    'year': self._extract_year(dates[0] if dates else doc.get('date')),
                    'citations': 0,  # For visualization (size)
                }
                
                self.nodes.append(node)
                self.node_id_map[node_id] = len(self.nodes) - 1
            
            # Create links based on causal relations
            for relation in doc.get('causal_relations', []):
                if relation['type'] == 'temporal_sequence':
                    source_idx = relation['source']
                    target_idx = relation['target']
                    
                    if source_idx < len(doc['events']) and target_idx < len(doc['events']):
                        source_id = self._generate_node_id(doc['filename'], source_idx)
                        target_id = self._generate_node_id(doc['filename'], target_idx)
                        
                        link = {
                            'source': source_id,
                            'target': target_id,
                            'weight': 2,
                            'type': 'temporal'
                        }
                        self.links.append(link)
                
                elif relation['type'] == 'explicit_causal':
                    # Link this event to the next one (simple heuristic)
                    event_idx = relation['event_index']
                    if event_idx < len(doc['events']) - 1:
                        source_id = self._generate_node_id(doc['filename'], event_idx)
                        target_id = self._generate_node_id(doc['filename'], event_idx + 1)
                        
                        link = {
                            'source': source_id,
                            'target': target_id,
                            'weight': 3,
                            'type': 'causal',
                            'keyword': relation.get('causal_keyword', '')
                        }
                        self.links.append(link)
        
        print(f"✅ Created {len(self.nodes)} nodes and {len(self.links)} links")
        
        return {
            'nodes': self.nodes,
            'links': self.links
        }
    
    def _generate_node_id(self, filename, event_idx):
        """Generate unique node ID"""
        return f"{filename.replace('.txt', '')}_{event_idx}"
    
    def _extract_year(self, date_str):
        """Extract year from date string"""
        if not date_str or date_str == 'Unknown':
            return 1918  # Default WWI year
        
        # Try to find 4-digit year
        import re
        year_match = re.search(r'\b(19\d{2})\b', str(date_str))
        if year_match:
            return int(year_match.group(1))
        
        return 1918
    
    def save_for_visualization(self, output_file):
        """Save graph in format compatible with Connected Papers demo"""
        
        # Convert to the format expected by your demo
        graph_data = {
            'nodes': [
                {
                    'id': node['id'],
                    'title': node['title'],
                    'citations': len([l for l in self.links if l['target'] == node['id']]),  # Incoming links as "citations"
                    'year': node['year']
                }
                for node in self.nodes
            ],
            'links': self.links
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved visualization data to: {output_file}")
        
        # Also save detailed node information for the API
        nodes_detail = {
            node['id']: {
                'id': node['id'],
                'title': node['title'],
                'authors': node['author'],
                'year': node['year'],
                'citations': len([l for l in self.links if l['target'] == node['id']]),
                'journal': f"From: {node['document']}",
                'abstract': node['full_text'],
                'url': f"#event_{node['id']}"
            }
            for node in self.nodes
        }
        
        detail_file = output_file.parent / 'nodes_detail.json'
        with open(detail_file, 'w', encoding='utf-8') as f:
            json.dump(nodes_detail, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved node details to: {detail_file}")
        
        return graph_data


def integrate_with_demo():
    """
    Update the Connected Papers demo to use real data
    """
    print("\n🔗 Integrating with Connected Papers Demo...")
    
    base_dir = Path("/Users/vaibhavmangroliya/Documents/PY_CODES/SEM_3_PROJECTS/cgb_historical_texts")
    events_file = base_dir / "extracted_events.json"
    graph_file = base_dir / "connected_papers_demo" / "graph_data.json"
    
    if not events_file.exists():
        print("❌ extracted_events.json not found!")
        print("👉 Run step2_extract_events.py first")
        return
    
    # Build graph
    builder = GraphBuilder()
    graph = builder.create_graph_from_events(events_file)
    
    # Save for visualization
    builder.save_for_visualization(graph_file)
    
    print("\n✅ Integration complete!")
    print("\n📝 TODO: Update server.py to:")
    print("   1. Load graph_data.json instead of hardcoded GRAPH_DATA")
    print("   2. Load nodes_detail.json for PAPERS dictionary")
    print("   3. Restart the server")


def main():
    integrate_with_demo()
    
    print("\n💡 Next steps:")
    print("   1. Review graph_data.json and nodes_detail.json")
    print("   2. Update server.py to use the new data")
    print("   3. Run the visualization and see real historical events!")
    print("   4. Manually refine causal relationships")


if __name__ == "__main__":
    main()
