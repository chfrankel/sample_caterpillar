#!python3
from agent_base import Agent_base

########################## STRING CONSTANTS ##########################

# © 2025 Charles Frankel. All rights reserved.

#####
# CONSTANT: PROGRAMMING_TASK
#####
PROGRAMMING_TASK = f'''xxx '''
ACCURACY_VALIDATION = f'''yyyy'''

#####
# CONSTANT: INITIAL_QUERY
#####
INITIAL_QUERY = f'''
zzzz'''

#####
# CONSTANT: ITERATIVE_QUERIES
#####
ITERATIVE_QUERIES = '''
aaaaa
'''

#####
# CONSTANT: ITERATIVE_QUERIES
#####
FINAL_QUERY = f'''
bbbbb
'''

#####
# CLASS: Py_Dev_Agent
#####
class Py_Style_Agent(Agent_base):

    #####
    # METHOD: __init__
    #####
    def __init__(self, input_catalog = None, output_catalog = None):
        super().__init__(input_catalog = input_catalog, output_catalog = output_catalog)
    
    ########################## accessor methods ##########################

    #####
    # METHOD: agent_name
    #####
    def agent_name(self) -> str:
        return 'py_style_agent'
    
    #####
    # METHOD: get_query
    #####
    def get_query(self, stage : str) -> str:
        match stage:
            case 'initial_query':
                return INITIAL_QUERY
            case 'iteration_query':
                return ITERATIVE_QUERIES
            case 'final_query':
                return FINAL_QUERY
            case _:
                raise ValueError(f"Py_Style_Agent:get_query --- Unknown stage: {stage}")
    
    ########################## public methods ##########################

    #####
    # METHOD: build_iterative_queries
    #####
    def build_iterative_queries(self, results):
        iterative_query = self.get_query('iteration_query')
        query_list = []
        for current_model, result in results.items():
            execution_time, program = result

            program = f"```python\n{program}```\n"
            other_results = [[result[0], result[1]] for model, result in results.items() if model != current_model]
            query_list.append(iterative_query.format(initial_query= self.get_query('initial_query'), execution_time=execution_time, this_program=program, other_programs=other_results))
        return query_list
    
    #####
    # METHOD: test_results_in_simulation
    #####
    def test_results_in_simulation(self, full_query_results, iteration) -> dict[str, str]:

        # returns {query_model: [program_file, program]}
        program_dict = self.write_program_files_to_disk(full_query_results, iteration)
        
        simulation_results = {}
        for query_model, (program_file, program) in program_dict.items():

            # run the simulation
            output = self._run_python_program(program_file)
            simulation_results[query_model] = [output, program]
            print(f"{query_model}: {output}")

        return simulation_results

############ Program Entry Point ############

if __name__ == "__main__":

    print('welcome to __main__ for the py_style_agent class')
