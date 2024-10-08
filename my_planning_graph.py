from itertools import chain, combinations
from aimacode.planning import Action
from aimacode.utils import expr
from layers import BaseActionLayer, BaseLiteralLayer, makeNoOp, make_node

class ActionLayer(BaseActionLayer):

    def _inconsistent_effects(self, actionA, actionB):

        for effectA in actionA.effects:
            if ~effectA in actionB.effects:
                return True

        return False
      


    def _interference(self, actionA, actionB):

        for effect in actionA.effects:
            
            for precondition in actionB.preconditions:
                
                if precondition == ~effect:
                    return True
        #raise NotImplementedError

    def _competing_needs(self, actionA, actionB):
        _parent = self.parent_layer
        
        for preconA in actionA.preconditions:
            for preconB in actionB.preconditions:
                if  _parent.is_mutex(preconA, preconB): return True
        return False

        #raise NotImplementedError


class LiteralLayer(BaseLiteralLayer):

    def _inconsistent_support(self, literalA, literalB):
        """ Return True if all ways to achieve both literals are pairwise mutex in the parent layer
        See Also
        --------
        layers.BaseLayer.parent_layer
        """
        
        return all(self.parent_layer.is_mutex(actionA,actionB) 
                   for actionA in self.parents[literalA] 
                   for actionB in self.parents[literalB]) \
                and all(self.parent_layer.is_mutex(actionB, actionA) 
                        for actionA in self.parents[literalA] 
                        for actionB in self.parents[literalB])

        #raise NotImplementedError

    def _negation(self, literalA, literalB):
        """ Return True if two literals are negations of each other """
        return literalA == ~literalB
        #raise NotImplementedError


class PlanningGraph:
    def __init__(self, problem, state, serialize=True, ignore_mutexes=False):
        """
        Parameters
        ----------
        problem : PlanningProblem
            An instance of the PlanningProblem class
        state : tuple(bool)
            An ordered sequence of True/False values indicating the literal value
            of the corresponding fluent in problem.state_map
        serialize : bool
            Flag indicating whether to serialize non-persistence actions. Actions
            should NOT be serialized for regression search (e.g., GraphPlan), and
            _should_ be serialized if the planning graph is being used to estimate
            a heuristic
        """
        self._serialize = serialize
        self._is_leveled = False
        self._ignore_mutexes = ignore_mutexes
        self.goal = set(problem.goal)

        # make no-op actions that persist every literal to the next layer
        no_ops = [make_node(n, no_op=True) for n in chain(*(makeNoOp(s) for s in problem.state_map))]
        self._actionNodes = no_ops + [make_node(a) for a in problem.actions_list]
        
        # initialize the planning graph by finding the literals that are in the
        # first layer and finding the actions they they should be connected to
        literals = [s if f else ~s for f, s in zip(state, problem.state_map)]
        layer = LiteralLayer(literals, ActionLayer(), self._ignore_mutexes)
        layer.update_mutexes()
        self.literal_layers = [layer]
        self.action_layers = []

    def h_levelsum(self):
        """ Calculate the level sum heuristic for the planning graph
        The level sum is the sum of the level costs of all the goal literals
        combined. The "level cost" to achieve any single goal literal is the
        level at which the literal first appears in the planning graph. Note
        that the level cost is **NOT** the minimum number of actions to
        achieve a single goal literal.
        
        For example, if Goal1 first appears in level 0 of the graph (i.e.,
        it is satisfied at the root of the planning graph) and Goal2 first
        appears in level 3, then the levelsum is 0 + 3 = 3.
        Hint: expand the graph one level at a time and accumulate the level
        cost of each goal.
        See Also
        --------
        Russell-Norvig 10.3.1 (3rd Edition)
        """

        _graph = self
        remainingGoals = [goal for goal in _graph.goal]
        satisfiedGoals = []
        
        currentLevel = 0
        levelCost = 0

        while remainingGoals:
            _level = _graph.literal_layers[currentLevel]
            
            for g in remainingGoals:
                if g in _level:
                    levelCost  += currentLevel
                    satisfiedGoals.append(g)
                
            if satisfiedGoals: remainingGoals = [g for g in remainingGoals if g not in satisfiedGoals]    
                
            if remainingGoals:
                _graph._extend()
                currentLevel += 1   
                
        return levelCost

        # raise NotImplementedError

    def h_maxlevel(self):

        self.fill()
        level_cost = 0
        for goal in self.goal:
            for cost, layer in enumerate(self.literal_layers):
                if goal in layer:
                    level_cost = max(cost, level_cost)
                    break
        return level_cost
        #raise NotImplementedError

    def h_setlevel(self):

        while not self._is_leveled:
            
            layer = self.literal_layers[-1]

            if self.goal.issubset(layer):
                
                no_pairmutex = True

                for goal1 in self.goal:
                    for goal2 in self.goal:
                        if layer.is_mutex(goal1, goal2):
                            no_pairmutex = False
                            break

                if no_pairmutex:
                    return len(self.literal_layers) - 1

            self._extend()

        return len(self.literal_layers) - 1   
        #raise NotImplementedError


    def levelcost(self, graph, goal):

        for level, layer in enumerate(self.literal_layers):

            if goal in layer:
                return level



    ##############################################################################
    #                     DO NOT MODIFY CODE BELOW THIS LINE                     #
    ##############################################################################

    def fill(self, maxlevels=-1):
        """ Extend the planning graph until it is leveled, or until a specified number of
        levels have been added
        Parameters
        ----------
        maxlevels : int
            The maximum number of levels to extend before breaking the loop. (Starting with
            a negative value will never interrupt the loop.)
        Notes
        -----
        YOU SHOULD NOT THIS FUNCTION TO COMPLETE THE PROJECT, BUT IT MAY BE USEFUL FOR TESTING
        """
        while not self._is_leveled:
            if maxlevels == 0: break
            self._extend()
            maxlevels -= 1
        return self

    def _extend(self):
        """ Extend the planning graph by adding both a new action layer and a new literal layer
        The new action layer contains all actions that could be taken given the positive AND
        negative literals in the leaf nodes of the parent literal level.
        The new literal layer contains all literals that could result from taking each possible
        action in the NEW action layer. 
        """
        if self._is_leveled: return

        parent_literals = self.literal_layers[-1]
        parent_actions = parent_literals.parent_layer
        action_layer = ActionLayer(parent_actions, parent_literals, self._serialize, self._ignore_mutexes)
        literal_layer = LiteralLayer(parent_literals, action_layer, self._ignore_mutexes)

        for action in self._actionNodes:
            # actions in the parent layer are skipped because are added monotonically to planning graphs,
            # which is performed automatically in the ActionLayer and LiteralLayer constructors
            if action not in parent_actions and action.preconditions <= parent_literals:
                action_layer.add(action)
                literal_layer |= action.effects

                # add two-way edges in the graph connecting the parent layer with the new action
                parent_literals.add_outbound_edges(action, action.preconditions)
                action_layer.add_inbound_edges(action, action.preconditions)

                # # add two-way edges in the graph connecting the new literaly layer with the new action
                action_layer.add_outbound_edges(action, action.effects)
                literal_layer.add_inbound_edges(action, action.effects)

        action_layer.update_mutexes()
        literal_layer.update_mutexes()
        self.action_layers.append(action_layer)
        self.literal_layers.append(literal_layer)
        self._is_leveled = literal_layer == action_layer.parent_layer