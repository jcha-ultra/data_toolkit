def collect_samples(dataset: Any, conditions: 'list[Callable[[list, Any], bool]]', idx_iter: Iterator=None, help_data: Any=None) -> list[Any]:
    """Given a dataframe of matching entries, return a set of sample values such that all of the conditions are fulfilled.

    Parameters
    ----------
    dataset : Any
        The dataset to be sampled.
    conditions : list
        A list of conditions that must be fulfilled by the sample in order for sample collection to be complete. Each condition will be run on the sample set.
    idx_iter : Iterator, optional
        An iterator that can be used to iterate over all indices in the target dataset.
    help_data : Any, optional
        Any additional data that can be used to determine whether the conditions pass or not.

    Returns
    -------
    list[Any]
        A list of indices from the target dataset that satisfies all of the conditions.
    """

    if idx_iter is None:
        idx_iter = make_idx_iter(dataset)

    sample_idxes = []
    pass_count = 0
    def find_pass_count(indices, current_idx) -> int:
        """Given an index under consideration, figure out the number of consecutive passes if you were to include it in the sample."""
        if len(indices) == 0:
            return 0
        nonlocal pass_count
        current_pass_count = 0
        for num, condition in enumerate(conditions):
            try:
                if condition(dataset, indices, help_data):
                    current_pass_count += 1
                else:
                    break
            except:
                print(f"Error: {sys.exc_info()[0]}. {sys.exc_info()[1]}, line: {sys.exc_info()[2].tb_lineno}")
                print(f"Error checking condition {num} while checking sample with index {current_idx}.")
                return 0
        return current_pass_count

    # Add sample indices until all conditions are met, including indices that don't immediately improve the passing rate.
    # The reason is that a single condition may require multiple samples to be added before passing.
    while pass_count < len(conditions):
        next_idx = next(idx_iter)
        new_pass_count = find_pass_count(sample_idxes + [next_idx], next_idx)
        if new_pass_count >= pass_count:
            sample_idxes.append(next_idx)
            pass_count = new_pass_count
    
    # Remove any indices added that aren't needed after all
    trimmed_sample_idxes = []
    for sample_idx in sample_idxes:
        if pass_count > find_pass_count([idx for idx in sample_idxes if idx != sample_idx], sample_idx):
            trimmed_sample_idxes.append(sample_idx)

    return sample_idxes

