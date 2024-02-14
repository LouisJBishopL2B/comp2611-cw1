#!/usr/bin/env python
# coding: utf-8

# # bbSearch
# 
# This version of `bbSearch` written during January and February 2022.
# 
# 
# ### My personal notes:
# To install on cloud for download use shell script `publish-bbSearch`.

# In[47]:


#<<<
#<<< def __MAKE_SCRIPT__(notebook_stem):
#<<<     get_ipython().system( f' jupyter nbconvert --to python {notebook_stem}.ipynb')
#<<<     with open( notebook_stem + ".py", "r") as f: 
#<<<         lines = f.read().split('\n')      
#<<<     new_lines = []
#<<<     exclude = False
#<<<     for l in lines:
#<<<         if l.startswith("#<<<"):
#<<<             exclude = True
#<<<             new_lines.append(l)
#<<<             continue
#<<<         if l.startswith("#>>>"):
#<<<             exclude = False
#<<<             new_lines.append(l)
#<<<             continue
#<<<         if exclude:
#<<<             new_lines.append("#<<< " + l)
#<<<         else:
#<<<             new_lines.append(l)
#<<<             
#<<<     new_content = '\n'.join(new_lines) 
#<<<     #new_content = "### MODIFIED\n" + new_content
#<<<     with open( notebook_stem + ".py", "w") as f:    
#<<<         f.write(new_content) 
#<<<    
#<<< __MAKE_SCRIPT__("bbSearch")
#<<< get_ipython().system('s3cmd put --acl-public bbSearch.py s3://bb-ai.net/bb-python-modules/')
#>>>


# In[34]:


from datetime import datetime
time = datetime.now().strftime("%H:%M, %a %d %b")
print(f"Loading bbSearch Version 2.1 (at {time})")
print("Last module source code edit 9am Thursday 24th Feb 2022")


# In[35]:


class SearchProblem:

    def __init__( self ):
        """
        The __init__ method must set the initial state for the search.
        Arguments could be added to __init__ and used to configure the
        initial state and/or other aspects of a problem instance.
        """
        self.initial_state = None
        raise NotImplementedError

    def info(self):
        """
        This function is called when the search is stared and should
        print out useful information about the problem.
        """
        print("This is the general SearchProblem parent class")
        print("You must extend this class to encode a particular search problem.")

    def possible_actions(self, state):
        """
        This takes a state as argument and must return a list of actions.
        Both states and actions can be any kinds of python data type (e.g.
        numbers, strings, tuples or complex objects of any class).
        """
        return []

    def successor(self, state, action):
        """
        This takes a state and an action and returns the new state that would result
        from doing that action in that state. You can assume that the given action
        is in the list of 'possible_actions' for that state. 
        """
        return state

    def goal_test(self, state):
        """
        This method shoudl return True or False given any state. It should return 
        True for all and only those states that are considert "goal" states.
        """
        return False
    
    def cost(self, path, state):
        """
        This is an optional method that you only need to define if you are using
        a cost based algorithm such as "uniform cost" or "A*". It should return
        the cost of reaching a given state via a given path.
        If this is not defined, it will is assumed that each action costs one unit
        of effort to perform, so it returns the length of the path.
        """
        return len(path)
    
    def heuristic(self, state):
        """
        This is an optional method that should return a heuristic value for any
        state. The value should be an estimate of the remaining cost that will be
        required to reach a goal. For an "admissible" heuristic, the value should
        always be equal to or less than the actual cost.
        """
        raise NotImplementedError

    def display_action(self, action):
        """
        You can set the way an action will be displayed in outputs.
        """
        print("   ", action)

    def display_state(self, state):
        """
        You can set the way a state will be displayed in outputs.
        """
        print(state)
        
    def display_state_path( self, actions ):
        """
        This defines output of a solution path when a list of actions
        is applied to the initial state. It assumes it is a valid path
        with all actions being possible in the preceeding state.
        You probably don't need to override this.
        """
        s = self.initial_state
        self.display_state(s)
        for a in actions:
            self.display_action(a)
            s = self.successor(s,a)
            self.display_state(s)


# In[36]:


