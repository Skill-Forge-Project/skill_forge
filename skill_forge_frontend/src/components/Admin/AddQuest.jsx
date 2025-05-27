import React, { useState } from "react";
import "github-markdown-css/github-markdown.css";
import CodeEditor from "../Layout/CodeEditor";

const AddQuest = () => {
  const userId = localStorage.getItem("userId");
  const QUEST_API = import.meta.env.VITE_QUESTS_SERVICE_URL;

  const [formData, setFormData] = useState({
    quest_name: "",
    quest_language: "",
    quest_difficulty: "",
    quest_condition: "",
    quest_inputs: "",
    quest_outputs: "",
    function_template: "",
    quest_unitests: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${QUEST_API}/quests`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          language: formData.quest_language,
          difficulty: formData.quest_difficulty,
          quest_name: formData.quest_name,
          quest_author: userId,
          condition: formData.quest_condition,
          function_template: formData.function_template,
          unit_tests: formData.quest_unitests,
          test_inputs: formData.quest_inputs,
          test_outputs: formData.quest_outputs,
          type: "Basic",
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert("Quest added successfully!");
        console.log("Quest ID:", data.quest_id);
      } else {
        console.error("Error:", data.error);
        alert("Failed to add quest.");
      }
    } catch (error) {
      console.error("Fetch error:", error);
      alert("An error occurred.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="flex flex-col space-y-4 w-full">
        <label
          className="primary_object secondary_text p-2 w-full"
          htmlFor="quest_name"
        >
          Quest Name
        </label>
        <input
          type="text"
          id="quest_name"
          name="quest_name"
          className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:text-white"
          value={formData.quest_name}
          onChange={handleChange}
        />
      </div>

      <div className="flex flex-col space-y-4 w-full">
        <select
          id="quest_language"
          name="quest_language"
          className="primary_object secondary_text p-2 w-full"
          value={formData.quest_language}
          onChange={handleChange}
        >
          <option value="">Select language</option>
          <option value="Python">Python</option>
          <option value="Java">Java</option>
          <option value="CSharp">C#</option>
          <option value="JavaScript">JavaScript</option>
        </select>
      </div>

      <div className="flex flex-col space-y-4 w-full">
        <select
          id="quest_difficulty"
          name="quest_difficulty"
          className="primary_object secondary_text p-2 w-full"
          value={formData.quest_difficulty}
          onChange={handleChange}
        >
          <option value="">Select difficulty</option>
          <option value="Easy">Novice Quests</option>
          <option value="Medium">Adventurous Challenges</option>
          <option value="Hard">Epic Campaigns</option>
        </select>
      </div>

      <div className="flex flex-col space-y-4 w-full">
        <label
          className="primary_object secondary_text p-2 w-full"
          htmlFor="quest_condition"
        >
          Condition
        </label>
        <textarea
          id="quest_condition"
          name="quest_condition"
          className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:text-white"
          rows={15}
          value={formData.quest_condition}
          onChange={handleChange}
        />
      </div>

      <div className="flex flex-col space-y-4 w-full">
        <label
          className="primary_object secondary_text p-2 w-full"
          htmlFor="quest_inputs"
        >
          Inputs
        </label>
        <textarea
          id="quest_inputs"
          name="quest_inputs"
          className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:text-white"
          rows={10}
          value={formData.quest_inputs}
          onChange={handleChange}
        />
      </div>

      <div className="flex flex-col space-y-4 w-full">
        <label
          className="primary_object secondary_text p-2 w-full"
          htmlFor="quest_outputs"
        >
          Outputs
        </label>
        <textarea
          id="quest_outputs"
          name="quest_outputs"
          className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:text-white"
          rows={10}
          value={formData.quest_outputs}
          onChange={handleChange}
        />
      </div>

      <div className="flex flex-col space-y-4 w-full">
        <label
          className="primary_object secondary_text p-2 w-full"
          htmlFor="function_template"
        >
          Function Template
        </label>
        <CodeEditor
          language={formData.quest_language}
          code={formData.function_template}
          onChange={(val) =>
            setFormData((prev) => ({
              ...prev,
              function_template: val,
            }))
          }
        />
      </div>

      <div className="flex flex-col space-y-4 w-full">
        <label
          className="primary_object secondary_text p-2 w-full"
          htmlFor="quest_unitests"
        >
          Example Solution
        </label>
        <CodeEditor
          language={formData.quest_language}
          code={formData.quest_unitests}
          onChange={(val) =>
            setFormData((prev) => ({
              ...prev,
              quest_unitests: val,
            }))
          }
        />
      </div>

      <div className="btn-container">
        <button type="submit" className="primary_button">
          Submit Quest
        </button>
      </div>
    </form>
  );
};

export default AddQuest;