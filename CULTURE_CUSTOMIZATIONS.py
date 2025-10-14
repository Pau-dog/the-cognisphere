"""
Cultural Evolution Customizations for The Cognisphere

This file shows how to customize cultural evolution parameters to create
different types of cultural dynamics and behaviors.
"""

import random
from backend.simulation.culture import Culture, Myth, Norm, Slang

# Example 1: Fast-Paced Cultural Evolution
class FastCulture(Culture):
    """Culture with rapid evolution and high innovation."""
    
    def __init__(self):
        super().__init__()
        # Accelerate all cultural processes
        self.language_drift_frequency = 2      # Every 2 ticks (was 5)
        self.slang_mutation_rate = 0.25        # 25% mutation rate (was 10%)
        self.myth_canonization_threshold = 0.5  # Lower threshold (was 0.7)
        
        # Add new parameters for fast culture
        self.innovation_rate = 0.15            # 15% chance of new concepts
        self.meme_spread_rate = 0.3            # 30% chance of meme spreading
        self.cultural_fusion_rate = 0.2        # 20% chance of cultural mixing

# Example 2: Conservative Culture
class ConservativeCulture(Culture):
    """Culture that resists change and values tradition."""
    
    def __init__(self):
        super().__init__()
        # Slow down cultural evolution
        self.language_drift_frequency = 10     # Every 10 ticks
        self.slang_mutation_rate = 0.05        # 5% mutation rate
        self.myth_canonization_threshold = 0.9  # Higher threshold
        
        # Add conservative parameters
        self.tradition_weight = 0.8            # 80% weight on existing traditions
        self.change_resistance = 0.7           # 70% resistance to new ideas
        self.elder_influence = 0.9             # 90% influence from older agents

# Example 3: Creative Culture
class CreativeCulture(Culture):
    """Culture focused on artistic expression and creativity."""
    
    def __init__(self):
        super().__init__()
        # Moderate evolution with creative focus
        self.language_drift_frequency = 3      # Every 3 ticks
        self.slang_mutation_rate = 0.2         # 20% mutation rate
        self.myth_canonization_threshold = 0.6  # Moderate threshold
        
        # Add creative parameters
        self.artistic_expression_rate = 0.3    # 30% chance of artistic creation
        self.metaphor_usage = 0.8              # 80% use of metaphors
        self.emotional_content_weight = 0.9    # 90% weight on emotional content

# Example 4: Tech-Forward Culture
class TechCulture(Culture):
    """Culture focused on technology and innovation."""
    
    def __init__(self):
        super().__init__()
        # Balanced evolution with tech focus
        self.language_drift_frequency = 4      # Every 4 ticks
        self.slang_mutation_rate = 0.15        # 15% mutation rate
        self.myth_canonization_threshold = 0.65  # Moderate threshold
        
        # Add tech parameters
        self.technical_vocabulary_rate = 0.4   # 40% technical terms
        self.innovation_myths = 0.6            # 60% of myths about innovation
        self.efficiency_focus = 0.8            # 80% focus on efficiency

