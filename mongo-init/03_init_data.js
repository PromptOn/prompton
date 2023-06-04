db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);
db.auth(process.env.MONGO_USER, process.env.MONGO_PASSWORD);

org = {
  created_at: new Date(),
  created_by_user_id: "000000000000000000000000",
  name: process.env.PROMPTON_ORG_NAME,
  access_keys: { "openai-api-key": process.env.PROMPTON_ORG_OPENAI_API_KEY },
};

res = db.orgs.insertOne(org);

user = {
  created_at: new Date(),
  created_by_user_id: "000000000000000000000000",
  org_id: res.insertedId,
  email: process.env.PROMPTON_USER_EMAIL,
  hashed_password: process.env.PROMPTON_USER_PASSWORD_HASH,
};

db.users.insertOne(user);
