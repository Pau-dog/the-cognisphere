"""
Economic System Customizations for The Cognisphere

This file shows how to customize economic rules, resource types,
trade mechanics, and market dynamics.
"""

import random
from backend.simulation.economy import Economy, Market, Resource, Trade, ResourceType

# Example 1: Different Economic Systems
class FreeMarketEconomy(Economy):
    """Classical free market with minimal intervention."""
    
    def __init__(self):
        super().__init__()
        # Free market parameters
        self.price_volatility = 0.3          # 30% price volatility
        self.competition_factor = 0.8        # 80% competition influence
        self.government_intervention = 0.0    # 0% government intervention
        self.market_friction = 0.1           # 10% market friction
        
        # Modify resource production for free market
        self.resource_production = {
            "food": 800.0,      # Lower base production
            "energy": 600.0,    # Encourages competition
            "artifacts": 150.0, # Scarce resources
            "influence": 80.0   # Limited influence
        }

class PlannedEconomy(Economy):
    """Centralized planning with resource allocation."""
    
    def __init__(self):
        super().__init__()
        # Planned economy parameters
        self.price_volatility = 0.05         # 5% price volatility (stable)
        self.competition_factor = 0.2        # 20% competition influence
        self.government_intervention = 0.9    # 90% government intervention
        self.market_friction = 0.3           # 30% market friction
        
        # Modify resource production for planned economy
        self.resource_production = {
            "food": 1200.0,     # Higher base production
            "energy": 1000.0,   # Guaranteed supply
            "artifacts": 300.0, # Controlled production
            "influence": 200.0  # Distributed influence
        }

class MixedEconomy(Economy):
    """Hybrid system with both market and planning elements."""
    
    def __init__(self):
        super().__init__()
        # Mixed economy parameters
        self.price_volatility = 0.15         # 15% price volatility
        self.competition_factor = 0.5        # 50% competition influence
        self.government_intervention = 0.4    # 40% government intervention
        self.market_friction = 0.2           # 20% market friction
        
        # Balanced resource production
        self.resource_production = {
            "food": 1000.0,     # Moderate production
            "energy": 800.0,    # Balanced supply
            "artifacts": 200.0, # Controlled scarcity
            "influence": 120.0  # Moderate influence
        }

# Example 2: Custom Resource Types
class AdvancedResourceTypes:
    """Define new resource types for different economic scenarios."""
    
    @staticmethod
    def get_knowledge_economy_resources():
        """Resources for a knowledge-based economy."""
        return {
            "data": Resource("data", base_value=2.0, production_rate=1.2),
            "algorithms": Resource("algorithms", base_value=3.0, production_rate=0.8),
            "insights": Resource("insights", base_value=4.0, production_rate=0.6),
            "reputation": Resource("reputation", base_value=2.5, production_rate=0.4),
            "connections": Resource("connections", base_value=1.8, production_rate=1.0),
            "time": Resource("time", base_value=1.0, production_rate=1.0, decay_rate=0.1)
        }
    
    @staticmethod
    def get_creative_economy_resources():
        """Resources for a creative economy."""
        return {
            "inspiration": Resource("inspiration", base_value=2.5, production_rate=0.7),
            "skills": Resource("skills", base_value=2.0, production_rate=0.5),
            "audience": Resource("audience", base_value=3.0, production_rate=0.8),
            "platform": Resource("platform", base_value=1.5, production_rate=0.3),
            "collaboration": Resource("collaboration", base_value=2.2, production_rate=0.6),
            "originality": Resource("originality", base_value=3.5, production_rate=0.4)
        }
    
    @staticmethod
    def get_sustainability_resources():
        """Resources for a sustainable economy."""
        return {
            "renewable_energy": Resource("renewable_energy", base_value=1.5, production_rate=1.5),
            "recycled_materials": Resource("recycled_materials", base_value=1.2, production_rate=1.3),
            "biodiversity": Resource("biodiversity", base_value=2.0, production_rate=0.8),
            "carbon_credits": Resource("carbon_credits", base_value=2.5, production_rate=0.6),
            "community_trust": Resource("community_trust", base_value=1.8, production_rate=0.7),
            "innovation": Resource("innovation", base_value=3.0, production_rate=0.5)
        }

