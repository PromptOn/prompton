from tests.shared_test_data import USER_SUPER_ADMIN
from tests.endpoints.orgs.orgs_get_test_spec import (
    test_db_data,
    test_specs_get,
)

from tests.endpoints.test_generators.get_test_genarator import (
    generate_pytest_get,
    generate_pytest_get_empty,
)


test_orgs_get = generate_pytest_get("/orgs", test_db_data, test_specs_get)

test_orgs_get_empty = generate_pytest_get_empty("/orgs", mock_users=[USER_SUPER_ADMIN])
