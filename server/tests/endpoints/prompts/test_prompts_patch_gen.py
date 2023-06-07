from server.tests.endpoints.prompts.prompts_patch_test_spec import (
    test_specs_patch,
    test_db_data,
)
from server.tests.endpoints.test_generators.patch_test_genarator import (
    generate_pytest_patch,
)


test_prompts_patch = generate_pytest_patch(
    "/prompts", test_db_data, "prompts", test_specs_patch
)
