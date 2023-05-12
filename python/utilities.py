def flatten_json(input_dict: dict) -> dict:
    """Recursively and efficiently flatten a json that has been read into memory as a dictionary."""
    # Import the necessary packages
    import collections.abc
    
    # Create an empty output dictionary
    output_dict = {}
    
    # Define a recursive function to flatten the input dictionary
    def flatten(x, name=()):
        # If the input is a dictionary
        if isinstance(x, collections.abc.Mapping):
            # Iterate through the dictionary
            for k, v in x.items():
                # Recursively call the function on the value of the current key
                flatten(v, name + (k,))
                # flatten(x[a], name + a + '_')
        # If the input is a list
        elif isinstance(x, collections.abc.Sequence) and not isinstance(x, str):
            # Iterate through the list
            for i, v in enumerate(x):
                # Recursively call the function on the current element
                flatten(v, name + (i,))
                # flatten(a, name + str(i) + '_')
        # If the input is not a dictionary
        else:
            # Add the key-value pair to the output dictionary
            # raise NotImplementedError(x, name)
            output_dict[name] = x
            # output_dict[name[:-1]] = x
    
    # Call the recursive function on the input dictionary
    flatten(input_dict)
    
    # Return the output dictionary
    return output_dict
