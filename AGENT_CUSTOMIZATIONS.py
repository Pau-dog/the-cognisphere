"""
Agent Personality Customizations for The Cognisphere

This file shows practical examples of how to customize agent personalities
to create different types of agents with distinct behaviors.
"""

import random
from backend.simulation.agents import AgentPersonality

# Example 1: Create Specialized Agent Types
class SpecializedPersonalities:
    """Predefined personality types for different agent roles."""
    
    @staticmethod
    def create_entrepreneur() -> AgentPersonality:
        """High-risk, high-reward agents who drive innovation."""
        return AgentPersonality(
            openness=0.9,        # Very creative and curious
            conscientiousness=0.7,  # Organized and goal-oriented
            extraversion=0.8,    # Social and outgoing
            agreeableness=0.4,   # Competitive, not always cooperative
            neuroticism=0.3      # Low anxiety, confident
        )
    
    @staticmethod
    def create_philosopher() -> AgentPersonality:
        """Deep thinkers who create complex myths and theories."""
        return AgentPersonality(
            openness=0.95,       # Extremely creative
            conscientiousness=0.6,  # Moderately organized
            extraversion=0.2,    # Introverted, prefers reflection
            agreeableness=0.8,   # Cooperative and empathetic
            neuroticism=0.4      # Thoughtful, not anxious
        )
    
    @staticmethod
    def create_leader() -> AgentPersonality:
        """Natural leaders who form alliances and institutions."""
        return AgentPersonality(
            openness=0.6,        # Moderately creative
            conscientiousness=0.9,  # Highly organized
            extraversion=0.95,   # Very outgoing
            agreeableness=0.8,   # Cooperative and trustworthy
            neuroticism=0.2      # Confident and stable
        )
    
    @staticmethod
    def create_merchant() -> AgentPersonality:
        """Trade-focused agents who optimize economic exchanges."""
        return AgentPersonality(
            openness=0.5,        # Moderate creativity
            conscientiousness=0.8,  # Very organized
            extraversion=0.7,    # Social for networking
            agreeableness=0.6,   # Balanced cooperation
            neuroticism=0.3      # Low anxiety, confident
        )
    
    @staticmethod
    def create_artist() -> AgentPersonality:
        """Creative agents who generate cultural content."""
        return AgentPersonality(
            openness=0.95,       # Extremely creative
            conscientiousness=0.4,  # Less organized
            extraversion=0.6,    # Moderately social
            agreeableness=0.7,   # Cooperative
            neuroticism=0.5      # Emotionally expressive
        )

# Example 2: Biased Random Generation
def generate_biased_personality(bias_type: str = "balanced") -> AgentPersonality:
    """Generate personalities with specific biases."""
    
    if bias_type == "creative":
        # Favor high openness and extraversion
        return AgentPersonality(
            openness=random.uniform(0.7, 1.0),
            conscientiousness=random.uniform(0.3, 0.8),
            extraversion=random.uniform(0.6, 1.0),
            agreeableness=random.uniform(0.4, 0.9),
            neuroticism=random.uniform(0.2, 0.6)
        )
    
    elif bias_type == "cooperative":
        # Favor high agreeableness and conscientiousness
        return AgentPersonality(
            openness=random.uniform(0.4, 0.8),
            conscientiousness=random.uniform(0.6, 1.0),
            extraversion=random.uniform(0.4, 0.9),
            agreeableness=random.uniform(0.7, 1.0),
            neuroticism=random.uniform(0.2, 0.5)
        )
    
    elif bias_type == "competitive":
        # Favor lower agreeableness, higher extraversion
        return AgentPersonality(
            openness=random.uniform(0.5, 0.9),
            conscientiousness=random.uniform(0.6, 1.0),
            extraversion=random.uniform(0.7, 1.0),
            agreeableness=random.uniform(0.2, 0.6),
            neuroticism=random.uniform(0.3, 0.7)
        )
    
    elif bias_type == "analytical":
        # Favor high conscientiousness, lower extraversion
        return AgentPersonality(
            openness=random.uniform(0.6, 0.9),
            conscientiousness=random.uniform(0.8, 1.0),
            extraversion=random.uniform(0.2, 0.6),
            agreeableness=random.uniform(0.5, 0.8),
            neuroticism=random.uniform(0.2, 0.5)
        )
    
    else:  # balanced
        return AgentPersonality.random()

# Example 3: Personality Clusters
def create_personality_clusters(num_agents: int, cluster_types: list = None) -> list:
    """Create groups of agents with similar personalities."""
    
    if cluster_types is None:
        cluster_types = ["entrepreneur", "philosopher", "leader", "merchant", "artist"]
    
    personalities = []
    
    for i in range(num_agents):
        # Assign cluster type
        cluster_type = cluster_types[i % len(cluster_types)]
        
        if cluster_type == "entrepreneur":
            base_personality = SpecializedPersonalities.create_entrepreneur()
        elif cluster_type == "philosopher":
            base_personality = SpecializedPersonalities.create_philosopher()
        elif cluster_type == "leader":
            base_personality = SpecializedPersonalities.create_leader()
        elif cluster_type == "merchant":
            base_personality = SpecializedPersonalities.create_merchant()
        elif cluster_type == "artist":
            base_personality = SpecializedPersonalities.create_artist()
        else:
            base_personality = AgentPersonality.random()
        
        # Add some variation within the cluster
        variation = 0.1  # 10% variation
        varied_personality = AgentPersonality(
            openness=max(0.0, min(1.0, base_personality.openness + random.uniform(-variation, variation))),
            conscientiousness=max(0.0, min(1.0, base_personality.conscientiousness + random.uniform(-variation, variation))),
            extraversion=max(0.0, min(1.0, base_personality.extraversion + random.uniform(-variation, variation))),
            agreeableness=max(0.0, min(1.0, base_personality.agreeableness + random.uniform(-variation, variation))),
            neuroticism=max(0.0, min(1.0, base_personality.neuroticism + random.uniform(-variation, variation)))
        )
        
        personalities.append(varied_personality)
    
    return personalities