class JugPouringPuzzle( SearchProblem ):
    
    def __init__( self, initial_state, goal_quantity ):
        self.initial_state = initial_state
        self.goal_quantity = goal_quantity
        print( "Creating SearchProblem object" )
        print( "Setting initial state to:", self.initial_state )
        print( "Want to measure quantity:", self.goal_quantity )
        
        self.jugs = self.initial_state.keys()

    def info(self):
        print( "\nMeasuring Jugs problem:" )
        print( "You have a number of jugs with a certain volume and initial contents,\n" 
               "as follows:")
        for jar in self.initial_state:
          print(f"{jar:>10} : volume={self.initial_state[jar][0]}, "
                          f"contents={self.initial_state[jar][1]}")
        print( f"The goal is to measure the quantity {self.goal_quantity} "
                "by pourning liquid between the jugs.")

    def possible_actions(self, state):
        actions = []
        for j1 in self.jugs:
            for j2 in self.jugs:
                if ( j1!=j2  #different jugs
                     and state[j1][1] > 0  # j1 not empty
                     and state[j2][0]>state[j2][1] # j2 not full
                   ): actions.append((j1,j2))
        return actions
                    
    def successor(self, state, action):
        new_state = { k:state[k] for k in state }
        j1, j2 = action[0], action[1]
        vol_in_j1 = state[j1][1]
        vol_in_j2 = state[j2][1]
        space_in_j2 = state[j2][0] - state[j2][1]
        if vol_in_j1 <= space_in_j2:
            new_j1 = 0
            new_j2 = vol_in_j1 + vol_in_j2
        else:
            new_j1 = vol_in_j1 - space_in_j2
            new_j2 = state[j2][0]
        new_state[j1] = (state[j1][0], new_j1)
        new_state[j2] = (state[j2][0], new_j2)
        return new_state

    def goal_test(self, state):
        quantities = [ state[k][1] for k in state]
        return  self.goal_quantity in quantities

    def display_action( self, action ):
        j1, j2 = action
        print(f"Pour from {j1} to {j2}:")

    def display_state( self, state ):
        jug_quantities = [ f"{k} ({state[k][0]}): {state[k][1]}" for k in state]
        print( ", ".join(jug_quantities))


# In[37]:


import bisect

## This is a Weighted queue optimised by using the bisect module
## to insert into the item list (via key indirection).

class WeightedQueue:
    
    def __init__(self, mode='fifo', weighted=True, weightfunc=None ):
        self.weighted = weighted
        self.weightfunc = weightfunc
        self.mode = mode
        self.weights = []
        self.items   = []
        
        if mode == 'fifo':
            if self.weighted:
                self.insert = self.insert_right
                self.pop = self.pop_weighted
            else:
                self.insert = self.add_right
        
        elif mode == 'lifo':
            if self.weighted:
                self.insert = self.insert_left
                self.pop = self.pop_weighted
            else:
                self.insert = self.add_left
                
 
        else:
            raise ValueError("!!! WeightedQueue 'mode' keyword arg "
                                  "must be 'fifo' or 'lifo'")
        
        
    def add_left(self,item, weight=None):
        self.items.insert(0,item)
        
    def add_right(self,item, weight=None):
        self.items.append(item)

    def insert_left(self, item, weight = None):
        if weight == None:
            weight = self.weightfunc(item)
        ipoint = bisect.bisect_left(self.weights, weight)
        bisect.insort_left(self.weights, weight)
        self.items.insert(ipoint,item)
        
    def insert_right(self, item, weight = None):
        if weight == None:
            weight = self.weightfunc(item)
        ipoint = bisect.bisect_right(self.weights, weight)
        bisect.insort_right(self.weights, weight)
        self.items.insert(ipoint,item)
        
    def initialise(self, items, weights=None):
        self.items = items
        if weights:
            iwpairs = list(zip(items,weights))
            iwpairs.sort(key=lambda x:x[1])
            self.items   = [x[0] for x in iwpairs]
            self.weights = [x[1] for x in iwpairs]
        elif self.weightfunc:
            self.items.sort(key=self.weightfunc)
            self.weights = [self.weightfunc(i) for i in self.items]
        
    def pop(self):
        return self.items.pop(0)
    
    def pop_weighted(self):
        self.weights.pop(0)
        return self.items.pop(0)
    
    def display(self):
        for w, i in zip(self.weights, self.items):
            print(f"{w}: {i}")
    


# In[44]:


