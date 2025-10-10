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
        
        # Add MORE links based on similarity to make it dense like Connected Papers
        self._add_similarity_links()
        
        print(f"✅ After adding similarity links: {len(self.links)} total links")
        
        return {
            'nodes': self.nodes,
            'links': self.links
        }
    
    def _add_similarity_links(self):
        """Add links between similar events (same year, location, author, etc.)"""
        print("🔗 Adding similarity-based connections...")
        
        # Group nodes by year for temporal connections
        year_groups = defaultdict(list)
        for node in self.nodes:
            year_groups[node['year']].append(node['id'])
        
        # Connect events in same year
        for year, node_ids in year_groups.items():
            if len(node_ids) > 1:
                # Connect each node to 2-3 nearby nodes in same year
                for i, node_id in enumerate(node_ids):
                    # Connect to next 2 nodes (circular)
                    for j in range(1, min(3, len(node_ids))):
                        target_idx = (i + j) % len(node_ids)
                        if node_id != node_ids[target_idx]:
                            self.links.append({
                                'source': node_id,
                                'target': node_ids[target_idx],
                                'weight': 1,
                                'type': 'temporal_proximity'
                            })
        
        # ADD BRIDGE CONNECTIONS BETWEEN YEARS to pull clusters together
        sorted_years = sorted(year_groups.keys())
        for i in range(len(sorted_years) - 1):
            year1 = sorted_years[i]
            year2 = sorted_years[i + 1]
            
            # Connect 3-5 random nodes between consecutive years
            nodes1 = year_groups[year1]
            nodes2 = year_groups[year2]
            
            import random
            num_bridges = min(5, len(nodes1), len(nodes2))
            for _ in range(num_bridges):
                source = random.choice(nodes1)
                target = random.choice(nodes2)
                self.links.append({
                    'source': source,
                    'target': target,
                    'weight': 1,
                    'type': 'year_bridge'
                })
        
        # Group by author for author connections
        author_groups = defaultdict(list)
        for node in self.nodes:
            if node['author'] != 'Unknown':
                author_groups[node['author']].append(node['id'])
        
        # Connect events by same author
        for author, node_ids in author_groups.items():
            if len(node_ids) > 1:
                for i in range(len(node_ids) - 1):
                    self.links.append({
                        'source': node_ids[i],
                        'target': node_ids[i + 1],
                        'weight': 2,
                        'type': 'same_author'
                    })
        
        # Group by location for location connections  
        location_groups = defaultdict(list)
        for node in self.nodes:
            if node['location'] != 'Unknown':
                location_groups[node['location']].append(node['id'])
        
        # Connect events at same location
        for location, node_ids in location_groups.items():
            if len(node_ids) > 1 and len(node_ids) < 20:  # Only for reasonable groups
                for i in range(len(node_ids) - 1):
                    self.links.append({
                        'source': node_ids[i],
                        'target': node_ids[i + 1],
                        'weight': 1,
                        'type': 'same_location'
                    })
        
        # ADD CROSS-CLUSTER BRIDGES between different documents
        doc_groups = defaultdict(list)
        for node in self.nodes:
            doc_groups[node['document']].append(node['id'])
        
        # Connect first node of each document to create a connected graph
        all_docs = list(doc_groups.keys())
        for i in range(len(all_docs) - 1):
            if doc_groups[all_docs[i]] and doc_groups[all_docs[i + 1]]:
                self.links.append({
                    'source': doc_groups[all_docs[i]][0],
                    'target': doc_groups[all_docs[i + 1]][0],
                    'weight': 1,
                    'type': 'document_bridge'
                })
    
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
