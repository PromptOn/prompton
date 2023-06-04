from inferences_post_test_spec import (
    test_specs_post,
    test_db_data,
)

from server.tests.endpoints.test_generators.post_test_genarator import (
    generate_pytest_post,
)


test_inferences_post = generate_pytest_post(
    "/inferences",
    test_db_data,
    "inferences",
    test_specs_post,
    additional_fixture_names=["mock_openai"],
)