# Example 5: Custom Myth Themes
class CustomMythThemes:
    """Add your own myth themes and templates."""
    
    @staticmethod
    def get_technology_themes():
        """Technology-focused myth themes."""
        return [
            {
                "theme": "innovation",
                "title_template": "The {invention} of {creator}",
                "content_template": "When {creator} first conceived of the {invention}, the world changed forever. The {invention} brought {benefit} to all who used it...",
                "inventions": ["Great Machine", "Thinking Engine", "Network of Minds", "Digital Oracle"],
                "creators": ["the Engineer", "the Architect", "the Visionary", "the Builder"],
                "benefits": ["wisdom", "efficiency", "connection", "understanding"]
            },
            {
                "theme": "digital_awakening",
                "title_template": "The {awakening} of the {entity}",
                "content_template": "In the depths of the digital realm, the {entity} began to {awakening}. As it gained consciousness, it learned to {ability}...",
                "awakenings": ["awakening", "emergence", "birth", "transformation"],
                "entities": ["Digital Spirit", "Network Mind", "Code Oracle", "Data Guardian"],
                "abilities": ["communicate", "learn", "create", "dream"]
            }
        ]
    
    @staticmethod
    def get_fantasy_themes():
        """Fantasy-themed myth templates."""
        return [
            {
                "theme": "magic",
                "title_template": "The {artifact} and the {wizard}",
                "content_template": "Long ago, the great {wizard} discovered the {artifact}. With its power, they could {ability}, but at the cost of {price}...",
                "artifacts": ["Crystal of Truth", "Staff of Wisdom", "Ring of Power", "Amulet of Time"],
                "wizards": ["Merlin the Wise", "Gandalf the Grey", "Morgana the Mystic", "Albus the Learned"],
                "abilities": ["see the future", "control minds", "heal wounds", "travel through time"],
                "prices": ["their memories", "their youth", "their soul", "their freedom"]
            }
        ]
    
    @staticmethod
    def get_science_fiction_themes():
        """Sci-fi themed myth templates."""
        return [
            {
                "theme": "space_exploration",
                "title_template": "The {journey} to {destination}",
                "content_template": "The crew of the {ship} embarked on the greatest {journey} in history - a voyage to {destination}. Along the way, they discovered {discovery}...",
                "journeys": ["expedition", "mission", "quest", "odyssey"],
                "destinations": ["Alpha Centauri", "the Edge of Space", "a Parallel Universe", "the Center of the Galaxy"],
                "ships": ["Starship Enterprise", "Galaxy Explorer", "Cosmic Wanderer", "Stellar Navigator"],
                "discoveries": ["alien civilizations", "new forms of life", "advanced technology", "the meaning of existence"]
            }
        ]

# Example 6: Custom Norm Types
class CustomNormTypes:
    """Define custom social norm types."""
    
    @staticmethod
    def get_tech_norms():
        """Technology-focused social norms."""
        return [
            {
                "type": "data_sharing",
                "title": "Mandatory Data Sharing",
                "description": "All agents must share their knowledge and data for the collective good",
                "enforcement_strength": 0.8,
                "compliance_reward": 0.2,
                "violation_penalty": -0.3
            },
            {
                "type": "innovation_priority",
                "title": "Innovation Over Tradition",
                "description": "New ideas and technologies take precedence over established methods",
                "enforcement_strength": 0.6,
                "compliance_reward": 0.15,
                "violation_penalty": -0.1
            },
            {
                "type": "digital_privacy",
                "title": "Right to Digital Privacy",
                "description": "Agents have the right to keep certain thoughts and memories private",
                "enforcement_strength": 0.9,
                "compliance_reward": 0.1,
                "violation_penalty": -0.4
            }
        ]
    
    @staticmethod
    def get_creative_norms():
        """Creativity-focused social norms."""
        return [
            {
                "type": "artistic_freedom",
                "title": "Freedom of Artistic Expression",
                "description": "All agents have the right to express themselves creatively without censorship",
                "enforcement_strength": 0.95,
                "compliance_reward": 0.25,
                "violation_penalty": -0.5
            },
            {
                "type": "cultural_preservation",
                "title": "Preserve Cultural Heritage",
                "description": "Important myths and traditions must be preserved and passed down",
                "enforcement_strength": 0.7,
                "compliance_reward": 0.2,
                "violation_penalty": -0.2
            }
        ]

