use admin
db.createUser(
  {
    user: "admin1",
    pwd: "password",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
)
