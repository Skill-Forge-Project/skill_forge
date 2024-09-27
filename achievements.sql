-- achievements.sql

-- Create the achievements table
CREATE TABLE achievements (
    achievement_id VARCHAR(20) PRIMARY KEY,
    achievement_name VARCHAR(50) NOT NULL,
    achievement_description VARCHAR(255) NOT NULL,
    achievement_picture VARCHAR(255) NOT NULL,
    "language" VARCHAR(50) NOT NULL,
    quests_number_required INTEGER NOT NULL
);

-- Create achivements table and insert some data
INSERT INTO achievements (achievement_id,achievement_name,achievement_description,achievement_picture,"language",quests_number_required) VALUES
	 ('ACH-JS-001','JavaScript Novice Mage','Solve 10 JavaScript Quests','JavaScript/javascript-1.png','JavaScript',10),
	 ('ACH-JS-002','JavaScript Adept Enchanter','Solve 20 JavaScript Quests','JavaScript/javascript-2.png','JavaScript',20),
	 ('ACH-JS-003','JavaScript Skilled Sorcerer','Solve 40 JavaScript Quests','JavaScript/javascript-3.png','JavaScript',40),
	 ('ACH-JS-004','JavaScript Master Wizard','Solve 60 JavaScript Quests','JavaScript/javascript-4.png','JavaScript',60),
	 ('ACH-JS-005','JavaScript Archmage','Solve 80 JavaScript Quests','JavaScript/javascript-5.png','JavaScript',80),
	 ('ACH-JS-006','JavaScript Legendary Hero','Solve 100 JavaScript Quests','JavaScript/javascript-6.png','JavaScript',100),
	 ('ACH-PY-001','Python Apprentice','Solve 10 Python Quests','Python/python-1.png','Python',10),
	 ('ACH-PY-002','Python Spellcaster','Solve 20 Python Quests','Python/python-2.png','Python',20),
	 ('ACH-PY-003','Python Rune Scribe','Solve 40 Python Quests','Python/python-3.png','Python',40),
	 ('ACH-PY-004','Python Arcane Adept','Solve 60 Python Quests','Python/python-4.png','Python',60);
INSERT INTO achievements (achievement_id,achievement_name,achievement_description,achievement_picture,"language",quests_number_required) VALUES
	 ('ACH-PY-005','Python Mystic Sage','Solve 80 Python Quests','Python/python-5.png','Python',80),
	 ('ACH-PY-006','Python High Sorcerer','Solve 100 Python Quests','Python/python-6.png','Python',100),
	 ('ACH-JV-001','Java Novice','Solve 10 Java Quests','Java/java-1.png','Java',10),
	 ('ACH-JV-002','Java Initiate','Solve 20 Java Quests','Java/java-2.png','Java',20),
	 ('ACH-JV-003','Java Enchanter','Solve 40 Java Quests','Java/java-3.png','Java',40),
	 ('ACH-JV-004','Java Conjurer','Solve 60 Java Quests','Java/java-4.png','Java',60),
	 ('ACH-JV-005','Java Sorcerer','Solve 80 Java Quests','Java/java-5.png','Java',80),
	 ('ACH-JV-006','Java Archmage','Solve 100 Java Quests','Java/java-6.png','Java',100),
	 ('ACH-CS-001','C# Apprentice','Solve 10 C# Quests','CS/cs-1.png','C#',10),
	 ('ACH-CS-002','C# Adept','Solve 20 C# Quests','CS/cs-1.png','C#',20);
INSERT INTO achievements (achievement_id,achievement_name,achievement_description,achievement_picture,"language",quests_number_required) VALUES
	 ('ACH-CS-003','C# Spellcaster','Solve 40 C# Quests','CS/cs-1.png','C#',40),
	 ('ACH-CS-004','C# Mystic','Solve 60 C# Quests','CS/cs-1.png','C#',60),
	 ('ACH-CS-005','C# Sorcerer','Solve 80 C# Quests','CS/cs-1.png','C#',80),
	 ('ACH-CS-006','C# Grand Enchanter','Solve 100 C# Quests','CS/cs-1.png','C#',100),
	 ('ACH-GEN-001','Skill Forge Contributor','Successfully Submited a Quest','General/quest_approved.png','General',1),
	 ('ACH-GEN-002','Early Bird','Thanks for joining us early!','General/early_bird.png','General',1);
