# Great Expectations Tips

- If during the run of datasource_new Jupyter notebook, you get an error that 'module_name' must not be None, then you need to add a module_name key to the config YAML file, under the execution_engine key, and set it to 'great_expectations.execution_engine'.
- On Windows, when generating the expectations and/or running the expectations, you may encounter a 'file not found' error; this could be the result of the path length being too long.
- On Windows, in the datasource_new notebook, the test_yaml_config function can fail if the backslashes in the path are not escaped properly.