# Example 3: Custom Trade Mechanics
class AdvancedTradeMechanics:
    """Customize trade negotiation and execution."""
    
    @staticmethod
    def get_auction_based_trading():
        """Auction-based trading system."""
        return {
            "auction_duration": 5,            # 5 ticks per auction
            "bidding_rounds": 3,              # 3 rounds of bidding
            "price_increment": 0.1,           # 10% price increment
            "reserve_price_factor": 0.8,      # 80% of estimated value
            "winner_takes_all": True,         # Winner gets entire lot
            "participation_fee": 0.05         # 5% participation fee
        }
    
    @staticmethod
    def get_negotiation_based_trading():
        """Detailed negotiation trading system."""
        return {
            "max_rounds": 10,                 # 10 negotiation rounds
            "concession_rate": 0.1,           # 10% concession per round
            "bluff_probability": 0.3,         # 30% chance of bluffing
            "trust_modifier": 0.5,            # 50% influence of trust
            "patience_factor": 0.7,           # 70% influence of patience
            "walk_away_threshold": 0.2        # 20% walk-away threshold
        }
    
    @staticmethod
    def get_blockchain_trading():
        """Blockchain-based trading with smart contracts."""
        return {
            "transaction_fee": 0.02,          # 2% transaction fee
            "settlement_time": 2,             # 2 ticks settlement
            "smart_contract_enabled": True,   # Enable smart contracts
            "immutable_records": True,        # Immutable trade records
            "consensus_required": 0.6,        # 60% consensus required
            "gas_price_volatility": 0.2       # 20% gas price volatility
        }

# Example 4: Market Dynamics Customization
class MarketDynamics:
    """Customize market behavior and price dynamics."""
    
    @staticmethod
    def get_volatile_market():
        """High-volatility market with rapid price changes."""
        return {
            "price_change_rate": 0.3,         # 30% max price change per tick
            "trend_momentum": 0.8,            # 80% trend continuation
            "reversal_probability": 0.4,      # 40% chance of trend reversal
            "panic_threshold": 0.7,           # 70% price drop triggers panic
            "euphoria_threshold": 0.5,        # 50% price rise triggers euphoria
            "correlation_factor": 0.6         # 60% correlation between assets
        }
    
    @staticmethod
    def get_stable_market():
        """Low-volatility market with stable prices."""
        return {
            "price_change_rate": 0.05,        # 5% max price change per tick
            "trend_momentum": 0.3,            # 30% trend continuation
            "reversal_probability": 0.1,      # 10% chance of trend reversal
            "panic_threshold": 0.9,           # 90% price drop triggers panic
            "euphoria_threshold": 0.8,        # 80% price rise triggers euphoria
            "correlation_factor": 0.2         # 20% correlation between assets
        }
    
    @staticmethod
    def get_bubble_market():
        """Market prone to bubbles and crashes."""
        return {
            "price_change_rate": 0.4,         # 40% max price change per tick
            "trend_momentum": 0.9,            # 90% trend continuation
            "reversal_probability": 0.2,      # 20% chance of trend reversal
            "panic_threshold": 0.6,           # 60% price drop triggers panic
            "euphoria_threshold": 0.3,        # 30% price rise triggers euphoria
            "correlation_factor": 0.8,        # 80% correlation between assets
            "herd_behavior": 0.7,             # 70% herd behavior influence
            "fomo_factor": 0.6                # 60% fear of missing out
        }

# Example 5: Economic Events and Shocks
class EconomicEvents:
    """Define economic events that affect the simulation."""
    
    @staticmethod
    def get_technology_shocks():
        """Technology-related economic events."""
        return [
            {
                "name": "AI_breakthrough",
                "probability": 0.1,           # 10% chance per tick
                "duration": 20,               # 20 ticks duration
                "effects": {
                    "algorithms": 2.0,        # Double algorithm production
                    "data": 1.5,              # 50% increase in data value
                    "insights": 1.8           # 80% increase in insights
                },
                "description": "Major AI breakthrough accelerates innovation"
            },
            {
                "name": "tech_bubble_burst",
                "probability": 0.05,          # 5% chance per tick
                "duration": 15,               # 15 ticks duration
                "effects": {
                    "algorithms": 0.5,        # Half algorithm value
                    "data": 0.7,              # 30% decrease in data value
                    "reputation": 0.8         # 20% decrease in reputation
                },
                "description": "Technology bubble bursts, causing market correction"
            }
        ]
    
    @staticmethod
    def get_resource_shocks():
        """Resource-related economic events."""
        return [
            {
                "name": "energy_crisis",
                "probability": 0.08,          # 8% chance per tick
                "duration": 25,               # 25 ticks duration
                "effects": {
                    "energy": 0.4,            # 60% decrease in energy
                    "food": 0.8,              # 20% decrease in food
                    "influence": 1.2          # 20% increase in influence value
                },
                "description": "Energy crisis disrupts production chains"
            },
            {
                "name": "resource_discovery",
                "probability": 0.12,          # 12% chance per tick
                "duration": 30,               # 30 ticks duration
                "effects": {
                    "artifacts": 1.6,         # 60% increase in artifacts
                    "influence": 1.3,         # 30% increase in influence
                    "food": 1.1               # 10% increase in food
                },
                "description": "New resource deposits discovered"
            }
        ]
    
    @staticmethod
    def get_social_shocks():
        """Social and cultural economic events."""
        return [
            {
                "name": "cultural_revolution",
                "probability": 0.06,          # 6% chance per tick
                "duration": 40,               # 40 ticks duration
                "effects": {
                    "influence": 1.8,         # 80% increase in influence
                    "artifacts": 0.7,         # 30% decrease in artifacts
                    "reputation": 0.5         # 50% decrease in reputation
                },
                "description": "Cultural revolution disrupts traditional power structures"
            },
            {
                "name": "social_harmony",
                "probability": 0.15,          # 15% chance per tick
                "duration": 20,               # 20 ticks duration
                "effects": {
                    "collaboration": 1.5,     # 50% increase in collaboration
                    "community_trust": 1.4,   # 40% increase in community trust
                    "innovation": 1.2         # 20% increase in innovation
                },
                "description": "Period of social harmony boosts cooperation"
            }
        ]

