from tests.endpoints.feedbacks.feedback_get_test_spec import (
    test_db_data,
    feedbacks_get_test_spec,
)

from tests.endpoints.test_generators.get_test_genarator import (
    generate_pytest_get,
    generate_pytest_get_empty,
)


test_promptVersions_get = generate_pytest_get(
    "/feedbacks", test_db_data, feedbacks_get_test_spec
)

test_pronptVersions_get_empty = generate_pytest_get_empty("/feedbacks")
