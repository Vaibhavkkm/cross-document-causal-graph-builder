import json
import re
import math
from collections import defaultdict, Counter

class CauseEffectDetector:
    def __init__(self, min_conf=0.85):
        self.min_conf = min_conf
        
        # causal phrases to look for
        self.causal_phrases = {
            'forward': [
                r'\b(caused|led to|resulted in|triggered|sparked|brought about)\b',
                r'\b(consequently|therefore|thus|hence|as a result)\b',
                r'\b(in response to|following|after the|due to the)\b',
                r'\bwhen\s+.{10,60}\s*,\s*.{10,60}(then|we|they|he|she|it)\b',
                r'\bbecause\s+(of\s+)?(the|this|their|our|his|her)\b',
            ],
            'reverse': [
                r'\b(because|due to|owing to|on account of)\b',
                r'\b(as a result of|in consequence of)\b',
                r'\b(was caused by|resulted from)\b',
            ]
        }
        
        # important events and locations
        self.important_events = {
            'somme', 'verdun', 'ypres', 'passchendaele', 'marne', 'gallipoli',
            'dardanelles', 'jutland', 'arras', 'cambrai', 'vimy', 'amiens',
            'messines', 'belleau', 'meuse-argonne', 'caporetto', 'tannenberg',
            'france', 'belgium', 'flanders', 'picardy', 'alsace', 'lorraine',
            'serbia', 'gallipoli peninsula', 'mesopotamia', 'palestine',
            'sinai', 'egypt', 'salonika', 'cape helles', 'anzac cove',
            'battalion', 'brigade', 'division', 'regiment', 'corps', 'army',
            'artillery', 'infantry', 'cavalry', 'australian', 'british',
            'french', 'german', 'turkish', 'anzac',
        }
        
        # words to exclude from entity matching
        self.excluded = {
            'battle', 'war', 'fight', 'attack', 'front', 'line', 'trench',
            'soldier', 'officer', 'men', 'man', 'enemy', 'troops', 'forces',
            'the', 'they', 'we', 'he', 'she', 'it', 'when', 'then', 'after',
            'before', 'during', 'about', 'with', 'from', 'into', 'over',
            'wounded', 'killed', 'dead', 'hospital', 'ambulance', 'casualty',
            'shell', 'gun', 'rifle', 'bomb', 'bullet', 'fire', 'shot',
        }
        
        # action indicators (causes)
        self.cause_words = {
            'bombardment', 'shelling', 'artillery fire', 'machine gun fire',
            'gas attack', 'offensive', 'assault', 'raid', 'advance',
            'counter-attack', 'barrage', 'explosion', 'ambush', 'charge',
            'opened fire', 'attacked', 'bombed', 'torpedoed', 'mined',
        }
        
        # consequence indicators (effects)
        self.effect_words = {
            'casualties', 'losses', 'killed', 'wounded', 'injured', 'died',
            'destroyed', 'captured', 'retreated', 'surrendered', 'evacuated',
            'hospitalized', 'amputation', 'shell shock', 'blinded', 'gassed',
            'reinforcements', 'relief', 'treatment', 'operation',
        }
        
        self.idf = {}
        self.ndocs = 0

    def build_idf(self, docs):
        print("  Building IDF...")
        self.ndocs = len(docs)
        freq = defaultdict(int)
        for doc in docs:
            for w in set(self.tokenize(doc)):
                freq[w] += 1
        for w, f in freq.items():
            self.idf[w] = math.log(self.ndocs / (1 + f))
        print(f"    {len(self.idf):,} words")

    def tokenize(self, text):
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        return [w for w in text.split() if len(w) > 2]

    def tfidf(self, text):
        words = self.tokenize(text)
        if not words:
            return {}
        tf = Counter(words)
        mx = max(tf.values())
        return {w: (c/mx) * self.idf.get(w, 0) for w, c in tf.items()}

    def cosine(self, v1, v2):
        if not v1 or not v2:
            return 0.0
        common = set(v1) & set(v2)
        dot = sum(v1[w] * v2[w] for w in common)
        m1 = math.sqrt(sum(x**2 for x in v1.values()))
        m2 = math.sqrt(sum(x**2 for x in v2.values()))
        return dot / (m1 * m2) if m1 > 0 and m2 > 0 else 0.0

    def has_causal(self, text):
        tl = text.lower()
        for d, pats in self.causal_phrases.items():
            for p in pats:
                m = re.search(p, tl)
                if m:
                    return True, d, m.group(0)
        return False, '', ''

    def get_entities(self, text):
        ents = set()
        tl = text.lower()
        for ev in self.important_events:
            if ev in tl:
                ents.add(ev)
        # dates
        for p in [r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b', r'\b\d{4}\b']:
            for m in re.findall(p, tl):
                ents.add(m if isinstance(m, str) else m[0])
        # unit numbers
        for m in re.findall(r'\b(\d+(?:st|nd|rd|th)?\s+(?:battalion|brigade|division|regiment))\b', tl):
            ents.add(m)
        # proper nouns
        for m in re.findall(r'\b([A-Z][a-z]{3,})\b', text):
            if m.lower() not in self.excluded:
                ents.add(m.lower())
        return {e for e in ents if e.lower() not in self.excluded}

    def count_indicators(self, text, words):
        tl = text.lower()
        return sum(1 for w in words if w in tl)

    def validate(self, cause_txt, effect_txt, cause_file, effect_file):
        details = {'reasons': []}
        score = 0.0
        
        if cause_file == effect_file:
            return False, 0.0, {'rejection': 'Same file'}
        if len(cause_txt) < 50 or len(effect_txt) < 50:
            return False, 0.0, {'rejection': 'Too short'}

        c_has, c_dir, c_phrase = self.has_causal(cause_txt)
        e_has, e_dir, e_phrase = self.has_causal(effect_txt)
        
        if not c_has and not e_has:
            return False, 0.0, {'rejection': 'No causal language'}

        if c_has:
            score += 0.30
            details['reasons'].append(f'Causal phrase in cause: "{c_phrase}" (+0.30)')
        if e_has:
            score += 0.25
            details['reasons'].append(f'Causal phrase in effect: "{e_phrase}" (+0.25)')

        sim = self.cosine(self.tfidf(cause_txt), self.tfidf(effect_txt))
        if sim < 0.15:
            return False, 0.0, {'rejection': f'Low similarity ({sim:.3f})'}
        if sim > 0.65:
            return False, 0.0, {'rejection': f'Too similar ({sim:.3f})'}
        
        if 0.25 <= sim <= 0.50:
            score += 0.20
            details['reasons'].append(f'Good semantic similarity: {sim:.3f} (+0.20)')
        elif 0.15 <= sim < 0.25:
            score += 0.10
            details['reasons'].append(f'Moderate semantic similarity: {sim:.3f} (+0.10)')

        c_ents = self.get_entities(cause_txt)
        e_ents = self.get_entities(effect_txt)
        shared = c_ents & e_ents
        
        if len(shared) < 2:
            return False, 0.0, {'rejection': f'Not enough shared entities ({len(shared)})'}
        
        ent_score = min(0.25, len(shared) * 0.08)
        score += ent_score
        details['reasons'].append(f'Shared entities: {list(shared)[:5]} (+{ent_score:.2f})')

        c_ind = self.count_indicators(cause_txt, self.cause_words)
        e_ind = self.count_indicators(effect_txt, self.effect_words)
        if c_ind > 0:
            score += 0.10
            details['reasons'].append(f'Cause has {c_ind} action indicators (+0.10)')
        if e_ind > 0:
            score += 0.10
            details['reasons'].append(f'Effect has {e_ind} consequence indicators (+0.10)')

        valid = score >= self.min_conf
        if not valid:
            details['rejection'] = f'Score {score:.2f} below {self.min_conf}'
        return valid, min(score, 1.0), details

    def find_relationships(self, all_files):
        print("\n" + "="*60)
        print("Cross-file cause-effect detection")
        print("="*60)
        
        sentences = []
        for f in all_files:
            sentences.extend(f.get('sentences', []))
        self.build_idf(sentences)

        print("\n  Indexing sentences...")
        causes = []
        effects = []
        
        for fd in all_files:
            fid = fd['file_id']
            for idx, sent in enumerate(fd.get('sentences', [])):
                if len(sent) < 50:
                    continue
                has_c, direction, _ = self.has_causal(sent)
                c_cnt = self.count_indicators(sent, self.cause_words)
                e_cnt = self.count_indicators(sent, self.effect_words)
                ents = self.get_entities(sent)
                
                if has_c or c_cnt > 0 or e_cnt > 0:
                    entry = {'file': fid, 'line': idx, 'text': sent, 'entities': ents,
                             'has_causal': has_c, 'dir': direction, 'c_cnt': c_cnt, 'e_cnt': e_cnt}
                    if c_cnt > e_cnt or direction == 'forward':
                        causes.append(entry)
                    if e_cnt > c_cnt or direction == 'reverse' or has_c:
                        effects.append(entry)

        print(f"    {len(causes):,} potential causes")
        print(f"    {len(effects):,} potential effects")

        print("\n  Matching...")
        results = []
        seen = set()
        rejections = defaultdict(int)

        for i, cause in enumerate(causes):
            if i % 200 == 0 and i > 0:
                print(f"    {i}/{len(causes)} | found: {len(results)}")
            
            for effect in effects:
                if effect['file'] == cause['file']:
                    continue
                if not (cause['entities'] & effect['entities']):
                    continue
                
                key = (cause['file'], cause['line'], effect['file'], effect['line'])
                if key in seen:
                    continue
                seen.add(key)

                valid, conf, det = self.validate(cause['text'], effect['text'], cause['file'], effect['file'])
                if valid:
                    results.append({
                        'type': 'cross_file',
                        'cause_file': cause['file'],
                        'cause_text': cause['text'],
                        'effect_file': effect['file'],
                        'effect_text': effect['text'],
                        'confidence': round(conf, 3)
                    })
                else:
                    rejections[det.get('rejection', 'Unknown')] += 1

        print(f"\n  Done: {len(results):,} found, {sum(rejections.values()):,} rejected")
        return results

    def run(self, infile, outfile):
        print("="*60)
        print("Cause-Effect Detector")
        print("="*60)
        
        with open(infile, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {len(data):,} files")
        
        results = self.find_relationships(data)
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved {len(results):,} relationships to {outfile}")
        
        # show top results
        if results:
            print("\nTop results:")
            for i, r in enumerate(results[:5], 1):
                print(f"\n{i}. [{r['confidence']:.2f}] {r['cause_file']} -> {r['effect_file']}")
                print(f"   Cause: {r['cause_text'][:100]}...")
                print(f"   Effect: {r['effect_text'][:100]}...")
        
        return results


if __name__ == "__main__":
    import sys
    threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 0.85
    
    detector = CauseEffectDetector(min_conf=threshold)
    detector.run('../data/processed_data.json', '../output/cause_effect_rulebased.json')
