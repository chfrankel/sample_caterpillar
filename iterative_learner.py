#!python3
from AGENTS.agent_base import Agent_base
from AGENTS.py_dev_agent import Py_Dev_Agent

LEARNED_CATALOG = 'OUTPUT_DIRECTORIES/LEARNED_CATALOG'

#####
# CLASS: Iterative_Learner
# this class takes an initial query and follow-up queries and saves the learned results
#####
class Iterative_Learner():

    #####
    # METHOD: __init__
    #####
    def __init__(self, agent_class : Agent_base, models, input_catalog = None, output_catalog = None):
        self.agent = agent_class(input_catalog = input_catalog, output_catalog = output_catalog)
        self.agent_name = self.agent.agent_name()
        self.models = models
 
    #####
    # METHOD: run_initial_queries
    #####
    def run_initial_queries(self) -> dict[str, str]:
        self.agent.create_queries(query_stage = 'initial', 
                                  query_list  = [self.agent.get_query('initial_query')], 
                                  models      = self.models)
        
        results = self.agent.execute_queries()
        results = self.agent.test_results_in_simulation(results, iteration=0)
        return results
    
    #####
    # METHOD: run_follow_up_queries
    #
    # results from simulations are in format {model 1: [output, program], model 2: [output, program]}
    #####
    def run_follow_up_queries(self, initial_results, num_follow_up_queries) -> dict[str, str]:
        
        results = initial_results # first iteration uses initial results

        for iteration_number in range(0, num_follow_up_queries):
            print(f'iteration {iteration_number+1}')
 
            # build query_list - unique for each model
            query_list = self.agent.build_iterative_queries(results)
 
            self.agent.create_queries(query_stage = f"follow-up-{iteration_number+1}", 
                                      query_list  = query_list, 
                                      models      = self.models)
            results = self.agent.execute_queries()
            results = self.agent.test_results_in_simulation(results, iteration = iteration_number)
        return results
    
    #####
    # METHOD: run_final_query
    #####
    def run_final_query(self):
        
        self.agent.create_queries(query_stage = 'final', 
                                  query_list  = [self.agent.get_query('final_query')], 
                                  models      = self.models)
        results = self.agent.execute_queries()
        self.agent.save_results_to_calalog(results)

#####
# High-level functions
#####
# ALL_KNOWN_MODELS = ['gpt-4o-mini', 'hybrid', 'gpt-4o'] # this seems to return a dummy result, 'gpt-3.5', or not properly indented code
ALL_KNOWN_MODELS = ['gpt-4o-mini', 'hybrid', 'gpt-4o']
def learn_and_save():
    i = Iterative_Learner(Py_Dev_Agent, models=ALL_KNOWN_MODELS, input_catalog=None, output_catalog=LEARNED_CATALOG)
    print('first query')
    r = i.run_initial_queries()
    i.run_follow_up_queries(r, 3)
    i.run_final_query()

def test_results():
    i = Iterative_Learner(Py_Dev_Agent, models=ALL_KNOWN_MODELS, input_catalog=LEARNED_CATALOG)
    print('first query')
    r = i.run_initial_queries()

#############################################        
############ Program Entry Point ############
#############################################
if __name__ == "__main__":

    # learn_and_save()
    test_results()