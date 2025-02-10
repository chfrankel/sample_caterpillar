#!python3
import argparse
from agent_base import Agent_base

class Molecular_Dynamics_Agent(Agent_base):
    def __init__(self, agent_input_file):
        super().__init__(agent_input_file)
    
    def agent_name(self) -> str:
        return 'molecular_dynamics_agent'
    
    def test_results_in_simulation(self, query_results : dict[str, str]) -> None:
        pass
    

############ Program Entry Point ############
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Molecular Dynamics Agent")
    args = parser.parse_args()

    args.input = "py_dev_agent.json"
    a = Molecular_Dynamics_Agent(args.input)

    a.create_queries(['''
write a complete python program to generate a histogram of three letter sequences in pdf files named DATA/sfl_hamlet.pdf, DATA/sfl_hamlet.pdf and DATA/sfl_hamlet.pdf
calculate the top 1,000 most frequent sequences for each file.
print out only the execution time of the script
                      '''])
    results = a.execute_queries()
    program = a.find_program_in_result(results)
    a.test_results_in_simulation(program)