class SearchQueue:
    
    def __init__( self, mode='BF/FIFO', cost=None, heuristic=None ):
        self.mod = mode
        self.cost = cost
        self.heuristic = heuristic
        self.weighted = (cost!=None or heuristic!=None)

        #mode parameter determines whether queue mode is filo or fifo
        modemap = { 'BF/FIFO':'fifo',     'DF/LIFO': 'lifo',
                    'bf'  :   'fifo',          'df': 'lifo', 
                    'BF'  :   'fifo',          'DF': 'lifo', 
                    'fifo':   'fifo',        'lifo': 'lifo',
                    'FIFO':   'fifo',        'LIFO': 'lifo',
           'breadth_first':   'fifo', 'depth_first': 'lifo',
                  }
        if not mode in modemap.keys():
            raise ValueError("!!! SearchQueue 'mode' argument "
                                  "must be 'BF/FIFO' or 'DF/LIFO'")
        
        self.wq = WeightedQueue(modemap[mode], weighted=self.weighted)
                
    def empty(self):
        return self.wq.items == []
    
    def len(self):
        return len(self.wq.items)
    
    def insert(self,item, weight=None):
#         print("Insert in SearchQueue")
#         print("item=", item)
#         print("weight=", weight)
        self.wq.insert(item, weight=weight)
        
    def initialise(self,items,weights=None):
        return self.wq.initialise(items,weights=weights)
        
    def pop(self):
        return self.wq.pop()
    


        
#sq = SearchQueue()       


# In[45]:


import time, random

