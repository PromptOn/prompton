console.log(">>>>>>>>>>>>>>> 02_indexes.js starting ");

db = db.getSiblingDB(process.env.MONGO_DATABASE);
db.auth(process.env.MONGO_USER, process.env.MONGO_PASSWORD);

db.users.createIndex({ email: 1 }, { unique: true });

db.users.createIndex({ created_by_org_id: 1 });
db.orgs.createIndex({ created_by_org_id: 1 });
db.prompts.createIndex({ created_by_org_id: 1 });
db.promptVersions.createIndex({ created_by_org_id: 1 });
db.inferences.createIndex({ created_by_org_id: 1 });

db.promptVersions.createIndex({ prompt_id: 1 });

db.inferences.createIndex({ prompt_id: 1 });
db.inferences.createIndex({ prompt_version_id: 1 });
db.inferences.createIndex({ end_user_id: 1 });
db.inferences.createIndex({ client_ref_id: 1 });

db.feedbacks.createIndex({ inference_id: -1 });
db.feedbacks.createIndex({ prompt_version_id: -1 });
db.feedbacks.createIndex({ created_by_user_id: 1 });
