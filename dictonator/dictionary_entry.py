class DictionaryEntry:
    def __init__(self, 
                 word: str, 
                 base_word: str, 
                 definition: str, 
                 word_type: str, 
                 pronunciation: str, 
                 example: str, 
                 etymology: str, 
                 synonyms: list, 
                 antonyms: list, 
                 usage_notes: str, 
                 frequency: str, 
                 language: str,
                 requested_language: str,
                 prompt: str):
        """
        Initializes a new DictionaryEntry object.
        
        :param word: The term being defined.
        :param definition: A clear and concise explanation of the word’s meaning.
        :param word_type: The part of speech (e.g. noun, verb, adjective, adverb).
        :param pronunciation: A guide on how to pronounce the word, usually using phonetic notation.
        :param example: A sentence or phrase demonstrating how the word is used in context.
        :param etymology: The origin and history of the word, detailing its evolution in form and meaning over time.
        :param synonyms: A list of words that have similar meanings.
        :param antonyms: A list of words that have opposite meanings, if applicable.
        :param usage_notes: Any additional information on how the word is used, including any grammatical notes or common collocations.
        :param frequency: Information on how common a word is.
        :param language: The language to which the word belongs.
        :param requested_language: The language to which the word was requested in.
        :param situation: The prompt for generating this word.
        """
        self.word = word
        self.base_word = base_word
        self.definition = definition
        self.word_type = word_type
        self.pronunciation = pronunciation
        self.example = example
        self.etymology = etymology
        self.synonyms = synonyms
        self.antonyms = antonyms
        self.usage_notes = usage_notes
        self.frequency = frequency
        self.language = language
        self.requested_language = requested_language
        self.prompt= prompt
        
    def __str__(self):
        """
        Returns a string representation of the DictionaryEntry object.
        """
        return f"{self.word} ({self.language}, {self.word_type})\nDefinition: {self.definition}\nPronunciation: {self.pronunciation}\nExample: {self.example}\nEtymology: {self.etymology}\nSynonyms: {', '.join(self.synonyms) if self.synonyms else 'None'}\nAntonyms: {', '.join(self.antonyms) if self.antonyms else 'None'}\nUsage Notes: {self.usage_notes}\nFrequency: {self.frequency}"

# Example usage:
# entry = DictionaryEntry(word='Lexicographer', 
#                         definition='A person who compiles dictionaries.', 
#                         word_type='Noun', 
#                         pronunciation='/ˌleksɪˈkɒɡrəfə(r)/', 
#                         example='The lexicographer spent years compiling definitions for the new dictionary.', 
#                         etymology='Mid 17th century: from Greek lexikon (see lexicon) + -grapher.', 
#                         synonyms=['lexicologist', 'wordsmith'], 
#                         antonyms=[], 
#                         usage_notes='Often used to refer to professional dictionary compilers.', 
#                         frequency='Rare', 
#                         language='English')
# 
# print(entry)
