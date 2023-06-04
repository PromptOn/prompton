from server.tests.endpoints.prompts.prompts_post_test_spec import (
    test_specs_post,
)
from server.tests.endpoints.test_generators.post_test_genarator import (
    generate_pytest_post,
)


test_prompts_post = generate_pytest_post("/prompts", None, "prompts", test_specs_post)
