import json
import re
import math
from collections import defaultdict, Counter
from transformers import pipeline

class HybridCauseEffect:
    """
    BEST APPROACH: Rule-based extraction + ML reranking
    1. Use strict rule-based detection (proven quality)
    2. Add ML confidence score on top
    """
    
    def __init__(self, min_conf=0.85):
        self.min_conf = min_conf
        
        print("Loading NLI model for ML scoring...")
        self.nli = pipeline("zero-shot-classification", 
                           model="valhalla/distilbart-mnli-12-3",
                           device=-1)
        print("Model loaded.\n")
        
        # causal phrases (from proven rule-based approach)
        self.causal_phrases = {
            'forward': [
                r'\b(caused|led to|resulted in|triggered|sparked|brought about)\b',
                r'\b(consequently|therefore|thus|hence|as a result)\b',
                r'\b(in response to|following|after the|due to the)\b',
                r'\bbecause\s+(of\s+)?(the|this|their|our|his|her)\b',
            ],
            'reverse': [
                r'\b(because|due to|owing to|on account of)\b',
                r'\b(as a result of|in consequence of)\b',
                r'\b(was caused by|resulted from)\b',
            ]
        }
        
        self.important_events = {
            'somme', 'verdun', 'ypres', 'passchendaele', 'marne', 'gallipoli',
            'dardanelles', 'jutland', 'arras', 'cambrai', 'vimy', 'amiens',
            'france', 'belgium', 'flanders', 'picardy', 'alsace', 'lorraine',
            'serbia', 'mesopotamia', 'palestine', 'sinai', 'egypt',
            'battalion', 'brigade', 'division', 'regiment', 'corps', 'army',
            'artillery', 'infantry', 'cavalry', 'australian', 'british',
            'french', 'german', 'turkish', 'anzac',
        }
        
        self.excluded = {
            'battle', 'war', 'fight', 'attack', 'front', 'line', 'trench',
            'soldier', 'officer', 'men', 'man', 'enemy', 'troops', 'forces',
        }
        
        self.cause_words = {'bombardment', 'shelling', 'offensive', 'assault', 
                           'raid', 'advance', 'barrage', 'explosion', 'attack'}
        self.effect_words = {'casualties', 'losses', 'killed', 'wounded', 
                            'destroyed', 'captured', 'retreated', 'surrendered'}
        
        self.idf = {}

    def build_idf(self, docs):
        ndocs = len(docs)
        freq = defaultdict(int)
        for doc in docs:
            for w in set(self.tokenize(doc)):
                freq[w] += 1
        for w, f in freq.items():
            self.idf[w] = math.log(ndocs / (1 + f))

    def tokenize(self, text):
        return [w for w in re.sub(r'[^\w\s]', ' ', text.lower()).split() if len(w) > 2]

    def tfidf(self, text):
        words = self.tokenize(text)
        if not words: return {}
        tf = Counter(words)
        mx = max(tf.values())
        return {w: (c/mx) * self.idf.get(w, 0) for w, c in tf.items()}

    def cosine(self, v1, v2):
        if not v1 or not v2: return 0.0
        common = set(v1) & set(v2)
        dot = sum(v1[w] * v2[w] for w in common)
        m1 = math.sqrt(sum(x**2 for x in v1.values()))
        m2 = math.sqrt(sum(x**2 for x in v2.values()))
        return dot / (m1 * m2) if m1 > 0 and m2 > 0 else 0.0

    def has_causal(self, text):
        tl = text.lower()
        for d, pats in self.causal_phrases.items():
            for p in pats:
                if re.search(p, tl): return True, d
        return False, ''

    def get_entities(self, text):
        ents = set()
        tl = text.lower()
        for ev in self.important_events:
            if ev in tl: ents.add(ev)
        for m in re.findall(r'\b([A-Z][a-z]{3,})\b', text):
            if m.lower() not in self.excluded: ents.add(m.lower())
        return ents

    def count_indicators(self, text, words):
        tl = text.lower()
        return sum(1 for w in words if w in tl)

    def rule_score(self, cause_txt, effect_txt, cause_file, effect_file):
        """Rule-based validation (proven approach)"""
        if cause_file == effect_file: return 0, "same file"
        if len(cause_txt) < 50 or len(effect_txt) < 50: return 0, "too short"

        c_has, _ = self.has_causal(cause_txt)
        e_has, _ = self.has_causal(effect_txt)
        if not c_has and not e_has: return 0, "no causal language"

        sim = self.cosine(self.tfidf(cause_txt), self.tfidf(effect_txt))
        if sim < 0.15: return 0, "too different"
        if sim > 0.65: return 0, "too similar"

        c_ents = self.get_entities(cause_txt)
        e_ents = self.get_entities(effect_txt)
        shared = c_ents & e_ents
        if len(shared) < 2: return 0, "no shared context"

        # calculate score
        score = 0.4  # base
        if c_has: score += 0.2
        if e_has: score += 0.15
        score += min(0.15, len(shared) * 0.05)
        if self.count_indicators(cause_txt, self.cause_words): score += 0.05
        if self.count_indicators(effect_txt, self.effect_words): score += 0.05
        
        return score, list(shared)

    def ml_score(self, cause, effect):
        """Add ML confidence"""
        text = f"{cause[:150]}. As a result, {effect[:120]}"
        result = self.nli(text, candidate_labels=["causal relationship", "unrelated"])
        idx = result['labels'].index('causal relationship')
        return result['scores'][idx]

    def find_pairs(self, all_files):
        print("="*60)
        print("HYBRID CAUSE-EFFECT DETECTION")
        print("Rule-based validation + ML scoring")
        print("="*60)

        # build IDF
        sents = []
        for f in all_files:
            sents.extend(f.get('sentences', []))
        self.build_idf(sents)
        print(f"Built IDF from {len(sents)} sentences\n")

        # index
        candidates = []
        for fd in all_files:
            fid = fd['file_id']
            for sent in fd.get('sentences', []):
                if len(sent) < 50: continue
                has_c, _ = self.has_causal(sent)
                c_cnt = self.count_indicators(sent, self.cause_words)
                e_cnt = self.count_indicators(sent, self.effect_words)
                ents = self.get_entities(sent)
                
                if has_c or c_cnt > 0 or e_cnt > 0:
                    candidates.append({'file': fid, 'text': sent, 'ents': ents})

        print(f"Indexed {len(candidates)} candidate sentences")

        # match
        print("Matching and validating...")
        results = []
        seen = set()

        for i, c1 in enumerate(candidates):
            for c2 in candidates:
                if c1['file'] == c2['file']: continue
                if not (c1['ents'] & c2['ents']): continue
                
                key = (c1['text'][:40], c2['text'][:40])
                if key in seen: continue
                seen.add(key)

                rule, shared = self.rule_score(c1['text'], c2['text'], c1['file'], c2['file'])
                if rule >= self.min_conf:
                    results.append({
                        'cause_file': c1['file'],
                        'cause_text': c1['text'],
                        'effect_file': c2['file'],
                        'effect_text': c2['text'],
                        'rule_score': round(rule, 3),
                        'shared_context': shared if isinstance(shared, list) else [],
                    })

        print(f"Rule-based: {len(results)} pairs passed\n")

        # add ML scores
        print("Adding ML scores...")
        for i, r in enumerate(results):
            if i % 20 == 0 and i > 0:
                print(f"  {i}/{len(results)}")
            r['ml_score'] = round(self.ml_score(r['cause_text'], r['effect_text']), 4)
            r['combined_score'] = round((r['rule_score'] + r['ml_score']) / 2, 4)

        # sort by combined score
        results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        print(f"\nTotal quality pairs: {len(results)}")
        return results

    def run(self, infile, outfile):
        with open(infile, 'r') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} files\n")

        results = self.find_pairs(data)

        with open(outfile, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\nSaved {len(results)} pairs to {outfile}")

        if results:
            print("\n" + "="*60)
            print("TOP 8 HIGH-QUALITY CAUSE-EFFECT PAIRS")
            print("="*60)
            for i, r in enumerate(results[:8], 1):
                print(f"\n{i}. Rule: {r['rule_score']:.2f} | ML: {r['ml_score']:.2f} | Combined: {r['combined_score']:.2f}")
                print(f"   Context: {r['shared_context']}")
                print(f"   CAUSE [{r['cause_file']}]:")
                print(f"   {r['cause_text'][:100]}...")
                print(f"   EFFECT [{r['effect_file']}]:")
                print(f"   {r['effect_text'][:100]}...")

        return results


if __name__ == "__main__":
    import sys
    conf = float(sys.argv[1]) if len(sys.argv) > 1 else 0.85

    print("="*60)
    print("HYBRID CAUSAL EXTRACTION")
    print("="*60)
    print("Best of both worlds:")
    print("  - Rule-based: explicit causal language, shared entities")
    print("  - ML: validates logical entailment")
    print("  - Combined score for ranking")
    print("="*60 + "\n")

    detector = HybridCauseEffect(min_conf=conf)
    detector.run('../data/processed_data.json', '../output/cause_effect_ml.json')
