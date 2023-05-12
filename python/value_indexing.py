
def map_by_value_index(dataset_A, dataset_B, value_index, keymap):
    """Map records from one dataset to another via value index method."""
    # Flatten record_data from dataset_A and dataset_B
    flattened_dataset_A = [record for sublist in dataset_A for record in sublist["record_data"]]
    flattened_dataset_B = [record for sublist in dataset_B for record in sublist["record_data"]]

    # Filter dataset_A using value_index
    filtered_dataset_A = [
        record
        for record in flattened_dataset_A
        if all(record[key] in value_index[key] for key in value_index)
    ]

    # Create a set of keys from filtered_dataset_A after applying the keymap
    mapped_keys = {tuple((keymap[k], v) for k, v in record.items()) for record in filtered_dataset_A}

    # Filter dataset_B using the mapped_keys
    mapped_values = [
        record for record in flattened_dataset_B if tuple(record.items()) in mapped_keys
    ]

    return mapped_values