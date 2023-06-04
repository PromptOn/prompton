from server.tests.endpoints.users.user_post_test_spec import (
    test_db_data,
    test_specs_post,
)

from server.tests.endpoints.test_generators.post_test_genarator import (
    generate_pytest_post,
)


test_users_post = generate_pytest_post(
    "/users",
    test_db_data,
    "users",
    test_specs_post,
    additional_fixture_names=["mock_get_hashed_password"],
)
