



# %%

from typing import Any, Callable, Iterable, Tuple

test_state = 1

class Condition:
    """
    A data structure to represent information related to a condition.
    """
    def __init__(self, threshold: float, check: 'Callable[[Any], bool]'):
        self.threshold = threshold
        self.check_fulfillment = check

    def is_fulfilled(self, fulfillment: float) -> bool:
        """
        Checks if the condition is fulfilled.
        """
        return fulfillment >= self.threshold

test_condition_1 = Condition(0.5, lambda state: state == 1)
test_condition_1_2 = Condition(0.5, lambda state: state == 1)
test_condition_2 = Condition(0.5, lambda state: state == 2)
test_condition_3 = Condition(0.5, lambda state: state == 3)
test_conditions = {'condition1': test_condition_1, 'condition1_2': test_condition_1_2, 'condition2': test_condition_2, 'condition3': test_condition_3}

class Update:
    """
    A data structure to represent information related to an update.

    # ....
    > for apply: return None for when exhausted
    """
    def __init__(self, prerequisites: 'Iterable[str]', apply: 'Callable[[Any], Any]'):
        self.prerequisites = prerequisites
        self.apply = apply

    def is_fulfilled(self, fulfilled_conditions: 'dict[str, Condition]') -> bool:
        """Checks if the update's prerequisites have been fulfilled."""
        # return all(condition.name in update.prerequisites for condition in fulfilled_conditions)
        # return all(condition_name in update.prerequisites for condition_name in fulfilled_conditions.keys())
        return all(prerequisite in fulfilled_conditions.keys() for prerequisite in self.prerequisites)
test_update_1 = Update(['condition1', 'condition2'], lambda state: state + 1)
test_update_2 = Update(['condition1', 'condition3'], lambda state: state + 2)
test_update_3 = Update(['condition1', 'condition1_2'], lambda state: state + 2)
test_is_fulfilled_Update_False = test_update_1.is_fulfilled({'condition1': test_condition_1})
test_is_fulfilled_Update_True = test_update_1.is_fulfilled({'condition1': test_condition_1, 'condition2': test_condition_2})

def find_prereqs(updates: 'dict[str, Update]') -> 'set[str]':
    """Retrieve a consolidated set of prerequisites for a group of updates."""
    return set().union(*[update.prerequisites for update in updates.values()])
    # return [prerequisite for update in updates.values() for prerequisite in update.prerequisites]
test_find_prereqs = find_prereqs({'update1': test_update_1, 'update2': test_update_2})

def find_fulfillment(state: Any, conditions: 'dict[str, Condition]') -> 'dict[str, float]':
    """Finds the fulfillment of the given conditions for a particular state."""
    return {condition_name: condition.check_fulfillment(state) for condition_name, condition in conditions.items()}
    # return sum(condition.check_fulfillment(state) for condition in conditions.values())

def is_valid(proposed_fulfillment: 'dict[str, int]', applied_updates: 'dict[str, Update]', conditions: 'dict[str, Condition]') -> bool:
    """Checks if the proposed state is valid."""
    # check if the proposed state would cause any of the dependencies to be violated
    dependencies = find_prereqs(applied_updates)
    for dependency_name in dependencies:
        # print(dependency_name)
        dependency = conditions[dependency_name]
        if not dependency.is_fulfilled(proposed_fulfillment[dependency_name]):
            return False
    return True
test_applied_updates_1 = {'update1': test_update_1, 'update2': test_update_2}
test_applied_updates_2 = {'update3': test_update_3}
test_fulfillment = find_fulfillment(test_state, test_conditions)
test_is_valid_False = is_valid(test_fulfillment, test_applied_updates_1, test_conditions)
test_is_valid_True = is_valid(test_fulfillment, test_applied_updates_2, test_conditions)
# test_is_valid_False = is_valid(test_state, test_applied_updates_1, test_conditions)
# test_is_valid_True = is_valid(test_state, test_applied_updates_2, test_conditions)

def assemble_updates(initial_state: Any, proposed_updates: 'dict[str, Update]', desired_conditions: 'dict[str, Condition]', max_exhaustion: int=1) -> 'Tuple[Any, dict[str, Update], dict[str, Condition]]':
    """Creates a sequence of updates that attempts to satisfy all desired conditions when applied on the state."""

    # initialize loop variables
    done = False
    exhaustion = 0
    while(not done):
        was_updated = False
        current_state = initial_state
        applied_updates = {}
        fulfilled_conditions = {}
        for update_name, update in proposed_updates.items():
            # if update's prerequisite conditions have not been fulfilled, then skip it
            if not update.is_fulfilled(fulfilled_conditions):
                continue
            # otherwise, evaluate the update
            proposed_state = update.apply(current_state)
            if proposed_state is None:
                continue
            current_condition_fulfillment = find_fulfillment(current_state, desired_conditions)
            proposed_condition_fulfillment = find_fulfillment(proposed_state, desired_conditions)
            # if the proposed state is not valid or doesn't increase fulfillment, then skip it
            if not is_valid(proposed_state, applied_updates, desired_conditions) \
                or sum(proposed_condition_fulfillment.values()) <= sum(current_condition_fulfillment.values()):
                continue
            # otherwise, update the state and the applied updates
            current_state = proposed_state
            applied_updates[update_name] = update
            new_fulfilled_conditions = {condition_name: condition for condition_name, condition in desired_conditions.items() if condition.is_fulfilled(proposed_condition_fulfillment[condition_name])}
            fulfilled_conditions.update(new_fulfilled_conditions)
            was_updated = True
        # if no updates were applied, then increase exhaustion, and break the loop if exhaustion is too high
        if not was_updated:
            exhaustion += 1
        if exhaustion >= max_exhaustion:
            done = True
    return current_state, applied_updates, fulfilled_conditions