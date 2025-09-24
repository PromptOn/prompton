from tests.endpoints.feedbacks.feedback_post_test_spec import (
    test_specs_post,
    test_db_data,
)
from tests.endpoints.test_generators.post_test_genarator import generate_pytest_post


test_prompts_post = generate_pytest_post(
    "/feedbacks", test_db_data, "feedbacks", test_specs_post
)
