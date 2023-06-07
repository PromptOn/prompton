from server.tests.endpoints.inferences.inferences_get_test_spec import (
    inferences_get_test_db,
    test_spec_get as inferences_test_spec_get,
)
from server.tests.endpoints.test_generators.get_test_genarator import (
    generate_pytest_get,
    generate_pytest_get_empty,
)


test_inferences_get = generate_pytest_get(
    "/inferences", inferences_get_test_db, inferences_test_spec_get
)

test_inferences_get_empty = generate_pytest_get_empty("/inferences")
