// this ran by the first docker-compose up but only if there is no DB data in the volume yet https://hub.docker.com/_/mongo

console.log(">>>>>>>>>>>>>>> 01_init_db.js s starting ");
db = db.getSiblingDB("admin");
db.auth(
  process.env.MONGO_INITDB_ROOT_USERNAME,
  process.env.MONGO_INITDB_ROOT_PASSWORD
);

db = db.getSiblingDB(process.env.MONGO_DATABASE);

db.log.insertOne({ message: "01_init_db.js : Database created." });

db.createUser({
  user: process.env.MONGO_USER,
  pwd: process.env.MONGO_PASSWORD,
  roles: [
    {
      role: "readWrite",
      db: process.env.MONGO_DATABASE,
    },
  ],
});

db.log.insertOne({
  message: "01_init_db.js : User " + process.env.MONGO_USER + " created.",
});

console.log(
  "<<<<<<<<<<<<< 01_init_db.js finished. " +
    process.env.MONGO_DATABASE +
    " database created"
);
