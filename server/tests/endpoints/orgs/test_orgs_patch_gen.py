from server.tests.endpoints.orgs.orgs_patch_test_spec import (
    test_db_data,
    test_specs_patch,
)
from server.tests.endpoints.test_generators.patch_test_genarator import (
    generate_pytest_patch,
)


test_orgs_patch = generate_pytest_patch("/orgs", test_db_data, "orgs", test_specs_patch)
