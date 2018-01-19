from gym import Env
from gym import error, spaces

'''
ENVIRONMENT

OBSERVATION

ACTIONS

REWARD

START STATE

EPISODE TERMINATION
'''

ACTS = ['switchon_sw1', 'switchoff_sw1']
PROPS = ['switch1_on', 'lightbulb_on']

class LsLiteEnv(Env):
	def __init__(self):
		self.state = None
	'''
	Performs the input action and returns the resulting state, reward
	Input: action
	Ouput: state, reward, done, log_info
	'''
	def _step(self, action):
		clause, act, prop, val = action
		pre, eff = self.state
		done = False
		reward = 0

		target_clause = pre
		if clause:
			target_clause = eff

		# Calculate starting index for triplet
		action_start = 3 * len(PROPS) * act
		prop_start = 3 * prop
		triplet_index = action_start + prop_start

		# Change bits for target triplet to 000
		new_clause_val = set_bit(target_clause, triplet_index, 0)
		new_clause_val = set_bit(new_clause_val, triplet_index + 1, 0)
		new_clause_val = set_bit(new_clause_val, triplet_index + 2, 0)

		if val == 0:
			# Change triplet to 100
			new_clause_val = set_bit(new_clause_val, triplet_index + 2, 1)
		elif val == 1:
			# Change triplet to 010
			new_clause_val = set_bit(new_clause_val, triplet_index + 1, 1)
		else:
			# Change triplet to 001
			new_clause_val = set_bit(new_clause_val, triplet_index, 1)
		if clause == 0:
			self.state = (new_clause_val, eff)
		else:
			self.state = (pre, new_clause_val)

		return self._get_obs(), done, reward, {}

	'''
	Resets the environment to the starting state
	'''
	def _reset(self):
		prop_clear = int('010010010010', 2)
		self.state = (prop_clear, prop_clear)
		self._render()

	'''
	Returns the current state
	'''
	def _get_obs(self):
		return self.state

	'''
	Prints the current domain model
	'''
	def _render(self, mode='human', close = False):
		pre, eff = self.state
		print("Preconditions: " + str(pre))
		print("Effects: " + str(eff))
	'''
	Returns a list of possible actions based on current state

	def getLegalActions(self):
	'''
	@property
	def observation_space(self):
		# (preconditions, effects)
		# Elements in the tuple are binary values that represent state
		# 010010010010 => 010 010 010 010
		return spaces.Tuple(int, int)

	@property
	def action_space(self):
		return spaces.Tuple(spaces.Discrete(2), spaces.Discrete(2), spaces.Discrete(2), spaces.Discrete(3))

	def parse_input(self, input, clause):
	    """
	    Parsing the (3 * n) bit input, based on the binary values.

	    100 - Proposition exists in the positive form
	    010 - Proposition is not present
	    001 - Proposition exists in the negative form

	    pre is a binary value of 0 or 1 indicating whether it is a precondition or effect
	    0 = precondition
	    1 = effect

	    Tests 2 predicates per action AKA 6 bits of the input binary.
	    The last actions potential predicates will be tested by the first 6 bits of the input binary.
	    """
	    accepted_relations = [] #List that stores the actions that are accepted
	    total_actions = int(len(input) / 6) #Each action has 6 binary values for the propositions tested
	    action_index = total_actions - 1 #index starts at 0, so subtract 1 from the total_actions
	    for i in range(0, len(input)):
	        if i % 6 == 0 and i != 0: #Updates the action_index for every 6 binary values
	            action_index -= 1
	        if i % 3 == 0: #Tests 3 bits at a time to see if the proposition is valid
	            if clause == 0:
	                if input[i: i + 3] == "100":
	                    action = ACTS[action_index] + "_has_precondition_pos_" + PROPS[action_index]
	                    #print(action)
	                    accepted_relations.append(action)

	                elif input[i: i + 3] == "001":
	                    action = ACTS[action_index] + "_has_precondition_neg_" + PROPS[action_index]
	                    #print(action)
	                    accepted_relations.append(action)
	                else:
	                    print(PROPS[action_index] + " was NOT an accepted precondition for the action " + ACTS[action_index])
	            else:
	                if input[i: i + 3] == "100":
	                    action = ACTS[action_index] + "_has_effect_pos_" + PROPS[action_index]
	                    #print(action)
	                    accepted_relations.append(action)

	                elif input[i: i + 3] == "001":
	                    action = ACTS[action_index] + "_has_effect_neg_" + PROPS[action_index]
	                    #print(action)
	                    accepted_relations.append(action)
	                else:
	                    print(PROPS[action_index] + " was NOT an accepted effect for the action " + ACTS[action_index])
	    #Prints out the list of accepted relations
	    #print("ACCEPTED ACTIONS: ")
	    #for i in range(0, len(accepted)):
	    	#print(accepted_relations[i])
def set_bit(value, index, flip):
	"""Set the index:th bit of value to 1 if flip = true, else 0"""
	mask = 1 << index
	value &= ~mask
	if flip:
		value |= mask
	return value
