from tests.endpoints.token.token_post_test_spec import (
    test_db_data,
    test_specs_token_post,
    test_specs_token_basic_post,
)

from tests.endpoints.test_generators.post_test_genarator import generate_pytest_post


test_token_post = generate_pytest_post(
    "/token", test_db_data, None, test_specs_token_post
)

test_token_basic_post = generate_pytest_post(
    "/token_basic", test_db_data, None, test_specs_token_basic_post
)
