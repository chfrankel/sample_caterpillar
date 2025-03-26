#!python3
# © 2025 Charles Frankel. All rights reserved.

import argparse
import functools
import json
import os
import subprocess
import time
from multiprocessing.pool import Pool

# a custom python library that allows for the updating of npm packages - only if the version changed e.g.
from cli_runner.cli_npm import npm_updater
#
# test jsons should exercise query, serp, for-each? smart-search and smart-query
# currently, both "serp" and "smart_search" return an error code of 429
# Commands:
#   xxxxx query <query>         
#   xxxxx serp <query>          
#   xxxxx for-each <query>    
#                             
#   xxxxx smart-search <query>  
#   xxxxx smart-query <query>   
#                                   

def _run_one_test_method_alias(obj, arg):
    """
    Alias for instance method that allows the method to be called in a 
    multiprocessing pool
    """
    return obj.run_one_test(arg)

##############################################################################################################
##########################################   class tester   ##########################################
##############################################################################################################
class tester:

    ########################################## Loading Tests ##########################################
    # method: __init__
    def __init__(self, test_input_file):
        self.successful_tests = []
        self.failed_tests = []

        if not os.path.isfile(test_input_file):
            raise Exception(f'Could not find {test_input_file} in the current directory')
        self.load_json_file(test_input_file)

    # load all the paremeters and tests from the input file
    def load_json_file(self, test_input_file : str):
                
        with open(test_input_file) as f:

            input_json = json.load(f)

            self.print_output     = input_json.get('print-output')
            self.print_summary    = input_json.get('print-summary')
            self.parallel_tasks   = input_json.get('parallel-tasks')
            self.json_output      = input_json.get('json-output')
            self.tests            = input_json.get('tests')
            if not self.tests:
                s = f'cound not find the "tests" attribute in {test_input_file}'
                raise Exception(s)

    ########################################## Printing Results ##########################################

    # method: print_test_results_summary
    def print_test_results_summary(self) -> dict:

        successful_tests = f"{len(self.successful_tests)}\n"
        for i in self.successful_tests:
            successful_tests += f"{i}\n"
            
        failed_tests = f"{len(self.failed_tests)}"
        for i in self.failed_tests:
            failed_tests += f"{i}\n"

        summary = {'successful_tests': successful_tests, 'failed_tests': failed_tests}

        if not self.json_output:
            print(summary)
        return summary
    
    # accepts a completed process and 
    def _process_one_result(self, r : subprocess.CompletedProcess) -> dict:

        quoted_args = [x if ' ' not in x else f'"{x}"' for x in r.args]
        cleaned_query = ' '.join([x for x in quoted_args])
        
        one_result_summary = {}

        one_result_summary['query'] = cleaned_query
        one_result_summary['return_code'] = r.returncode

        if r.returncode == 0:

            self.successful_tests.extend([cleaned_query])

            beginning_json_index = r.stdout.find('{')
            if beginning_json_index != -1: #json potentially found
                try:
                    output_json = json.loads(r.stdout[beginning_json_index:])
                    one_result_summary['message'] = output_json.get('message')
                    one_result_summary['details'] = output_json.get('details')

                    if beginning_json_index > 0:
                        beginning_stdout = r.stdout[:beginning_json_index]
                        one_result_summary['additional_messages'] = beginning_stdout

                    return one_result_summary
                except:
                    return r.stdout
            else:
                return r.stdout

        else:
            self.failed_tests.extend([cleaned_query])
            return r.stderr

    # method: print_output
    # prints the output of the tests - main entry point for the printing
    def return_results(self, output, execution_time):
        if self.print_summary:
            output['summary'] = self.print_test_results_summary()
        output['execution_time'] = f"{ (execution_time):.2f} seconds"

        if self.print_output:
            print(output)
        elif self.json_output:
            print(json.dumps(output, indent=4))
        else:
            print(f"No output, set 'print-output' or 'json_ouput' to true to see the output")
    ########################################## Executing Tests ##########################################

    # method: execute_llm
    def run_one_test(self, query: dict) -> subprocess.CompletedProcess:

        program = query['program']

        command_list : list[str] = [program]
        if program == 'xxxxx':                   # Only xxxxx supports json output currrently
            command_list.extend(['--output', 'json'])

        for key, value in query.items():
            if key == 'expected' or key == 'program':
                continue
            if key != 'query' and key != 'serp':
                key = f'--{key}'
            command_list.extend([key, str(value)])

        return subprocess.run(command_list, capture_output=True, text=True)
        
    # method: run_all_tests
    def run_all_tests(self) -> dict:
        if self.parallel_tasks:
            processes = os.cpu_count() 
        else:
            processes = 1 

        output = {}
        _bound_run_one_test_alias = functools.partial(_run_one_test_method_alias, self)
        with Pool(processes=processes) as pool:
            results = pool.map(_bound_run_one_test_alias, self.tests)
            output['all_results'] = [self._process_one_result(r) for r in results]

        assert(len(output) > 0), "No results found"
        return output

##############################################################################################################
########################################## end class tester   ########################################
##############################################################################################################

def main():
    INPUT_FILE = "tests.json"

    # command line arguements
    parser = argparse.ArgumentParser(description="test runner")
    parser.add_argument("-f", "--force", help = "Force execution even if version has not changed", action=argparse.BooleanOptionalAction)
    parser.add_argument("-u", "--update", help = "Update xxxx cli before execution", action=argparse.BooleanOptionalAction)
    parser.add_argument("-i", "--input", help = "json parameter file to run", type=str, default=INPUT_FILE)
    args = parser.parse_args()

    if args.update:
        u = npm_updater()
        if not u.version_changed and not args.force:
            print("not executing tests because the cli version has not changed, and the 'force' argument was not set")
        return

    if not os.path.isfile(args.input):
        # Get the current working directory
        current_directory = os.getcwd()
        print(f"The current working directory is: {current_directory}")
        print(f"could not find input file to run '{args.input}', exiting")
        return
    
    start_time = time.time()
    a = tester(args.input)
    output = a.run_all_tests()

    a.return_results(output, execution_time = time.time() - start_time)

############ Program Entry Point ############
if __name__ == "__main__":
    main()
