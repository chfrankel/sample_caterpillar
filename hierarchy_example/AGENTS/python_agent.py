#!python3
from agent_base import Agent_base
import json
import subprocess

SCRIPT_LOCATION = 'OUTPUT_DIRECTORIES/PYTHON_SCRIPTS'

#####
# CLASS: Py_Dev_Agent
#####
class Python_Agent(Agent_base):

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
        return 'python_agent'

    ########################## protected methods ##########################
    #####
    # METHOD: _write_program_files_to_disk
    #####
    def _write_program_files_to_disk(self, full_query_results, iteration) -> dict[str, list[str, str]]:

        program_query_results : dict[str, str] = self.__find_programs_in_results(full_query_results)

        program_dict : dict[str, list[str, str]] = {}
        for query_model, program in program_query_results.items():

            program_filename = f'{SCRIPT_LOCATION}/{query_model}_program_{iteration}.py'
            # write the output program to disk, so it can be run
            with open(program_filename, 'w') as f:
                for l in program:
                    f.write(f'{l}\n')
            program_dict[query_model] = [program_filename, program]
        return program_dict
    
     #####
    # METHOD: _run_python_program
    #####
    def _run_python_program(self, program_file) -> str:

        command_list : list[str] = ['python3', program_file]
        result : subprocess.CompletedProcess = subprocess.run(command_list, capture_output=True, text=True)
        return result.stdout

    #####
    # METHOD: _lint_python_program
    #####
    def _lint_python_program(self, program_file) -> str:

        command_list : list[str] = ['pylint', program_file]
        result : subprocess.CompletedProcess = subprocess.run(command_list, capture_output=True, text=True)
        return result.stdout

    ########################## private methods ##########################

    #####
    # METHOD: __find_programs_in_results
    #####
    def __find_programs_in_results(self, results) -> dict[str, str]:

        json_results = json.loads(results)
        individual_results = json_results['all_results']

        program_results: dict[str, str] = {}

        for one_result in individual_results:
            parsed_query = self.parse_query_string(one_result['query'])
            program = []
            found_program = False
            for l in one_result['message'].split('\n'):
                if l.startswith("```python"):
                    found_program = True
                elif l.startswith("```"):
                    found_program = False
                    program_results[parsed_query['model']] = program
                elif found_program:
                    program.append(l)

        return program_results
    
    ########################## public methods ##########################
    
    #####
    # METHOD: test_results_in_simulation
    #####
    def test_results_in_simulation(self, full_query_results, iteration) -> dict[str, str]:

        assert(0, "Py_Style_Agent:test_results_in_simulation --- Not implemented")
        pass