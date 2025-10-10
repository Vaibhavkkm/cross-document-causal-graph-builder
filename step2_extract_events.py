"""
Causal Graph Builder - Event Extraction
Phase 2: Extract events from historical texts using NLP

This script identifies key events, entities, and temporal markers
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    spacy = None

class EventExtractor:
    def __init__(self):
        """Initialize NLP model"""
        if not SPACY_AVAILABLE:
            print("⚠️  spaCy not installed - using simple pattern matching")
            self.nlp = None
        else:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                print("✅ Loaded spaCy model: en_core_web_sm")
            except:
                print("❌ spaCy model not found. Using fallback pattern matching.")
                print("   To use advanced NLP: python -m spacy download en_core_web_sm")
                self.nlp = None
    
    def extract_events_simple(self, text):
        """
        Extract events using simple heuristics
        Events are typically represented by:
        - Action verbs (went, fought, arrived, died)
        - With entities (people, places)
        - And temporal markers (dates, times)
        """
        events = []
        
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Action verbs that typically indicate events
        action_verbs = [
            'went', 'came', 'arrived', 'left', 'fought', 'died', 'born',
            'attacked', 'defended', 'retreated', 'advanced', 'marched',
            'wrote', 'received', 'sent', 'killed', 'wounded', 'captured',
            'launched', 'started', 'ended', 'began', 'finished', 'happened',
            'occurred', 'took place', 'led', 'caused', 'resulted'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short sentences
                continue
            
            # Check if sentence contains action verbs
            sentence_lower = sentence.lower()
            has_action = any(verb in sentence_lower for verb in action_verbs)
            
            if has_action:
                event = {
                    'text': sentence,
                    'type': 'action',
                    'entities': self._extract_entities_simple(sentence),
                    'dates': self._extract_dates(sentence)
                }
                events.append(event)
        
        return events
    
    def extract_events_nlp(self, text):
        """Extract events using spaCy NLP"""
        if not self.nlp:
            return self.extract_events_simple(text)
        
        doc = self.nlp(text)
        events = []
        
        for sent in doc.sents:
            # Look for verbs (which often indicate events)
            verbs = [token for token in sent if token.pos_ == 'VERB']
            
            if verbs:
                event = {
                    'text': sent.text.strip(),
                    'verbs': [v.lemma_ for v in verbs],
                    'entities': {
                        'PERSON': [ent.text for ent in sent.ents if ent.label_ == 'PERSON'],
                        'GPE': [ent.text for ent in sent.ents if ent.label_ == 'GPE'],
                        'DATE': [ent.text for ent in sent.ents if ent.label_ == 'DATE'],
                        'ORG': [ent.text for ent in sent.ents if ent.label_ == 'ORG'],
                        'LOC': [ent.text for ent in sent.ents if ent.label_ == 'LOC']
                    },
                    'subject': self._get_subject(sent),
                    'object': self._get_object(sent)
                }
                events.append(event)
        
        return events
    
    def _extract_entities_simple(self, text):
        """Simple entity extraction using patterns"""
        entities = {
            'PERSON': [],
            'LOCATION': [],
            'DATE': []
        }
        
        # Find capitalized words (potential names/places)
        words = text.split()
        for i, word in enumerate(words):
            if word and word[0].isupper() and len(word) > 2:
                # Check if it's likely a person or place
                if word not in ['The', 'A', 'An', 'I', 'We', 'They', 'He', 'She']:
                    entities['PERSON'].append(word)
        
        # Find dates
        entities['DATE'] = self._extract_dates(text)
        
        return entities
    
    def _extract_dates(self, text):
        """Extract date patterns"""
        date_patterns = [
            r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',
            r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
            r'\d{1,2}/\d{1,2}/\d{2,4}',
            r'\d{4}-\d{2}-\d{2}'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return dates
    
    def _get_subject(self, sent):
        """Extract subject of sentence"""
        for token in sent:
            if token.dep_ in ('nsubj', 'nsubjpass'):
                return token.text
        return None
    
    def _get_object(self, sent):
        """Extract object of sentence"""
        for token in sent:
            if token.dep_ in ('dobj', 'pobj'):
                return token.text
        return None
    
    def identify_causal_patterns(self, events):
        """
        Identify potential causal relationships based on:
        - Temporal ordering (A before B)
        - Causal keywords (because, caused, led to, resulted in)
        - Logical flow
        """
        causal_keywords = [
            'because', 'caused', 'led to', 'resulted in', 'due to',
            'as a result', 'consequently', 'therefore', 'thus',
            'so that', 'in order to', 'triggered', 'brought about'
        ]
        
        causal_relations = []
        
        for i, event in enumerate(events):
            text_lower = event['text'].lower()
            
            # Check for causal keywords
            for keyword in causal_keywords:
                if keyword in text_lower:
                    # This event likely has a causal relationship
                    causal_relations.append({
                        'event_index': i,
                        'event_text': event['text'],
                        'causal_keyword': keyword,
                        'type': 'explicit_causal'
                    })
        
        # Check temporal ordering (events with dates)
        dated_events = [(i, e) for i, e in enumerate(events) if e.get('dates')]
        if len(dated_events) > 1:
            for i in range(len(dated_events) - 1):
                causal_relations.append({
                    'source': dated_events[i][0],
                    'target': dated_events[i+1][0],
                    'type': 'temporal_sequence'
                })
        
        return causal_relations


def process_sample_documents(input_file, output_file, sample_size=10):
    """Process a sample of documents to extract events"""
    
    print(f"\n🔍 Processing sample documents...")
    
    # Load processed texts
    with open(input_file, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    print(f"📚 Loaded {len(documents)} documents")
    
    # If sample_size is None, process all documents
    if sample_size is None:
        sample_size = len(documents)
        print(f"🎯 Processing ALL {sample_size} documents\n")
    else:
        print(f"🎯 Processing first {sample_size} documents\n")
    
    # Initialize extractor
    extractor = EventExtractor()
    
    results = []
    
    for i, doc in enumerate(documents[:sample_size]):
        print(f"📄 Processing: {doc['filename']} ({i+1}/{sample_size})")
        
        text_content = doc['metadata'].get('text_content', doc['raw_content'])
        
        # Extract events
        if extractor.nlp:
            events = extractor.extract_events_nlp(text_content[:5000])  # Limit text length
        else:
            events = extractor.extract_events_simple(text_content[:5000])
        
        # Identify causal relationships
        causal_relations = extractor.identify_causal_patterns(events)
        
        result = {
            'filename': doc['filename'],
            'category': doc['category'],
            'author': doc['metadata'].get('author'),
            'date': doc['metadata'].get('date'),
            'location': doc['metadata'].get('location'),
            'events': events[:20],  # Limit to top 20 events
            'causal_relations': causal_relations,
            'num_events': len(events),
            'num_causal_relations': len(causal_relations)
        }
        
        results.append(result)
        print(f"   ✓ Found {len(events)} events, {len(causal_relations)} causal relations\n")
    
    # Save results
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved event extraction results to: {output_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 EVENT EXTRACTION SUMMARY")
    print("="*60)
    total_events = sum(r['num_events'] for r in results)
    total_causal = sum(r['num_causal_relations'] for r in results)
    print(f"Total Events Extracted: {total_events}")
    print(f"Total Causal Relations: {total_causal}")
    print(f"Average Events per Document: {total_events/len(results):.1f}")
    print("="*60)


def main():
    base_dir = Path("/Users/vaibhavmangroliya/Documents/PY_CODES/SEM_3_PROJECTS/cgb_historical_texts")
    
    input_file = base_dir / "processed_texts.json"
    output_file = base_dir / "extracted_events.json"
    
    if not input_file.exists():
        print("❌ processed_texts.json not found!")
        print("👉 Run step1_preprocess.py first")
        return
    
    # Process ALL documents (change sample_size to None for all, or set a number)
    process_sample_documents(input_file, output_file, sample_size=None)  # Changed from 20 to None for ALL files
    
    print("\n💡 Next steps:")
    print("   1. Review extracted_events.json")
    print("   2. Manually annotate causal relationships for training")
    print("   3. Build visualization with these events")


if __name__ == "__main__":
    main()
