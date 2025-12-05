import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# load data
with open('../output/cause_effect_results_final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} relationships")

G = nx.DiGraph()
events = {}
counter = 1

cause_nodes = set()
effect_nodes = set()

for rel in data:
    cause_key = (rel['cause_file'], rel['cause_text'][:100])
    effect_key = (rel['effect_file'], rel['effect_text'][:100])
    
    if cause_key not in events:
        cid = f"C{counter}"
        events[cause_key] = {'id': cid, 'file': rel['cause_file'], 'text': rel['cause_text'], 'type': 'cause'}
        cause_nodes.add(cid)
        counter += 1
    else:
        cid = events[cause_key]['id']
    
    if effect_key not in events:
        eid = f"E{counter}"
        events[effect_key] = {'id': eid, 'file': rel['effect_file'], 'text': rel['effect_text'], 'type': 'effect'}
        effect_nodes.add(eid)
        counter += 1
    else:
        eid = events[effect_key]['id']
    
    G.add_node(cid, type='cause', file=rel['cause_file'])
    G.add_node(eid, type='effect', file=rel['effect_file'])
    G.add_edge(cid, eid, confidence=rel['confidence'])

print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# visualization
fig, ax = plt.subplots(figsize=(20, 16))
pos = nx.spring_layout(G, k=0.5, iterations=100, seed=42, scale=2)

causes = [n for n in G.nodes() if G.nodes[n].get('type') == 'cause']
effects = [n for n in G.nodes() if G.nodes[n].get('type') == 'effect']

# edges
nx.draw_networkx_edges(G, pos, edge_color='red', alpha=0.5, arrows=True, 
                       arrowsize=12, width=1.2, style='dashed',
                       connectionstyle='arc3,rad=0.08', ax=ax)

# cause nodes (light blue)
nx.draw_networkx_nodes(G, pos, nodelist=causes, node_color='#87CEEB',
                       node_size=500, alpha=0.9, edgecolors='#333', linewidths=1, ax=ax)

# effect nodes (light green)  
nx.draw_networkx_nodes(G, pos, nodelist=effects, node_color='#90EE90',
                       node_size=500, alpha=0.9, edgecolors='#333', linewidths=1, ax=ax)

# labels
nx.draw_networkx_labels(G, pos, {n: n for n in G.nodes()}, font_size=6, font_weight='bold', ax=ax)

# legend
legend = [
    mpatches.Patch(facecolor='#87CEEB', edgecolor='#333', label='Cause (Source docs)'),
    mpatches.Patch(facecolor='#90EE90', edgecolor='#333', label='Effect (Extracted)'),
    plt.Line2D([0], [0], color='red', linewidth=2, linestyle='--', label='Causal link')
]
ax.legend(handles=legend, loc='upper right', fontsize=10, title='Legend')

plt.title(f'Events Network - {len(causes)} Causes, {len(effects)} Effects', fontsize=14, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig('../output/events.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved output/events.png")

# save mapping
with open('../output/cause_effect_mapping.txt', 'w', encoding='utf-8') as f:
    f.write("EVENT MAPPING\n" + "="*60 + "\n\n")
    for key, ev in sorted(events.items(), key=lambda x: x[1]['id']):
        f.write(f"{ev['id']} [{ev['file']}]: {ev['text'][:150]}...\n\n")

print("Saved output/cause_effect_mapping.txt")
print(f"\nStats: {len(causes)} causes, {len(effects)} effects, {G.number_of_edges()} relationships")
