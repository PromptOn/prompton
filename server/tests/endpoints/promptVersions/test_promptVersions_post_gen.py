from tests.endpoints.promptVersions.promptVersions_post_test_spec import (
    test_specs_post,
    test_db_data,
)

from tests.endpoints.test_generators.post_test_genarator import (
    generate_pytest_post,
)


test_promptVersions_post = generate_pytest_post(
    "/promptVersions", test_db_data, "promptVersions", test_specs_post
)