def search( problem, 
            mode, 
            max_nodes,
            loop_check       = False,
            randomise        = False,
            cost             = None,
            heuristic        = None,
            show_path        = True,
            show_state_path  = False,
            dots             = True,
            return_info      = False,
            #One could potentially define other node limits
            #max_generated    = False,
            #max_discarded    = False 
          ):
    
    problem.info()
    
    print( "\n** Running Brandon's Search Algorithm **")
    cost_name = (cost.__name__ if cost else None)
    heuristic_name = (heuristic.__name__ if heuristic else None)
    print( f"Strategy: mode={mode}, cost={cost_name}, heuristic={heuristic_name}")
    print( f"Max search nodes: {max_nodes}  (max number added to queue)" ) 
    
    start_time = time.perf_counter()
    queue = SearchQueue(mode,cost,heuristic)
    queue.initialise( [([], problem.initial_state )], weights=[0] )
    global weight_function
    weight_function = node_weight_function( cost, heuristic )
    
    states_seen = {problem.initial_state.__repr__()}
    nodes_generated = 1  # counting initial state
    nodes_kept = 1
    nodes_tested = 0
    nodes_discarded = 0
    
    termination_condition = None
    
    node_limit_exceeded = False
    
    if not dots:
        print( "Search started (progress dot output off)", flush=True)
    
    while True:
        if queue.empty():
            termination_condition = "SEARCH-SPACE_EXHAUSTED"  # Means there is no solution.
            break
        
        if dots:
            if nodes_tested % 1000 == 0:
                if nodes_tested==0:
                    print("Searching (will output '.' each 1000 goal_tests)", flush=True)
                else:
                    print('.', end='')
                    if nodes_tested % 100000 == 0:
                        print( f' ({nodes_tested})', flush=True)
        
        path, state = queue.pop()
        nodes_tested += 1
        if problem.goal_test(state):
            termination_condition = "GOAL_STATE_FOUND"
            break
            
        if node_limit_exceeded:
            termination_condition = "NODE_LIMIT_EXCEEDED"
            break
        
        #print("Considering state:", state)
        actions = problem.possible_actions(state)
        #print("Possible actions are:", actions)
        
        if randomise: # randomise action choice sequance (may be useful in DFS)
            random.shuffle(actions)
        
        for i, a in enumerate(actions):
            suc = problem.successor(state,a)
            nodes_generated += 1
            if loop_check:
                if suc.__repr__() in states_seen:
                    nodes_discarded += 1
                    continue # skip already seen state
                else:
                    states_seen.add(suc.__repr__())
            nodes_kept += 1
            if nodes_kept > max_nodes:
                node_limit_exceeded = True
                break
            extended_path = path+[a]
            #print("Making node with path:", extended_path)
            weight=weight_function(extended_path,suc)
            #print("weight=", weight)
            queue.insert((extended_path,suc), 
                         weight=weight)
              
    if termination_condition == "GOAL_STATE_FOUND":
        print( "\n:-)) *SUCCESS* ((-:\n" )
        print( f"Path length = {len(path)}" )
        print( "Goal state is:")
        problem.display_state(state)
        if cost != None:
            print("Cost of reaching goal:", cost(path,state))
        if show_path:
            print( "The action path to the solution is:" )
            for a in path:
                problem.display_action(a)
            print()
        if show_state_path:
            print( "The state/action path to the solution is:" )
            problem.display_state_path(path)
        goal_state = state
        path_length = len(path)
        
    if termination_condition == "SEARCH-SPACE_EXHAUSTED":
        print("\n!! Search space exhausted (tried everying) !!")
        print("): No solution found :(\n")
        goal_state=path=path_length=None
        
    if termination_condition == "NODE_LIMIT_EXCEEDED":
        print( f"\n!! Search node limit ({max_nodes}) reached !!")
        print("): No solution found :(\n")
        goal_state=path=path_length=None

    print( f"\nSEARCH SPACE STATS:")     
    print( f"Total nodes generated          = {nodes_generated:>8}  (includes start)")
    
    if loop_check:
        distinct_states_seen = len(states_seen)
    else:
        distinct_states_seen = "not recorded (loop_check=False)"
    
    if loop_check:
        print( f"Nodes discarded by loop_check  = {nodes_discarded:>8}" 
                f"  ({nodes_generated-nodes_discarded} distinct states added to queue)" )
        #print( f"Distinct states seen  = {distinct_states_seen:>8}" )
        
    print( f"Nodes tested (by goal_test)    = {nodes_tested:>8}",end=' ' )
    if termination_condition == "GOAL_STATE_FOUND":
        print(f" ({nodes_tested-1} expanded + 1 goal)")
    else:
        print( " (all expanded)")
        
    print( f"Nodes left in queue            = {queue.len():>8}")
    time_taken = time.perf_counter() - start_time
    print( f"\nTime taken = {round(time_taken, 4)} seconds\n" )
    
    if not return_info:
        return termination_condition
    else:
        return { 
            "args" : {"problem" : problem.__class__.__name__,
                          "mode" : mode,
                     "max_nodes" : max_nodes,
                    "loop_check" : loop_check,
                     "randomise" : randomise,
                          "cost" : cost_name,
                     "heuristic" : heuristic_name,
                         "dots"  : dots,
                      },
            "result": {
                     "termination_condition": termination_condition,
                     "goal_state"           : goal_state,
                     "path"                 : path,
                     "path_length"          : path_length,
                      },
            "search_stats" : {
                 "nodes_generated"      : nodes_generated,
                 "nodes_tested"         : nodes_tested,
                 "nodes_discarded"      : nodes_discarded,
                 "distinct_states_seen" : distinct_states_seen,
                 "nodes_left_in_queue"  : queue.len(),
                 "time_taken"           : time_taken,
                 }
           }
    


def node_weight_function( cost, heuristic ):    
        if not cost and not heuristic:
            return lambda p,s: None
        if cost and (not heuristic):
            return cost
        if (not cost) and heuristic:
            return lambda p,s: (heuristic(s))
        if cost and heuristic:
            return lambda p,s:(cost(p,s)+heuristic(s))
            
    


# In[46]:


def thecost(p,s):
    return(len(p)**2)


def test():
    JPP1 = JugPouringPuzzle( 
               {"small":(3,0), "medium":(5,0), "large":(8,8)}, #initial state
               4   # goal measurement
            )    

    JPP2 = JugPouringPuzzle( 
               {"small":(3,3), "medium":(5,0), "large":(8,8)}, #initial state
               12   # goal measurement
            )    


    
    res1 = search( JPP1, 'BF/FIFO', 10000, cost=thecost, loop_check=False, show_state_path=True )
    print("res1 =");  display(res1)
    res2 = search( JPP2, 'DF/LIFO', 10000, 
                  #dots = False,
                  randomise=True, loop_check=False, return_info=True)
    print("res2 ="); display(res2)
    
if __name__ == "__main__":
    test()


# In[ ]:





# In[ ]:





# In[ ]:




