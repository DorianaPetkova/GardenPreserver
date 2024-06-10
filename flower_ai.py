import os
import re

class FlowerAI:
    def __init__(self, flower_info_file):
        self.flower_info = self.load_flower_info(flower_info_file)
        self.patterns = {
            'overall': re.compile(r'\boverall\b', re.IGNORECASE),
            'water': re.compile(r'\bwater\b', re.IGNORECASE),
            'soil': re.compile(r'\bsoil\b', re.IGNORECASE),
            'light': re.compile(r'\blight\b', re.IGNORECASE)
        }
        self.debug_flower_info()

    def load_flower_info(self, file):
        flower_info = {}
        current_flower = None
        with open(file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):  # Ignore empty lines and comments
                if line.endswith(':'):
                    current_flower = line[:-1].lower()
                    flower_info[current_flower] = {}
                elif current_flower:
                    category, info = map(str.strip, line.split(':', 1))
                    flower_info[current_flower][category.lower()] = info

        return flower_info

    def classify_intent(self, query):
        for intent, pattern in self.patterns.items():
            if pattern.search(query):
                return intent
        return 'unknown'

    def extract_flower(self, query):
        for flower in self.flower_info.keys():
            if flower in query.lower():
                return flower
        return None

    def extract_section_info(self, section, flower):
        print(f"Extracting information for section: {section} and flower: {flower}")  # Debug statement
        # Check if the flower exists in the flower info
        if flower in self.flower_info:
            # Check if the section exists for the flower
            if section in self.flower_info[flower]:
                print(f"Found information for {section} in {flower}")  # Debug statement
                return self.flower_info[flower][section]
            else:
                print(f"Information for {section} not found in {flower}")  # Debug statement
                return f"Sorry, I don't have information on {section} for {flower}."
        else:
            print(f"No information found for flower: {flower}")  # Debug statement
            return f"I'm sorry, I couldn't find any information about {flower}."

    def generate_response(self, query):
        print(f"Received query: {query}")  # Debug statement
        intent = self.classify_intent(query)
        print(f"Identified intent: {intent}")  # Debug statement
        if intent == 'unknown':
            return "I'm sorry, I'm not sure how to respond to that."
        
        flower = self.extract_flower(query)
        print(f"Identified flower: {flower}")  # Debug statement
        if not flower:
            return "I'm sorry, I couldn't identify the flower in your question."

        return self.extract_section_info(intent, flower)

    def debug_flower_info(self):
        print("Loaded flower information:")
        for flower, details in self.flower_info.items():
            print(f"{flower}:")
            for category, info in details.items():
                print(f"  {category}: {info}")