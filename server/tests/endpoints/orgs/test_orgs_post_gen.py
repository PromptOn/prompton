from tests.endpoints.orgs.orgs_post_test_spec import test_specs_post

from tests.endpoints.test_generators.post_test_genarator import (
    generate_pytest_post,
)


test_orgs_post = generate_pytest_post("/orgs", None, "orgs", test_specs_post)
