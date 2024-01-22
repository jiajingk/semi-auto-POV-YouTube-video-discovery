import os
import json
from typing import Iterator, List
class KeywordsGenerator:
    def __init__(self):
        assert os.path.exists('keywords.json')
        with open('keywords.json', 'r', encoding='utf-8') as f:
            self.keywords = json.load(f)
    
    def next_keyworks(self, take: int = 1) -> Iterator[List[str]]:
        total_count = 0
        for catorgory in self.keywords:
            if total_count > take:
                break
            for keyword_sentence in self.keywords[catorgory]:
                if total_count > take:
                    break
                yield keyword_sentence.split(' ')
                total_count += 1
            
