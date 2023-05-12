import great_expectations as gx
from great_expectations.core.expectation_validation_result import ExpectationSuiteValidationResult
from great_expectations.data_context.types.resource_identifiers import DataContextKey

def deserialize_validation_results(validation_results: dict) -> ExpectationSuiteValidationResult:
    """Deserialize the validation results from a dictionary read in from a serialized JSON back to a Great Expectations object."""
    context = gx.get_context()
    return context.validations_store.deserialize(validation_results)

def list_keys_validations_keys() -> "list[DataContextKey]":
    """List the keys of the validation results in the store."""
    context = gx.get_context()
    return context.validations_store.list_keys()