# Example 4: Dynamic Personality Evolution
class PersonalityEvolution:
    """Allow agent personalities to evolve based on experiences."""
    
    @staticmethod
    def adapt_to_success(personality: AgentPersonality, success_type: str) -> AgentPersonality:
        """Modify personality based on successful interactions."""
        
        adaptation_rate = 0.05  # 5% change per success
        
        if success_type == "trade":
            # Successful traders become more conscientious and less neurotic
            return AgentPersonality(
                openness=personality.openness,
                conscientiousness=min(1.0, personality.conscientiousness + adaptation_rate),
                extraversion=personality.extraversion,
                agreeableness=personality.agreeableness,
                neuroticism=max(0.0, personality.neuroticism - adaptation_rate)
            )
        
        elif success_type == "social":
            # Successful social interactions increase extraversion and agreeableness
            return AgentPersonality(
                openness=personality.openness,
                conscientiousness=personality.conscientiousness,
                extraversion=min(1.0, personality.extraversion + adaptation_rate),
                agreeableness=min(1.0, personality.agreeableness + adaptation_rate),
                neuroticism=personality.neuroticism
            )
        
        elif success_type == "creative":
            # Successful creativity increases openness
            return AgentPersonality(
                openness=min(1.0, personality.openness + adaptation_rate),
                conscientiousness=personality.conscientiousness,
                extraversion=personality.extraversion,
                agreeableness=personality.agreeableness,
                neuroticism=personality.neuroticism
            )
        
        return personality
    
    @staticmethod
    def adapt_to_failure(personality: AgentPersonality, failure_type: str) -> AgentPersonality:
        """Modify personality based on failed interactions."""
        
        adaptation_rate = 0.03  # 3% change per failure (smaller than success)
        
        if failure_type == "betrayal":
            # Betrayal decreases agreeableness and increases neuroticism
            return AgentPersonality(
                openness=personality.openness,
                conscientiousness=personality.conscientiousness,
                extraversion=personality.extraversion,
                agreeableness=max(0.0, personality.agreeableness - adaptation_rate),
                neuroticism=min(1.0, personality.neuroticism + adaptation_rate)
            )
        
        elif failure_type == "isolation":
            # Isolation decreases extraversion
            return AgentPersonality(
                openness=personality.openness,
                conscientiousness=personality.conscientiousness,
                extraversion=max(0.0, personality.extraversion - adaptation_rate),
                agreeableness=personality.agreeableness,
                neuroticism=personality.neuroticism
            )
        
        return personality

# Example 5: Personality-Based Behavior Modifiers
class BehaviorModifiers:
    """Use personality to modify agent behavior probabilities."""
    
    @staticmethod
    def get_trade_probability(personality: AgentPersonality) -> float:
        """Higher conscientiousness and extraversion = more likely to trade."""
        base_prob = 0.3
        conscientiousness_bonus = personality.conscientiousness * 0.2
        extraversion_bonus = personality.extraversion * 0.15
        agreeableness_penalty = (1.0 - personality.agreeableness) * 0.1
        
        return min(0.8, base_prob + conscientiousness_bonus + extraversion_bonus - agreeableness_penalty)
    
    @staticmethod
    def get_myth_creation_probability(personality: AgentPersonality) -> float:
        """Higher openness = more likely to create myths."""
        base_prob = 0.1
        openness_bonus = personality.openness * 0.3
        neuroticism_bonus = personality.neuroticism * 0.1  # Emotional expression
        
        return min(0.6, base_prob + openness_bonus + neuroticism_bonus)
    
    @staticmethod
    def get_alliance_probability(personality: AgentPersonality) -> float:
        """Higher agreeableness and extraversion = more likely to form alliances."""
        base_prob = 0.2
        agreeableness_bonus = personality.agreeableness * 0.25
        extraversion_bonus = personality.extraversion * 0.2
        neuroticism_penalty = personality.neuroticism * 0.1
        
        return min(0.7, base_prob + agreeableness_bonus + extraversion_bonus - neuroticism_penalty)
    
    @staticmethod
    def get_innovation_probability(personality: AgentPersonality) -> float:
        """Higher openness and conscientiousness = more likely to innovate."""
        base_prob = 0.05
        openness_bonus = personality.openness * 0.4
        conscientiousness_bonus = personality.conscientiousness * 0.15
        
        return min(0.5, base_prob + openness_bonus + conscientiousness_bonus)

# Usage Examples:
if __name__ == "__main__":
    # Create a diverse population
    personalities = create_personality_clusters(20, ["entrepreneur", "philosopher", "leader", "merchant", "artist"])
    
    # Show behavior probabilities for each type
    for i, personality in enumerate(personalities[:5]):
        print(f"Agent {i+1}:")
        print(f"  Trade Probability: {BehaviorModifiers.get_trade_probability(personality):.2f}")
        print(f"  Myth Creation: {BehaviorModifiers.get_myth_creation_probability(personality):.2f}")
        print(f"  Alliance Formation: {BehaviorModifiers.get_alliance_probability(personality):.2f}")
        print(f"  Innovation: {BehaviorModifiers.get_innovation_probability(personality):.2f}")
        print()
