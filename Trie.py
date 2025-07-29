#!/usr/bin/env python3
"""
Trie Data Structure Implementation for Efficient Word Search

This module provides an optimized Trie implementation for the autocomplete
system, enabling fast word searches and context retrieval from sentences.

Author: Team 3
Date: 2024
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass


@dataclass
class TrieNode:
    """
    Trie node structure
    
    Attributes:
        char: Character stored in this node
        children: Dictionary of child nodes (character -> node)
        sentences_id: Dictionary mapping sentence IDs to word positions
        is_end_of_word: Indicates if this node marks the end of a word
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children: Dict[str, 'TrieNode'] = {}
        self.sentences_id: Dict[int, List[int]] = {}
        self.is_end_of_word: bool = False
    
    def add_sentence(self, sentence_id: int, position: int) -> None:
        """
        Adds a sentence and position to this node
        
        Args:
            sentence_id: Unique sentence ID
            position: Word position in the sentence
        """
        if sentence_id not in self.sentences_id:
            self.sentences_id[sentence_id] = []
        self.sentences_id[sentence_id].append(position)
    
    def get_sentence_count(self) -> int:
        """Returns the number of unique sentences in this node"""
        return len(self.sentences_id)


class Trie:
    """
    Trie data structure for efficient word search
    
    This implementation provides:
    - Fast word insertion with sentence context
    - Efficient word search
    - Sentence retrieval containing specific words
    - Support for typo-tolerant searches
    """
    
    def __init__(self):
        """Initializes an empty Trie"""
        self.root = TrieNode('')
        self.total_words = 0
        self.total_nodes = 1  # Only root node initially
    
    def insert(self, word: str, sentence_id: int, position: int) -> None:
        """
        Inserts a word into the Trie with context information
        
        Args:
            word: Word to insert
            sentence_id: ID of the sentence containing the word
            position: Position of the word in the sentence
        """
        if not word:
            return
        
        word = word.lower().strip()
        if not word:
            return
        
        node = self.root
        
        # Traverse the word character by character
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char)
                self.total_nodes += 1
            node = node.children[char]
        
        # Mark end of word and add context information
        node.is_end_of_word = True
        node.add_sentence(sentence_id, position)
        self.total_words += 1
    
    def search(self, word: str) -> Optional[TrieNode]:
        """
        Searches for a word in the Trie
        
        Args:
            word: Word to search for
            
        Returns:
            Trie node if the word exists, None otherwise
        """
        if not word:
            return None
        
        word = word.lower().strip()
        node = self.root
        
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node if node.is_end_of_word else None
    
    def get_sentences_of_word(self, word: str) -> Optional[Dict[int, List[int]]]:
        """
        Gets all sentences containing a specific word
        
        Args:
            word: Word to search for
            
        Returns:
            Dictionary mapping sentence IDs to word positions,
            or None if the word doesn't exist
        """
        node = self.search(word)
        return node.sentences_id if node else None
    
    def get_word_count(self) -> int:
        """Returns the total number of unique words in the Trie"""
        return self.total_words
    
    def get_node_count(self) -> int:
        """Returns the total number of nodes in the Trie"""
        return self.total_nodes
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Gets Trie statistics
        
        Returns:
            Dictionary with Trie statistics
        """
        return {
            'total_words': self.total_words,
            'total_nodes': self.total_nodes,
            'average_word_length': self._calculate_average_word_length()
        }
    
    def _calculate_average_word_length(self) -> float:
        """Calculates the average length of words in the Trie"""
        if self.total_words == 0:
            return 0.0
        
        total_length = 0
        self._count_word_lengths(self.root, 0, total_length)
        return total_length / self.total_words
    
    def _count_word_lengths(self, node: TrieNode, current_length: int, total_length: int) -> None:
        """Helper method to count word lengths"""
        if node.is_end_of_word:
            total_length += current_length
        
        for child in node.children.values():
            self._count_word_lengths(child, current_length + 1, total_length)
    
    def prefix_search(self, prefix: str) -> List[str]:
        """
        Searches for all words starting with a given prefix
        
        Args:
            prefix: Prefix to search for
            
        Returns:
            List of words starting with the prefix
        """
        if not prefix:
            return []
        
        prefix = prefix.lower().strip()
        node = self.root
        
        # Navigate to the prefix node
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all words starting with this prefix
        words = []
        self._collect_words_from_node(node, prefix, words)
        return words
    
    def _collect_words_from_node(self, node: TrieNode, current_word: str, words: List[str]) -> None:
        """Helper method to collect words from a node"""
        if node.is_end_of_word:
            words.append(current_word)
        
        for char, child in node.children.items():
            self._collect_words_from_node(child, current_word + char, words)
    
    def fuzzy_search(self, word: str, max_distance: int = 1) -> List[str]:
        """
        Fuzzy search for words with limited edit distance
        
        Args:
            word: Word to search for
            max_distance: Maximum allowed edit distance
            
        Returns:
            List of words matching within the specified distance
        """
        # This is a simplified implementation
        # In a complete implementation, we would use algorithms like Levenshtein
        results = []
        self._fuzzy_search_recursive(self.root, word, "", max_distance, results)
        return results
    
    def _fuzzy_search_recursive(self, node: TrieNode, target: str, current: str, 
                              remaining_distance: int, results: List[str]) -> None:
        """Helper method for recursive fuzzy search"""
        if node.is_end_of_word:
            # Calculate edit distance (simplified implementation)
            if self._levenshtein_distance(current, target) <= remaining_distance:
                results.append(current)
        
        for char, child in node.children.items():
            self._fuzzy_search_recursive(child, target, current + char, 
                                       remaining_distance, results)
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculates Levenshtein distance between two strings"""
        # Simplified implementation - use optimized library in production
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def clear(self) -> None:
        """Clears the Trie, removing all data"""
        self.root = TrieNode('')
        self.total_words = 0
        self.total_nodes = 1

