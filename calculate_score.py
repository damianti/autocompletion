#!/usr/bin/env python3
"""
Scoring System for Autocomplete

This module implements scoring algorithms to evaluate the quality of
autocomplete suggestions based on textual similarity, word position,
and typo penalties.

Author: Team 3
Date: 2024
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import string
import logging

try:
    import Levenshtein
    LEVENSHTEIN_AVAILABLE = True
except ImportError:
    LEVENSHTEIN_AVAILABLE = False
    logging.warning("Levenshtein not available, using basic implementation")


# Constants for error types
class ErrorTypes:
    """Supported typo error types"""
    ADDITION = "addition"
    DELETION = "deletion"
    SUBSTITUTION = "substitution"


@dataclass
class AutoCompleteData:
    """
    Autocomplete suggestion data
    
    Attributes:
        completed_sentence: Suggested completed sentence
        source_text: Original source text
        offset: Starting position in source text
        score: Calculated score for this suggestion
    """
    completed_sentence: str
    source_text: str
    offset: int
    score: float
    
    def __post_init__(self):
        """Post-initialization validation"""
        if self.score < 0:
            logging.warning(f"Negative score detected: {self.score}")


class ScoreCalculator:
    """
    Score calculator for autocomplete suggestions
    
    This class implements algorithms to evaluate suggestion quality
    based on multiple criteria.
    """
    
    def __init__(self):
        """Initializes the score calculator"""
        self.punctuation_translator = str.maketrans("", "", string.punctuation)
        
        # Penalty configuration
        self.penalty_config = {
            ErrorTypes.SUBSTITUTION: {
                0: 5,  # First position
                1: 4,  # Second position
                2: 3,  # Third position
                3: 2,  # Fourth position
                'default': 1  # Later positions
            },
            ErrorTypes.ADDITION: {
                0: 10,
                1: 8,
                2: 6,
                3: 4,
                'default': 2
            },
            ErrorTypes.DELETION: {
                0: 10,
                1: 8,
                2: 6,
                3: 4,
                'default': 2
            }
        }
    
    def preprocess_sentence(self, sentence: str) -> str:
        """
        Preprocesses a sentence by removing punctuation and normalizing
        
        Args:
            sentence: Sentence to preprocess
            
        Returns:
            Preprocessed sentence in lowercase without punctuation
        """
        if not sentence:
            return ""
        
        # Remove punctuation and convert to lowercase
        processed = sentence.translate(self.punctuation_translator).lower()
        # Normalize multiple spaces
        processed = ' '.join(processed.split())
        return processed
    
    def increment_score(self, current_score: float, word: str) -> float:
        """
        Increments score based on word length
        
        Args:
            current_score: Current score
            word: Word contributing to the score
            
        Returns:
            New incremented score
        """
        return current_score + len(word) * 2
    
    def calculate_penalty(self, position: int, penalty_type: str) -> float:
        """
        Calculates penalty based on position and error type
        
        Args:
            position: Error position in the word
            penalty_type: Error type (addition, deletion, substitution)
            
        Returns:
            Calculated penalty value
        """
        if penalty_type not in self.penalty_config:
            return 0.0
        
        penalties = self.penalty_config[penalty_type]
        return penalties.get(position, penalties['default'])
    
    def penalty_score(self, sentence: List[str], sentence_word: str, 
                     user_word: str, current_score: float, penalty_type: str) -> float:
        """
        Applies penalty to score based on error type
        
        Args:
            sentence: List of sentence words
            sentence_word: Word from the sentence
            user_word: User's word
            current_score: Current score
            penalty_type: Error type
            
        Returns:
            Score adjusted with penalty
        """
        if sentence_word not in sentence:
            return current_score
        
        if user_word == sentence_word:
            return current_score
        
        position = sentence.index(sentence_word)
        penalty = self.calculate_penalty(position, penalty_type)
        return current_score - penalty
    
    def calculate_change_type(self, user_word: str, sentence_word: str) -> Optional[str]:
        """
        Determines the type of change between two words
        
        Args:
            user_word: User's word
            sentence_word: Word from the sentence
            
        Returns:
            Change type or None if no distance 1 change
        """
        if LEVENSHTEIN_AVAILABLE:
            distance = Levenshtein.distance(user_word, sentence_word)
        else:
            distance = self._basic_levenshtein_distance(user_word, sentence_word)
        
        if distance == 1:
            if len(user_word) == len(sentence_word):
                return ErrorTypes.SUBSTITUTION
            elif len(user_word) < len(sentence_word):
                return ErrorTypes.DELETION
            else:
                return ErrorTypes.ADDITION
        return None
    
    def _basic_levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Basic Levenshtein distance implementation
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            Levenshtein distance between the strings
        """
        if len(s1) < len(s2):
            return self._basic_levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        # Use dynamic programming for better performance
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
    
    def calculate_similarity_score(self, word1: str, word2: str) -> float:
        """
        Calculates similarity score between two words (0.0 to 1.0)
        
        Args:
            word1: First word
            word2: Second word
            
        Returns:
            Similarity score between 0.0 (completely different) and 1.0 (identical)
        """
        if not word1 or not word2:
            return 0.0
        
        if word1 == word2:
            return 1.0
        
        # Calculate Levenshtein distance
        distance = self._basic_levenshtein_distance(word1, word2)
        
        # Calculate similarity based on distance and word lengths
        max_length = max(len(word1), len(word2))
        if max_length == 0:
            return 1.0
        
        # Normalize distance and convert to similarity
        similarity = 1.0 - (distance / max_length)
        
        # Apply bonus for words with similar lengths
        length_diff = abs(len(word1) - len(word2))
        length_penalty = length_diff / max_length * 0.1
        
        return max(0.0, similarity - length_penalty)
    
    def get_word_variations(self, word: str) -> List[str]:
        """
        Generates common word variations for fuzzy matching
        
        Args:
            word: Base word
            
        Returns:
            List of word variations
        """
        if not word:
            return []
        
        variations = [word]
        
        # Add common typos and variations
        for i in range(len(word)):
            # Character substitutions
            for char in 'abcdefghijklmnopqrstuvwxyz':
                if char != word[i]:
                    variation = word[:i] + char + word[i+1:]
                    variations.append(variation)
            
            # Character deletions
            if len(word) > 1:
                variation = word[:i] + word[i+1:]
                variations.append(variation)
            
            # Character insertions
            for char in 'abcdefghijklmnopqrstuvwxyz':
                variation = word[:i] + char + word[i:]
                variations.append(variation)
        
        # Add character at the end
        for char in 'abcdefghijklmnopqrstuvwxyz':
            variation = word + char
            variations.append(variation)
        
        return list(set(variations))  # Remove duplicates
    
    def update_results_list(self, results_list: List[AutoCompleteData], 
                           new_data: AutoCompleteData, min_top_score: float) -> Tuple[List[AutoCompleteData], float]:
        """
        Updates results list keeping only the best ones
        
        Args:
            results_list: Current results list
            new_data: New result to consider
            min_top_score: Current minimum score
            
        Returns:
            Tuple with updated list and new minimum score
        """
        max_results = 5
        
        if len(results_list) < max_results:
            results_list.append(new_data)
            min_top_score = min(min_top_score, new_data.score)
        elif new_data.score > min_top_score:
            # Replace worst result
            min_score_index = min(enumerate(results_list), key=lambda x: x[1].score)[0]
            results_list[min_score_index] = new_data
            min_top_score = min(results_list, key=lambda x: x.score).score
        
        return results_list, min_top_score
    
    def calculate_scores(self, user_sentence: str, sentences_df) -> List[AutoCompleteData]:
        """
        Calculates scores for all candidate sentences
        
        Args:
            user_sentence: User input sentence
            sentences_df: DataFrame with candidate sentences
            
        Returns:
            List of top 5 results ordered by score
        """
        if sentences_df.empty:
            return []
        
        autocomplete_results = []
        user_sentence = self.preprocess_sentence(user_sentence)
        user_words = user_sentence.split()
        
        if not user_words:
            return []
        
        for index, row in sentences_df.iterrows():
            try:
                score_data = self._calculate_single_sentence_score(
                    user_words, row['sentence'], user_sentence
                )
                if score_data:
                    autocomplete_results.append(score_data)
            except Exception as e:
                logging.error(f"Error calculating score for sentence {index}: {e}")
                continue
        
        # Sort by descending score and take the best
        autocomplete_results.sort(key=lambda x: x.score, reverse=True)
        return autocomplete_results[:5]
    
    def _calculate_single_sentence_score(self, user_words: List[str], 
                                       sentence: str, user_sentence: str) -> Optional[AutoCompleteData]:
        """
        Calculates score for a single sentence
        
        Args:
            user_words: User's words
            sentence: Candidate sentence
            user_sentence: Complete user sentence
            
        Returns:
            Autocomplete data with calculated score
        """
        position = 0
        score = 0.0
        one_change_found = False
        offset = 0
        
        processed_sentence = self.preprocess_sentence(sentence)
        processed_sentence_words = processed_sentence.split()
        
        for word in user_words:
            if word in processed_sentence_words[position:]:
                # Word found exactly
                score = self.increment_score(score, word)
                position = processed_sentence_words.index(word, position)
                if user_words.index(word) == 0:
                    offset = position + 1
            elif not one_change_found:
                # Search for word variations
                for i, sentence_word in enumerate(processed_sentence_words[position:], position):
                    change_type = self.calculate_change_type(word, sentence_word)
                    if change_type:
                        score = self.penalty_score(
                            processed_sentence_words, sentence_word, word, score, change_type
                        )
                        one_change_found = True
                        position = i
                        break
                else:
                    # No match found
                    score = float('-inf')
            else:
                # Already allowed one change, no more
                score = float('-inf')
                break
        
        # Add score for spaces in the sentence
        score += (2 * len(processed_sentence_words) - 1)
        
        if score == float('-inf'):
            return None
        
        return AutoCompleteData(
            completed_sentence=user_sentence,
            source_text=sentence,
            offset=offset,
            score=score
        )


# Global instance for compatibility with existing code
_score_calculator = ScoreCalculator()

# Convenience functions for compatibility
def preprocess_sentence(sentence: str) -> str:
    """Convenience function to preprocess sentences"""
    return _score_calculator.preprocess_sentence(sentence)


def calculate_scores(user_sentence: str, sentences_df) -> List[AutoCompleteData]:
    """Convenience function to calculate scores"""
    return _score_calculator.calculate_scores(user_sentence, sentences_df)


# Constants for compatibility with existing code
ERR_ADDITION = ErrorTypes.ADDITION
ERR_SUBTRACTION = ErrorTypes.DELETION
ERR_REPLACEMENT = ErrorTypes.SUBSTITUTION
