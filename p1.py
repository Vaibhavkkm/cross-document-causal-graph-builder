# Causal Graph Builder for Historical Texts
# Updated prototype: Added rule-based extraction for common causal phrases ('led to', 'caused', 'because of') to capture missed links from the model.
# Combines model summaries with rule-based pairs for more complete, accurate causality (unidirectional where possible).
# Improved matching to include all substring matches per phrase.

import logging
import networkx as nx
import matplotlib.pyplot as plt
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize
import re  # For parsing model output

nltk.download('punkt', quiet=True)  # For sentence tokenization
nltk.download('punkt_tab', quiet=True)  # Additional resource for tokenizer in newer NLTK versions

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Define sample historical texts (placeholders for the dataset)
# These are short excerpts from WWI-inspired narratives. Replace with actual dataset later.
sample_texts = [
    "The assassination of Archduke Franz Ferdinand led to the outbreak of World War I. Austria-Hungary declared war on Serbia because of the assassination.",
    "The sinking of the Lusitania caused the United States to enter the war. Germany’s unrestricted submarine warfare was the main reason."
]

# Step 2: Load Hugging Face models with CPU fallback
# Use device='cpu' to avoid MPS/CUDA issues; change to 0 for GPU if available and stable.
device = 'cpu'  # Or 'mps' if on Mac and stable, or 0 for CUDA
logging.info(f"Loading models on device: {device}")

try:
    ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", device=device,
                            aggregation_strategy="simple")
    cause_effect_extractor = pipeline("summarization", model="taskload/bart-cause-effect", device=device)
except Exception as e:
    logging.error(f"Error loading models: {e}")
    raise


# Step 3: Function to extract events from text
# Uses aggregated NER to get full entities without subwords.
def extract_events(text):
    sentences = sent_tokenize(text)
    events = []
    for sent in sentences:
        ner_results = ner_pipeline(sent)
        # Filter for potential event-like entities (using entity_group)
        event_candidates = [entity['word'] for entity in ner_results if
                            entity['entity_group'] in ['MISC', 'ORG', 'PER', 'LOC']]
        events.extend(event_candidates)  # Append individual entities, not joined
    unique_events = list(set(events))  # Remove duplicates
    logging.info(f"Extracted events: {unique_events}")
    return unique_events


# Step 4.1: Model-based detection (per sentence)
def model_based_causal(events, text):
    causal_pairs = []
    sentences = sent_tokenize(text)
    for sent in sentences:
        if len(sent) < 20:  # Skip short sentences
            continue
        result = cause_effect_extractor(sent, max_length=100, min_length=10, do_sample=False)
        summary = result[0]['summary_text']
        logging.info(f"Sentence summary: {summary}")

        # Parse for pairs
        matches = re.findall(r'Event Trigger:\s*(.+?)\s*Event Description:\s*(.+?)(?:$|\s*Event Trigger:)', summary,
                             re.IGNORECASE | re.DOTALL)
        for cause_phrase, effect_phrase in matches:
            cause_matches = [e for e in events if e.lower() in cause_phrase.lower()]
            effect_matches = [e for e in events if e.lower() in effect_phrase.lower()]
            for cause in cause_matches:
                for effect in effect_matches:
                    if cause != effect:
                        causal_pairs.append((cause, effect))
                        logging.info(f"Model detected pair: ({cause}, {effect})")

    return list(set(causal_pairs))