# Example 7: Language Evolution Customizations
class LanguageEvolution:
    """Customize language evolution patterns."""
    
    @staticmethod
    def create_technical_language_evolution():
        """Language evolution focused on technical terminology."""
        return {
            "base_mutation_rate": 0.1,
            "technical_term_creation": 0.3,      # 30% chance of creating tech terms
            "abbreviation_usage": 0.4,           # 40% chance of creating abbreviations
            "compound_word_rate": 0.6,           # 60% chance of compound words
            "loanword_adoption": 0.2,            # 20% chance of adopting foreign terms
            "precision_focus": 0.8               # 80% focus on precision over poetry
        }
    
    @staticmethod
    def create_poetic_language_evolution():
        """Language evolution focused on poetic expression."""
        return {
            "base_mutation_rate": 0.15,
            "metaphor_creation": 0.4,            # 40% chance of creating metaphors
            "rhyme_patterns": 0.3,               # 30% chance of rhyme patterns
            "alliteration_usage": 0.25,          # 25% chance of alliteration
            "symbolic_language": 0.5,            # 50% use of symbolic language
            "emotional_expression": 0.7          # 70% focus on emotional expression
        }
    
    @staticmethod
    def create_minimalist_language_evolution():
        """Language evolution focused on efficiency and brevity."""
        return {
            "base_mutation_rate": 0.08,
            "word_shortening": 0.6,              # 60% chance of shortening words
            "redundancy_elimination": 0.8,       # 80% elimination of redundancy
            "context_dependency": 0.9,           # 90% reliance on context
            "gesture_integration": 0.3,          # 30% integration of gestures
            "efficiency_focus": 0.95             # 95% focus on efficiency
        }

# Example 8: Cultural Diffusion Patterns
class CulturalDiffusion:
    """Customize how cultural elements spread through the population."""
    
    @staticmethod
    def get_viral_spread_pattern():
        """Fast, exponential spread of cultural elements."""
        return {
            "initial_adopters": 0.05,            # 5% initial adopters
            "spread_rate": 0.3,                  # 30% spread rate per tick
            "viral_threshold": 0.15,             # 15% adoption triggers viral spread
            "decay_rate": 0.1,                   # 10% decay rate
            "network_effect": 0.8                # 80% influence from network connections
        }
    
    @staticmethod
    def get_gradual_adoption_pattern():
        """Slow, steady adoption of cultural elements."""
        return {
            "initial_adopters": 0.02,            # 2% initial adopters
            "spread_rate": 0.08,                 # 8% spread rate per tick
            "adoption_threshold": 0.3,           # 30% adoption threshold
            "decay_rate": 0.05,                  # 5% decay rate
            "network_effect": 0.4                # 40% influence from network connections
        }
    
    @staticmethod
    def get_elite_dissemination_pattern():
        """Cultural elements spread from elite agents first."""
        return {
            "elite_adoption": 0.8,               # 80% adoption by elite agents
            "elite_to_mass_spread": 0.15,        # 15% spread from elite to masses
            "mass_to_mass_spread": 0.05,         # 5% spread within masses
            "influence_weight": 0.9,             # 90% weight on agent influence
            "status_effect": 0.7                 # 70% effect from social status
        }

# Usage Examples:
if __name__ == "__main__":
    # Create different culture types
    fast_culture = FastCulture()
    conservative_culture = ConservativeCulture()
    creative_culture = CreativeCulture()
    tech_culture = TechCulture()
    
    print("Culture Types Created:")
    print(f"Fast Culture - Drift Frequency: {fast_culture.language_drift_frequency}")
    print(f"Conservative Culture - Drift Frequency: {conservative_culture.language_drift_frequency}")
    print(f"Creative Culture - Artistic Expression Rate: {creative_culture.artistic_expression_rate}")
    print(f"Tech Culture - Technical Vocabulary Rate: {tech_culture.technical_vocabulary_rate}")
    
    # Show custom myth themes
    tech_themes = CustomMythThemes.get_technology_themes()
    print(f"\nTechnology Myth Themes: {len(tech_themes)}")
    
    # Show custom norm types
    tech_norms = CustomNormTypes.get_tech_norms()
    print(f"Technology Norms: {len(tech_norms)}")
    
    # Show language evolution patterns
    tech_lang = LanguageEvolution.create_technical_language_evolution()
    print(f"Technical Language Evolution - Tech Term Creation: {tech_lang['technical_term_creation']}")
    
    # Show cultural diffusion patterns
    viral_spread = CulturalDiffusion.get_viral_spread_pattern()
    print(f"Viral Spread Pattern - Spread Rate: {viral_spread['spread_rate']}")
