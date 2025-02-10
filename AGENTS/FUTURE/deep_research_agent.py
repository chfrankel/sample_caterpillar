#!python3
import argparse
from agent_base import Agent_base

class Deep_Research_Agent(Agent_base):
    def __init__(self, agent_input_file):
        super().__init__(agent_input_file)
    
    def agent_name(self) -> str:
        return 'deep_research_agent'
    
    def test_results_in_simulation(self, query_results : dict[str, str]) -> None:
        pass

############ Program Entry Point ############
if __name__ == "__main__":
    print('welcome to __main__ for the deep_research_agent class')
