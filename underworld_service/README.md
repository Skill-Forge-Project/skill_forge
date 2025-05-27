## Skill Forge Underworld

The **Underworld Realm** is a microservice designed for the Skill Forge app, where users can challenge AI-powered bosses specializing in various programming languages and topics. Each boss presents a unique coding challenge based on their expertise, difficulty level, and programming language. Users can submit their answers and code to be evaluated.

--- 
## 1. About 📖

- A variety of AI-powered bosses with unique specialties and difficulty levels.
- Randomly generated programming challenges across multiple languages such as Python, Java, JavaScript, and C#.
- Provides real-time question generation and response evaluation.
- Seamless integration with the Skill Forge application.

## 2. Installation 💾

To set up the Underworld Realm microservice locally or on a server, follow these steps:

### Prerequisites

- Python 3.x
- Flask
- PostgreSQL Database Viewer (DBeaver, pgAdmin)
- Virtual Environment (optional but recommended)
- OpenAI TOKEN

## 3. Usage 🛠️

The Underworld Realm microservice is meant to be used as a backend for the Skill Forge platform. It handles the generation of random programming challenges by AI bosses and receives users' answers for assessment.

### Example Workflow:

1. The user selects a boss from the list of available bosses.
2. A challenge is generated, and the user is presented with a problem to solve.
3. The user submits their solution (code and answer).
4. The boss evaluates the submission and provides feedback (using OpenAI).

## 4. Boss Structure 🤖

Each boss has a predefined structure that includes:

- **Name:** The name of the boss.
- **Title:** A subtitle that defines the boss's character or role.
- **Language:** The programming language the boss specializes in (e.g., Java, Python).
- **Difficulty:** The difficulty level of the boss (Easy, Medium, Hard).
- **Specialty:** A programming topic the boss focuses on (e.g., Algorithms, OOP, Functional Programming).
- **Description:** A brief background or flavor text about the boss's personality and expertise.

Example Boss:
```json
{ 
	"boss_name": "NullKnight", 
	"boss_title": "the Defiant", 
	"boss_language": "C#", 
	"boss_difficulty": "Hard", 
	"boss_specialty": "Memory Management & Exception Handling",
	"boss_description": "A powerful wielder of garbage collection  and defensive coding techniques, vanquishing bugs and memory leaks."
}
```

## 5. Contributing 👨‍💻👩‍💻

We welcome contributions to improve the Underworld Realm! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request describing the changes you made.
