"""
Causal Graph Builder - Data Preprocessing Pipeline
Phase 1: Explore and clean the historical texts dataset

Author: Your Name
Date: October 2025
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import json

class HistoricalTextProcessor:
    def __init__(self, dataset_dir):
        self.dataset_dir = Path(dataset_dir)
        self.documents = []
        self.stats = defaultdict(int)
        
    def load_all_texts(self):
        """Load all text files from the dataset directory"""
        txt_files = list(self.dataset_dir.glob("*.txt"))
        print(f"📁 Found {len(txt_files)} text files")
        
        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self.documents.append({
                        'filename': file_path.name,
                        'content': content,
                        'category': self._categorize_file(file_path.name)
                    })
                    self.stats['total_files'] += 1
            except Exception as e:
                print(f"❌ Error reading {file_path.name}: {e}")
                self.stats['failed_files'] += 1
        
        return self.documents
    
    def _categorize_file(self, filename):
        """Categorize files based on filename patterns"""
        if filename.startswith('diary_'):
            return 'diary'
        elif filename.startswith('battle_'):
            return 'battle'
        elif filename.startswith('british_'):
            return 'letter_british'
        elif filename.startswith('history_'):
            return 'history'
        elif filename.startswith('Harold') or filename.startswith('James'):
            return 'letter_personal'
        else:
            return 'other'
    
    def extract_metadata(self, text):
        """Extract structured metadata from text"""
        metadata = {
            'author': None,
            'date': None,
            'location': None,
            'nationality': None,
            'text_content': None
        }
        
        # Extract Author
        author_match = re.search(r'Author:\s*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if author_match:
            metadata['author'] = author_match.group(1).strip()
        
        # Extract Date
        date_match = re.search(r'Date:\s*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if date_match:
            metadata['date'] = date_match.group(1).strip()
        
        # Extract Location
        location_match = re.search(r'Location:\s*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if location_match:
            metadata['location'] = location_match.group(1).strip()
        
        # Extract Nationality
        nationality_match = re.search(r'Nationality:\s*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if nationality_match:
            metadata['nationality'] = nationality_match.group(1).strip()
        
        # Extract main text content
        text_match = re.search(r'Text:\s*(.+)', text, re.DOTALL | re.IGNORECASE)
        if text_match:
            metadata['text_content'] = text_match.group(1).strip()
        else:
            # If no "Text:" marker, use the whole content
            metadata['text_content'] = text.strip()
        
        return metadata
    
    def analyze_dataset(self):
        """Provide comprehensive statistics about the dataset"""
        categories = defaultdict(int)
        authors = set()
        locations = set()
        dates = []
        
        for doc in self.documents:
            categories[doc['category']] += 1
            
            metadata = self.extract_metadata(doc['content'])
            if metadata['author']:
                authors.add(metadata['author'])
            if metadata['location']:
                locations.add(metadata['location'])
            if metadata['date']:
                dates.append(metadata['date'])
        
        print("\n" + "="*60)
        print("📊 DATASET ANALYSIS")
        print("="*60)
        print(f"\n📁 Total Documents: {len(self.documents)}")
        print(f"\n📚 Categories:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {cat}: {count} files")
        
        print(f"\n✍️  Unique Authors: {len(authors)}")
        print(f"📍 Unique Locations: {len(locations)}")
        print(f"📅 Date Entries: {len([d for d in dates if d != 'Unknown'])}")
        
        # Show sample authors
        if authors:
            print(f"\n👥 Sample Authors:")
            for author in list(authors)[:10]:
                print(f"   • {author}")
        
        # Show sample locations
        if locations:
            print(f"\n🌍 Sample Locations:")
            for loc in list(locations)[:10]:
                print(f"   • {loc}")
        
        print("\n" + "="*60)
    
    def save_processed_data(self, output_file='processed_texts.json'):
        """Save processed data to JSON for further analysis"""
        processed = []
        
        for doc in self.documents:
            metadata = self.extract_metadata(doc['content'])
            processed.append({
                'filename': doc['filename'],
                'category': doc['category'],
                'metadata': metadata,
                'raw_content': doc['content']
            })
        
        output_path = self.dataset_dir.parent / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saved processed data to: {output_path}")
        return output_path


def main():
    # Configure paths
    dataset_dir = "/Users/vaibhavmangroliya/Documents/PY_CODES/SEM_3_PROJECTS/cgb_historical_texts/final_dataset"
    
    print("🚀 Starting Historical Text Processing...")
    print(f"📂 Dataset Directory: {dataset_dir}\n")
    
    # Initialize processor
    processor = HistoricalTextProcessor(dataset_dir)
    
    # Load all texts
    print("📖 Loading all text files...")
    processor.load_all_texts()
    
    # Analyze dataset
    processor.analyze_dataset()
    
    # Save processed data
    processor.save_processed_data()
    
    print("\n✨ Processing complete!")
    print("\n💡 Next steps:")
    print("   1. Review the processed_texts.json file")
    print("   2. Run event extraction on sample texts")
    print("   3. Build causal relationships manually for training")


if __name__ == "__main__":
    main()
