db = db.getSiblingDB('skill_forge_logs'); // Switch to the 'skill_forge_logs' database

db.createUser({
  user: "skill_forge",
  pwd: "skill_forge",  // Password for the new user
  roles: [
    {
      role: "readWrite",          // Assign readWrite role
      db: "skill_forge_logs"      // For the 'skill_forge_logs' database
    }
  ]
});