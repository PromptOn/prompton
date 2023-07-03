from pymongo.results import InsertOneResult

from src.core.database import Db
from src.crud.base import CrudBase
from src.schemas.base import NonEmptyStrField, PyObjectId
from src.schemas.user import (
    UserInDB,
    UserCreate,
    UserRoles,
    UserUpdate,
    Token,
    OauthUserInfo,
)

import src.core.auth as auth
from src.crud.org import org_crud
from src.endpoints.endpoint_exceptions import (
    InvalidUserNameOrPassword,
    NoOrgMatchForOAuthUserDomain,
)


class UserCRUD(CrudBase[UserInDB, UserCreate, UserUpdate]):
    async def get_token(self, db, email: str, plain_password: str) -> Token:
        user = await self.authenticate_user(db, email, plain_password)

        if not user:
            raise InvalidUserNameOrPassword

        # TODO: add user: prefix to sub
        access_token = auth.create_access_token(data={"sub": user.email})

        token = Token(access_token=access_token, token_type="bearer")

        return token

    async def authenticate_user(self, db: Db, email: str, password: str):
        user = await self.find_one(db, {"email": email})

        if not user or not auth.verify_password(password, user.hashed_password):
            return False
        return user

    async def get_token_after_oauth(self, db, userInfo: OauthUserInfo) -> Token:
        """Assuming user already authenticated with google and we have his email
        Returns token if useremail already exists
        If user doesn't exists it creates the email domain part is matching an orgs.google_auth_domain
        """
        domain = userInfo.email.split("@")[1]

        user = await self.find_one(db, {"email": userInfo.email})
        if not user:
            org = await org_crud.find_one(db, {"oauth_domain": domain})
            if not org:
                raise NoOrgMatchForOAuthUserDomain(oAuthDomain=domain)

            full_name = NonEmptyStrField(
                userInfo.name if userInfo.name else userInfo.email.split("@")[0]
            )

            user = UserInDB(
                email=userInfo.email,
                org_id=org.id,
                created_by_user_id=PyObjectId("111111111111111111111111"),
                created_by_org_id=org.id,
                full_name=full_name,
                hashed_password="google oauth",
                disabled=False,
                role=UserRoles.BASIC,  # TODO: user feedbackonly role as default
            )

            user_in_db_raw = user.dict(by_alias=True, exclude_unset=False)

            _ = await db[self.collection].insert_one(user_in_db_raw)

        access_token = auth.create_access_token(data={"sub": userInfo.email})

        return Token(access_token=access_token, token_type="bearer")

    async def create(
        self, db, obj_in: UserCreate, current_user: UserInDB
    ) -> InsertOneResult:
        await org_crud.assert_item_exists(db, obj_in.org_id, current_user=current_user)

        user_data = obj_in.dict(by_alias=True, exclude_unset=True)
        user_data.pop("plain_password")
        user_data["hashed_password"] = auth.get_hashed_password(obj_in.plain_password)

        user_in_db = UserInDB(**user_data)

        user_in_db_raw = user_in_db.dict(by_alias=True, exclude_unset=False)

        insert_result = await super().create_from_raw(db, user_in_db_raw, current_user)

        return insert_result


user_crud = UserCRUD(
    db_schema=UserInDB, collection="users", org_id_check_field_name="org_id"
)
