from server.tests.endpoints.promptVersions.promptVersions_patch_test_spec import (
    test_db_data,
    test_specs_patch,
)

from server.tests.endpoints.test_generators.patch_test_genarator import (
    generate_pytest_patch,
)


test_promptVersions_patch = generate_pytest_patch(
    "/promptVersions", test_db_data, "promptVersions", test_specs_patch
)
