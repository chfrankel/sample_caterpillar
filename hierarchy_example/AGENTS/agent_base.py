#!python3
from abc import ABC, abstractmethod
import json
import shlex
import subprocess

########################## DIRECTORIES ##########################
DEFAULT_CATALOG_LOCATION = 'OUTPUT_DIRECTORIES/CATALOG'
INPUT_QUERIES_DIR        = 'OUTPUT_DIRECTORIES/INPUT_QUERIES'
LEARNED_RESULTS_FILE     = 'learned_results.txt'

class Agent_base(ABC):
    #####
    # METHOD: __init__
    # parameter notes - the cli requires a catalog - using a dummy value unless one is provided
    #####
    def __init__(self, input_catalog = DEFAULT_CATALOG_LOCATION, output_catalog = DEFAULT_CATALOG_LOCATION):

        self.input_catalog  = input_catalog
        self.output_catalog = output_catalog
        self.agent_input_file = None
        
        # Define the base data structure
        self.query_struct = {
            "parallel-tasks": True,
            "print-summary":  True,
            "print-output":   False,
            "json-output":    True,
            "tests": []
        }

    ########################## private methods ##########################

    #####
    # METHOD: __add_query
    #####
    def __add_query(self, query, model="hybrid", provider = "company_provider") -> None:
        if "one_company_provider" in model:
            provider = "company.com"
        query = {
            "program": "program_here",
            "provider": provider,
            "model" : model,
            "catalog": self.input_catalog,
            # "crawl-depth": 1,
            "query": query
        }
        self.query_struct["tests"].append(query)

    ########################## public methods ##########################

    #####
    # METHOD: parse_query_string
    #####
    def parse_query_string(self, query_string : str) -> dict[str, str]:

        # Split the command into parts
        command = query_string.split("query: ", 1)[-1]
        command_parts = shlex.split(command)

        # Initialize dictionary to store parsed parameters
        my_query = {}

        # Iterate through parts to convert options and values into a dictionary
        iterator = iter(command_parts[1:])  # Skip the first command ('')
        for part in iterator:
            if part.startswith('--'):  # Check for flags
                key = part.lstrip('--')
                value = next(iterator, None)  # Get the next item as value
                my_query[key] = value

        return my_query

    #####
    # METHOD: create_queries
    #####
    def create_queries(self, query_stage : str, query_list : list[str], models = None) -> bool:

        self.query_struct["tests"].clear()
        assert len(query_list) > 0, "No queries provided"

        if len(query_list) == 1:
            # run the query against each model
            for m in models:
                self.__add_query(query=query_list[0], model=m)
        else:
            # run each query against the first model
            for i in range(len(query_list)):
                self.__add_query(query=query_list[i], model=models[i])

        # Write the data to a JSON file
        self.agent_input_file = f"{INPUT_QUERIES_DIR}/{self.agent_name()}-{query_stage}.json"
        with open(self.agent_input_file , "w") as json_file:
            json.dump(self.query_struct, json_file, indent=4)

        return True

    #####
    # METHOD: execute_queries
    #####
    def execute_queries(self) -> str:

        assert self.agent_input_file is not None, "No queries to execute"

        command_list : list[str] = ['program_here']
        command_list.extend(['--i', self.agent_input_file])
        # print(f"Executing command: {command_list}")
        result : subprocess.CompletedProcess = subprocess.run(command_list, capture_output=True, text=True)
        # print(result.stdout)
        return result.stdout

    #####
    # METHOD: save_results_to_calalog
    #####
    def save_results_to_calalog(self, results) -> None:

        json_results = json.loads(results)
        individual_results = json_results['all_results']
        with open(LEARNED_RESULTS_FILE, 'w') as f:
            for one_result in individual_results:
                parsed_query = self.parse_query_string(one_result['query'])
                f.write(f'''
--------------------
MODEL: {parsed_query['model']}
{one_result['message']}
''')
            
        command_list : list[str] = ['program_here', 'ingest', self.output_catalog, '-u', LEARNED_RESULTS_FILE]
        result : subprocess.CompletedProcess = subprocess.run(command_list, capture_output=True, text=True)

        print(f"Results saved to catalog: {command_list}")
        print(result.stdout)

    ########################## abscract methods ##########################

    #####
    # METHOD: test_results_in_simulation (abstract)
    #####
    @abstractmethod
    def test_results_in_simulation(self, query_results : dict[str, str]) -> None:
        pass

    #####
    # METHOD: evaluate_simulation_result (abstract)
    #####
    # @abstractmethod
    # def evaluate_simulation_result(self, query_results : dict[str, str]) -> None:
    #     pass

    #####
    # METHOD: agent_name (abstract)
    #####
    @abstractmethod
    def agent_name(self) -> str:
        pass