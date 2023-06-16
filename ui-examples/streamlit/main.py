import streamlit as st

from prompton import client as prompton_client
from prompton import errors as prompton_errors


prompton_env = "http://127.0.0.1:8000/"
# prompton_env = "https://staging.api.prompton.ai/"

st.set_page_config(layout="wide", page_title="Prompton API Example")
prompton = prompton_client.PromptonApi(environment=prompton_env)

if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None

if st.button("Click me"):
    st.success("Success message!")

if not st.session_state["auth_token"]:
    with st.form("Login"):
        st.write("## Prompton Login ")
        st.write(prompton_env)
        email = st.text_input("email", key="email")
        password = st.text_input("Password", type="password", key="password")

        submitted = st.form_submit_button("Login")

        if submitted:
            try:
                with st.spinner("Authenticating..."):
                    token = prompton.authentication.get_access_token(
                        username=email, password=password
                    )

                st.session_state["auth_token"] = token.access_token

                st.experimental_rerun()

            except prompton_errors.UnauthorizedError as e:
                st.error("😕 Login failed: " + str(e.body["detail"]))
            except prompton_errors.BadRequestError as e:
                st.error("😕 Bad request: " + str(e.body))
            except prompton_errors.UnprocessableEntityError as e:
                st.error("😕 Unprocessable entity: " + str(e.body))

            except Exception as e:
                st.error("😕 Error while trying to login: " + str(e))

if st.session_state["auth_token"]:
    prompton = prompton_client.PromptonApi(
        environment=prompton_env, token=st.session_state["auth_token"]
    )

    my_org = prompton.orgs.get_current_user_org()
    my_user = prompton.users.get_current_user()
    my_role = my_user.role.value if my_user.role else "No role"

    st.write("# Prompton UI")

    st.write(f"{my_user.email}  @  {my_org.name} ( { my_role} )")

    st.write("## My Prompts")
    with st.spinner("Loading prompts..."):
        my_prompts = prompton.prompts.get_prompts_list()
        st.write(my_prompts)

    st.write("## My Prompt Versions")
    with st.spinner("Loading versions..."):
        my_prompt_versions = prompton.prompt_versions.get_prompt_versions_list()
        st.write(my_prompt_versions)
