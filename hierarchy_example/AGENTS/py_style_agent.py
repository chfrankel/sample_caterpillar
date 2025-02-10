#!python3
from agent_base import Agent_base

########################## STRING CONSTANTS ##########################

#####
# CONSTANT: PROGRAMMING_TASK
#####
PROGRAMMING_TASK = f'''Refactor the following Python program following the style of '''
ACCURACY_VALIDATION = f'''the resultant sum of all prime numbers up to 10,000,000''' # is 37550402023'''

#####
# CONSTANT: INITIAL_QUERY
#####
INITIAL_QUERY = f'''
Write a complete, fully functional, and properly formatted python program to accomplish the following PROGRAMGING TASK:

PROGRAMGING TASK:
{PROGRAMMING_TASK}

print out only the execution time of the script, and the accuracy validation : {ACCURACY_VALIDATION}
format the time to 3 decimal places in the format 0.123 seconds
format the accuracy validation as a single **number**, defined as {ACCURACY_VALIDATION}, for instance 1,234,567 - note commas separating the thousands places
The final output should be in this format: '[Execution time: 0.123 seconds, accuracy validation]']
'''

#####
# CONSTANT: ITERATIVE_QUERIES
#####
ITERATIVE_QUERIES = '''
I asked this query:
"{initial_query}"

I want you to examine the program you wrote, and write a new program that is faster than the one you initially wrote
Your program's exucution time: {execution_time}
Your prorgam's output: {this_program}

Here are is a list of programs that accomplished the same task, the format is execution time, followed by the program. 
Use these programs to learn a better way to solve the problem.
{other_programs}
'''

#####
# CONSTANT: ITERATIVE_QUERIES
#####
FINAL_QUERY = f'''
Given your last several attempts to write accomplish this programming task:

PROGRAMMING_TASK: {PROGRAMMING_TASK}

summarize what you learned about writing the fastest program to accomlish the task.
Output adivce including a summary and list of tips, ordered from most important advice to least important for instance:

SUMMARY: overview of what was learned

TIPS:
1) Most important advice
2) second most important advice
3) third most important advice
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