# Step 4.2: Rule-based detection for common causal phrases
def rule_based_causal(text, events):
    causal_pairs = []
    sentences = sent_tokenize(text)
    for sent in sentences:
        sent_lower = sent.lower()
        # Pattern for 'led to'
        if 'led to' in sent_lower:
            parts = sent_lower.split('led to')
            cause_phrase = parts[0].strip()
            effect_phrase = parts[1].strip()
            cause_matches = [e for e in events if e.lower() in cause_phrase]
            effect_matches = [e for e in events if e.lower() in effect_phrase]
            for cause in cause_matches:
                for effect in effect_matches:
                    if cause != effect:
                        causal_pairs.append((cause, effect))
                        logging.info(f"Rule ('led to') detected pair: ({cause}, {effect})")
        # Pattern for 'caused'
        if 'caused' in sent_lower:
            parts = sent_lower.split('caused')
            cause_phrase = parts[0].strip()
            effect_phrase = parts[1].strip()
            cause_matches = [e for e in events if e.lower() in cause_phrase]
            effect_matches = [e for e in events if e.lower() in effect_phrase]
            for cause in cause_matches:
                for effect in effect_matches:
                    if cause != effect:
                        causal_pairs.append((cause, effect))
                        logging.info(f"Rule ('caused') detected pair: ({cause}, {effect})")
        # Pattern for 'because of' (reverse: effect because of cause)
        if 'because of' in sent_lower:
            parts = sent_lower.split('because of')
            effect_phrase = parts[0].strip()
            cause_phrase = parts[1].strip()
            cause_matches = [e for e in events if e.lower() in cause_phrase]
            effect_matches = [e for e in events if e.lower() in effect_phrase]
            for cause in cause_matches:
                for effect in effect_matches:
                    if cause != effect:
                        causal_pairs.append((cause, effect))
                        logging.info(f"Rule ('because of') detected pair: ({cause}, {effect})")
        # Add more patterns if needed, e.g., 'main reason' as cause
        if 'main reason' in sent_lower:
            parts = sent_lower.split('main reason')
            effect_phrase = parts[0].strip()  # Implied previous context, but for simplicity, skip or link to known
            cause_phrase = parts[1].strip()
            cause_matches = [e for e in events if e.lower() in cause_phrase]
            effect_matches = [e for e in events if e.lower() in effect_phrase]
            for cause in cause_matches:
                for effect in effect_matches:
                    if cause != effect:
                        causal_pairs.append((cause, effect))
                        logging.info(f"Rule ('main reason') detected pair: ({cause}, {effect})")
    return list(set(causal_pairs))


# Step 4: Combined detection
def detect_causal_relations(events, text):
    model_pairs = model_based_causal(events, text)
    rule_pairs = rule_based_causal(text, events)
    return list(set(model_pairs + rule_pairs))  # Combine and deduplicate


# Step 5: Build the graph
def build_graph(events, causal_pairs):
    G = nx.DiGraph()
    G.add_nodes_from(events)
    G.add_edges_from(causal_pairs)
    return G


# Step 6: Visualize the graph
def visualize_graph(G):
    if len(G.nodes) == 0:
        logging.warning("No events found; cannot visualize empty graph.")
        return
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold',
            arrows=True)
    plt.title("Causal Event Graph")
    plt.show()  # In a script, this displays the plot; in Jupyter, use %matplotlib inline


# Step 7: Main pipeline with error handling
def causal_graph_builder(texts):
    all_events = []
    all_causal_pairs = []

    for text in texts:
        try:
            events = extract_events(text)
            causal_pairs = detect_causal_relations(events, text)
            all_events.extend(events)
            all_causal_pairs.extend(causal_pairs)
        except Exception as e:
            logging.error(f"Error processing text: {text[:50]}... - {e}")

    # Deduplicate
    all_events = list(set(all_events))
    all_causal_pairs = list(set(all_causal_pairs))

    if not all_events:
        logging.warning("No events extracted from any texts.")
        return None

    G = build_graph(all_events, all_causal_pairs)
    visualize_graph(G)
    return G


# Run the prototype
if __name__ == "__main__":
    logging.info("Starting causal graph builder...")
    graph = causal_graph_builder(sample_texts)
    if graph:
        print("Graph nodes (events):", graph.nodes())
        print("Graph edges (causal relations):", graph.edges())
    else:
        print("No graph generated due to lack of events.")
    logging.info("Execution complete.")

# Notes for Expansion:
# - Combined model and rule-based for accuracy; rules handle common phrases to catch missed links.
# - Customize rules for more patterns (e.g., 'resulted in', 'due to').
# - For production, annotate data and fine-tune a model like BERT for relation extraction.