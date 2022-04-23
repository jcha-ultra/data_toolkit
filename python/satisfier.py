"""This is an idea for creating a system for figuring out how to navigate between a potentially heterogenous set of requirements in an automated way."""

from random import random
from typing import Any, Callable, Tuple

import numpy as np

class RequirementInfo:
    """A class to keep track of a requirement's information."""
    def __init__(self, id: int, importance: int, ease: int, requirement: Callable, satisfaction: int):
        self.id = id
        self.importance = importance
        self.ease = ease
        self.requirement = requirement
        self.satisfaction = satisfaction
    
    @property
    def priority(self) -> int:
        return self.importance * ((1-self.satisfaction)/(4*self.satisfaction+1)) * self.ease

def is_satisfied(requirement_tracker: list[RequirementInfo]) -> bool:
    """Determines whether all of the requirements in the tracker are satisfied.
    
    Parameters
    ----------
        A list of RequirementInfo objects to check the satisfaction of.
    
    Returns
    -------
        Whether all of the requirements in the tracker are satisfied.
    """
    for info in requirement_tracker:
        if info.satisfaction < 1:
            return False
    return True

def get_satisfaction(requirement_tracker: list[RequirementInfo]) -> float:
    """Gets the satisfaction of all of the requirements in the tracker.
    
    Parameters
    ----------
    requirement_tracker : list[RequirementInfo]
        A list of RequirementInfo objects to get the satisfaction of.
    
    Returns
    -------
    float
        The satisfaction of all of the requirements in the tracker.
    """
    return sum([info.satisfaction * info.importance for info in requirement_tracker])

def find_satisfaction(requirement_tracker: list[RequirementInfo], state: Any) -> float:
    """Gets the satisfaction of all of the requirements in the tracker, for a potential state to evaluate.
    
    Parameters
    ----------
    requirement_tracker : list[RequirementInfo]
        A list of RequirementInfo objects to find the satisfaction of.
    state : Any
        The state to evaluate the satisfaction of the requirements for.
    
    Returns
    -------
    float
        The summed satisfaction of all of the requirements in the tracker, given the state.
    """

    return sum([info.importance * max(0, min(1, info.requirement(state)[0])) for info in requirement_tracker])

def update_satisfaction(requirement_tracker: list[RequirementInfo], state: Any) -> None:
    """Updates the satisfaction of all of the requirements in the tracker, given a state to evaluate.
    
    Parameters
    ----------
    requirement_tracker : list[RequirementInfo]
        A list of RequirementInfo objects to update the satisfaction of.
    state : Any
        The state to update the satisfaction of the requirements for.

    Returns
    -------
    None
    """
    for info in requirement_tracker:
        info.satisfaction = max(0, min(1, info.requirement(state)[0]))
    return

def apply_requirements(requirements: list[Callable[[Any], Tuple[float, Callable[[Any], Any]]]], initial_state: Any, importance: list[int], stalemate_threshold: int=5) -> Tuple[Any, dict]:
    """Applies the requirements to the initial state, returning the final state and a dictionary of how the requirements were satisfied.
    
    Parameters
    ----------
    requirements : list[Callable[[Any], Tuple[float, Callable[[Any], Any]]]]
        A list of requirements that apply to the state.
    initial_state : Any
        The initial state to apply the requirements to.
    importance : list[int]
        A list of importance values for the requirements. More important requirements will get more consideration when calculating the satisfaction score.
    stalemate_count : int, optional
        The number of times to try to apply the requirements to the state without improvements before giving up. The default is 5.

    Returns
    -------
    Tuple[Any, dict]
        A tuple of the final state and a dictionary of how well each of the requirements were satisfied.
    """

    if importance is None: importance = [1] * len(requirements)
    state = initial_state
    
    # initiate the requirement tracking
    requirement_tracker = []
    for requirement, importance in zip(requirements, importance):
        satisfaction, _ = requirement(state)
        requirement_tracker.append(RequirementInfo(len(requirement_tracker), importance, 1, requirement, satisfaction))

    stalemate_count = 0
    while(not is_satisfied(requirement_tracker) and stalemate_count < stalemate_threshold):
        # track whether the rating improvement process has stalled
        current_satisfaction = get_satisfaction(requirement_tracker)

        print(stalemate_count, state)

        # find the highest priority requirement and evaluate its proposal via the other requirements
        for info in sorted(requirement_tracker, key=lambda x: x.priority, reverse=True):
            _, proposal = info.requirement(state)
            proposed_state = proposal(state)
            proposal_rating = find_satisfaction(requirement_tracker, proposed_state)
            if proposal_rating > current_satisfaction:
                state = proposed_state
                new_satisfaction = proposal_rating
                update_satisfaction(requirement_tracker, state)
                break
            # if the proposal causes the satisfaction score to go down, reduce how easy the requirement is to satisfy
            if proposal_rating < current_satisfaction:
                info.ease *= 0.5
        
        # if the satisfaction rating has not improved, increase the stalemate count
        if current_satisfaction == new_satisfaction:
            stalemate_count += 1

    return state, {info.id: info.satisfaction for info in requirement_tracker}

def test_apply_requirements():
    """A Test function for `apply_requirements`."""
    def test_less_1k(n):
        if n < 1000:
            satisfaction = 1
        else:
            satisfaction = 999/n
        proposal = lambda n: n if n < 1000 else int(n/2 - 50*random())
        return satisfaction, proposal

    def test_is_odd(n):
        if n % 2 == 1:
            satisfaction = 1
        else:
            satisfaction = 0
        proposal = lambda n: n if n % 2 == 1 else n+1
        return satisfaction, proposal

    def ends_with_3(n):
        if n % 10 == 3:
            satisfaction = 1
        else:
            satisfaction = 0
        proposal = lambda n: n if n % 10 == 3 else n + 13 - (n % 10)
        return satisfaction, proposal

    def is_large(n):
        satisfaction = max(0, (n-1)/(n))
        proposal = lambda n: int(n*1.5 * (random()+1))
        return satisfaction, proposal

    def test_is_prime(n):
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(np.sqrt(n))+1):
                if n % i == 0:
                    return False
            return True
        satisfaction = 1 if is_prime(n) else 0
        proposal = lambda n: n if is_prime(n) else int(n+10*random())
        return satisfaction, proposal
    return apply_requirements([test_is_prime, test_less_1k, test_is_odd, ends_with_3], 2000, [1, 1, 1, 1], 10000)