# Example 6: Economic Policies
class EconomicPolicies:
    """Define economic policies that agents can implement."""
    
    @staticmethod
    def get_redistribution_policies():
        """Policies for wealth redistribution."""
        return [
            {
                "name": "progressive_taxation",
                "description": "Tax higher earners at higher rates",
                "implementation_cost": 0.1,    # 10% implementation cost
                "effectiveness": 0.7,          # 70% effectiveness
                "gini_reduction": 0.2,         # 20% reduction in Gini coefficient
                "economic_growth_impact": -0.1  # 10% reduction in growth
            },
            {
                "name": "universal_basic_income",
                "description": "Provide basic income to all agents",
                "implementation_cost": 0.3,    # 30% implementation cost
                "effectiveness": 0.8,          # 80% effectiveness
                "gini_reduction": 0.4,         # 40% reduction in Gini coefficient
                "economic_growth_impact": 0.05  # 5% increase in growth
            }
        ]
    
    @staticmethod
    def get_innovation_policies():
        """Policies to encourage innovation."""
        return [
            {
                "name": "research_subsidies",
                "description": "Subsidize research and development",
                "implementation_cost": 0.2,    # 20% implementation cost
                "innovation_boost": 0.4,       # 40% increase in innovation
                "time_to_effect": 10,          # 10 ticks to see effect
                "success_probability": 0.6     # 60% chance of success
            },
            {
                "name": "patent_protection",
                "description": "Strengthen intellectual property rights",
                "implementation_cost": 0.05,   # 5% implementation cost
                "innovation_boost": 0.3,       # 30% increase in innovation
                "time_to_effect": 5,           # 5 ticks to see effect
                "success_probability": 0.8     # 80% chance of success
            }
        ]

# Usage Examples:
if __name__ == "__main__":
    # Create different economic systems
    free_market = FreeMarketEconomy()
    planned_economy = PlannedEconomy()
    mixed_economy = MixedEconomy()
    
    print("Economic Systems:")
    print(f"Free Market - Volatility: {free_market.price_volatility}")
    print(f"Planned Economy - Government Intervention: {planned_economy.government_intervention}")
    print(f"Mixed Economy - Competition Factor: {mixed_economy.competition_factor}")
    
    # Show custom resource types
    knowledge_resources = AdvancedResourceTypes.get_knowledge_economy_resources()
    print(f"\nKnowledge Economy Resources: {len(knowledge_resources)}")
    
    # Show custom trade mechanics
    auction_trading = AdvancedTradeMechanics.get_auction_based_trading()
    print(f"Auction Trading - Rounds: {auction_trading['bidding_rounds']}")
    
    # Show market dynamics
    volatile_market = MarketDynamics.get_volatile_market()
    print(f"Volatile Market - Price Change Rate: {volatile_market['price_change_rate']}")
    
    # Show economic events
    tech_shocks = EconomicEvents.get_technology_shocks()
    print(f"Technology Shocks: {len(tech_shocks)}")
    
    # Show economic policies
    redistribution_policies = EconomicPolicies.get_redistribution_policies()
    print(f"Redistribution Policies: {len(redistribution_policies)}")
