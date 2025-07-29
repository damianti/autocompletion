#!/usr/bin/env python3
"""
Intelligent Autocomplete System

This module implements an autocomplete system based on Trie that searches
through millions of sentences from academic documents and RFCs to provide
intelligent suggestions to the user.

Author: Team 3
Date: 2024
"""

import pandas as pd
import os
import time
import logging
import cProfile
import pstats
import io
import psutil
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from Trie import Trie
from calculate_score import calculate_scores, preprocess_sentence

# Configuration constants
DATA_DIR = "/Archive"
ENGLISH_LETTERS_NUM = 26
MAX_RESULTS = 5
MIN_WORD_LENGTH = 2

# Logging configuration
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
LOGS_DIR = os.path.join(CURR_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOGS_DIR, "application.log")
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class SearchResult:
    """Class to represent a search result"""
    sentence: str
    file_path: str
    score: float
    rank: int


class AutoCompleteSystem:
    """Main autocomplete system"""
    
    def __init__(self):
        self.sentences_df = pd.DataFrame(columns=['sentence', 'file_path'])
        self.words_trie = Trie()
        self.is_initialized = False
        
    def monitor_memory_usage(self) -> float:
        """Monitors memory usage of the process"""
        process = psutil.Process()
        memory_info = process.memory_info()
        rss_mb = memory_info.rss / (1024 * 1024)
        logging.info(f"Memory Usage - RSS: {rss_mb:.2f} MB")
        return rss_mb
    
    def timeit(self, func):
        """Decorator to measure function execution time"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"⏱️  {func.__name__} executed in {execution_time:.2f} seconds")
            logging.info(f"Function {func.__name__} took {execution_time:.2f} seconds")
            return result
        return wrapper
    
    def initialize_words_trie(self, line: str, sentence_id: int) -> None:
        """Initializes Trie with words from a sentence"""
        words = line.split()
        for position, word in enumerate(words):
            self.words_trie.insert(word, sentence_id, position)
    
    def contains_words(self, line: str) -> bool:
        """Checks if a line contains words"""
        return any(c.isalpha() for c in line)
    
    def load_data_files(self) -> None:
        """Loads data files and prepares data structures"""
        logging.info("🔄 Starting file loading and system preparation...")
        print("🔄 Loading files and preparing system...")
        
        self.monitor_memory_usage()
        
        directory = CURR_DIR + DATA_DIR
        sentence_id = 1
        sentences = []
        
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Data directory not found: {directory}")
        
        # Walk through directory and process files
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(subdir, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as txt_file:
                            content = txt_file.read()
                            lines = content.split('\n')
                            
                            for line in lines:
                                line = line.strip()
                                if self.contains_words(line) and len(line) > 0:
                                    sentences.append([line, file])
                                    self.initialize_words_trie(line, sentence_id)
                                    sentence_id += 1
                                    
                    except Exception as e:
                        logging.error(f"Error processing file {file_path}: {e}")
                        continue
        
        self.sentences_df = pd.DataFrame(sentences, columns=['sentence', 'file_path'])
        self.is_initialized = True
        
        print(f"✅ System initialized with {len(sentences)} sentences")
        logging.info(f"System initialized with {len(sentences)} sentences")
        self.monitor_memory_usage()
    
    def filter_sentences_for_short_input(self, input_string: str) -> List[int]:
        """Filters sentences for short inputs (less than 2 words)"""
        input_string = preprocess_sentence(input_string)
        words = input_string.split()
        all_sentence_ids = set()
        
        for word in words:
            word_sentence_ids = set()
            original_match_sentences = self.words_trie.get_sentences_of_word(word) or {}
            word_sentence_ids.update(original_match_sentences.keys())
            
            # Generate word variations (edit distance 1)
            for i in range(len(word)):
                for char_num in range(ENGLISH_LETTERS_NUM):
                    # Add character
                    add_char_before = word[:i] + chr(ord('a') + char_num) + word[i:]
                    # Change character
                    change_char = word[:i] + chr(ord('a') + char_num) + word[i + 1:]
                    # Remove character
                    remove_char = word[:i] + word[i + 1:]
                    
                    # Search variations in Trie
                    for variation in [add_char_before, change_char, remove_char]:
                        match_sentences = self.words_trie.get_sentences_of_word(variation) or {}
                        word_sentence_ids.update(match_sentences.keys())
            
            # Add character at the end
            for char_num in range(ENGLISH_LETTERS_NUM):
                add_char_end = word + chr(ord('a') + char_num)
                match_sentences_end = self.words_trie.get_sentences_of_word(add_char_end) or {}
                word_sentence_ids.update(match_sentences_end.keys())
            
            if not all_sentence_ids:
                all_sentence_ids = word_sentence_ids
            else:
                all_sentence_ids = all_sentence_ids.intersection(word_sentence_ids)
        
        return [index - 1 for index in all_sentence_ids]
    
    @timeit
    def search_matches(self, user_input: str) -> pd.DataFrame:
        """
        Searches for sentences that match user input
        
        Args:
            user_input: User input text
            
        Returns:
            DataFrame with matching sentences
        """
        if not self.is_initialized:
            raise RuntimeError("System has not been initialized")
        
        user_input = user_input.lower().strip()
        if not user_input:
            return pd.DataFrame(columns=['sentence', 'file_path'])
        
        words = user_input.split()
        
        if len(words) >= MIN_WORD_LENGTH:
            # Search for long inputs
            match_sentences = {}
            
            for word_index, word in enumerate(words):
                sentences_that_word_appears = self.words_trie.get_sentences_of_word(word)
                if sentences_that_word_appears:
                    for sentence_id, positions in sentences_that_word_appears.items():
                        if word_index == 0:
                            match_sentences[sentence_id] = 1
                        elif word_index == 1:
                            match_sentences[sentence_id] = match_sentences.get(sentence_id, 0) + 1
                        else:
                            if match_sentences.get(sentence_id, 0) is None:
                                match_sentences[sentence_id] = None
                            elif match_sentences.get(sentence_id, 0) >= word_index - 1:
                                match_sentences[sentence_id] += 1
                            else:
                                match_sentences[sentence_id] = None
            
            # Filter valid results
            matching_sentence_ids = [
                key - 1 for key, value in match_sentences.items() 
                if value is not None and value >= len(words) - 1
            ]
        else:
            # Search for short inputs
            matching_sentence_ids = self.filter_sentences_for_short_input(user_input)
        
        # Get sentences from DataFrame
        if matching_sentence_ids:
            filtered_df = self.sentences_df[self.sentences_df.index.isin(matching_sentence_ids)].copy()
            filtered_df.columns = ['sentence', 'file_path']
        else:
            filtered_df = pd.DataFrame(columns=['sentence', 'file_path'])
        
        self.monitor_memory_usage()
        return filtered_df
    
    def get_autocomplete_suggestions(self, user_input: str) -> List[SearchResult]:
        """
        Gets autocomplete suggestions for user input
        
        Args:
            user_input: User input text
            
        Returns:
            List of autocomplete results ordered by score
        """
        try:
            filtered_df = self.search_matches(user_input)
            
            if filtered_df.empty:
                return []
            
            # Calculate scores and get top results
            top_results = calculate_scores(user_input, filtered_df)
            
            # Convert to SearchResult objects
            search_results = []
            for idx, result in enumerate(top_results, start=1):
                search_result = SearchResult(
                    sentence=result.source_text,
                    file_path=filtered_df.iloc[result.offset - 1]['file_path'] if result.offset > 0 else "N/A",
                    score=result.score,
                    rank=idx
                )
                search_results.append(search_result)
            
            return search_results
            
        except Exception as e:
            logging.error(f"Error in autocomplete search: {e}")
            return []
    
    def display_results(self, results: List[SearchResult]) -> None:
        """Displays autocomplete results elegantly"""
        if not results:
            print("❌ No autocomplete suggestions found")
            return
        
        print(f"\n🎯 Top {len(results)} Autocomplete Suggestions:")
        print("=" * 80)
        
        for result in results:
            print(f"\n{result.rank}. 📄 File: {result.file_path}")
            print(f"   💯 Score: {result.score:.2f}")
            print(f"   📝 Suggestion: {result.sentence}")
            print("-" * 80)


def main():
    """Main program function"""
    print("🚀 Intelligent Autocomplete System")
    print("=" * 50)
    
    # Configure profiling
    profiler = cProfile.Profile()
    profiler.enable()
    
    try:
        # Initialize system
        system = AutoCompleteSystem()
        system.load_data_files()
        
        print(f"\n📊 System Statistics:")
        print(f"   • Total sentences loaded: {len(system.sentences_df):,}")
        print(f"   • Files processed: {system.sentences_df['file_path'].nunique()}")
        print(f"   • Memory used: {system.monitor_memory_usage():.2f} MB")
        
        # Main interaction loop
        while True:
            try:
                print("\n" + "=" * 50)
                user_input = input("💬 Enter your text (or 'quit' to exit): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'salir', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    print("⚠️  Please enter some text")
                    continue
                
                # Get and display suggestions
                results = system.get_autocomplete_suggestions(user_input)
                system.display_results(results)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                print(f"❌ Error: {e}")
    
    except Exception as e:
        logging.error(f"Fatal error in application: {e}")
        print(f"❌ Fatal error: {e}")
    
    finally:
        # Disable profiling and show statistics
        profiler.disable()
        stats_buffer = io.StringIO()
        stats = pstats.Stats(profiler, stream=stats_buffer).sort_stats('cumulative')
        stats.print_stats(20)  # Top 20 functions
        logging.info("Application profiling completed")


if __name__ == "__main__":
    main()
