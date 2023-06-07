from server.tests.endpoints.prompts.prompts_get_test_spec import (
    test_db_data,
    test_specs_get,
)

from server.tests.endpoints.test_generators.get_test_genarator import (
    generate_pytest_get,
    generate_pytest_get_empty,
)


test_prompts_get = generate_pytest_get("/prompts", test_db_data, test_specs_get)

test_pronpts_get_empty = generate_pytest_get_empty("/prompts")
