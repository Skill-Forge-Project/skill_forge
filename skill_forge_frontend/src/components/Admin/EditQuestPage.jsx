import React, { useEffect, useState } from "react";
import { editQuestById } from "../../services/questsServices";
import CodeEditor from "../Layout/CodeEditor";
import Modal from "../Layout/Modal";


const EditQuestPage = ({ questId, onBack }) => {
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

  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMessage, setModalMessage] = useState("");
  const userId = localStorage.getItem("user_id");
  const token = localStorage.getItem("token");
  const QUESTS_API = import.meta.env.VITE_QUESTS_SERVICE_URL;

  useEffect(() => {
    const fetchQuest = async () => {
      try {
        const data = await editQuestById(questId); // should return the quest by ID
        setFormData({
          quest_name: data.quest_name || "",
          quest_language: data.language || "",
          quest_difficulty: data.difficulty || "",
          quest_condition: data.condition || "",
          quest_inputs: data.test_inputs || "",
          quest_outputs: data.test_outputs || "",
          function_template: data.function_template || "",
          quest_unitests: data.unit_tests || "",
        });
      } catch (error) {
        console.error("Error fetching quest:", error);
        setMessage("Failed to load quest.");
      } finally {
        setLoading(false);
      }
    };

    fetchQuest();
  }, [questId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const response = await fetch(`${QUESTS_API}/quests/${questId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
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
        setModalMessage("Quest updated successfully!");
        setModalOpen(true);
        // alert("Quest updated successfully!");
        // console.log("Updated Quest ID:", data.quest_id);
      } else {
        setModalMessage("Failed to update quest.");
        setModalOpen(true);
        // console.error("Error:", data.error);
        // alert("Failed to update quest.");
      }
    } catch (error) {
      setModalMessage("An error occurred.");
      setModalOpen(true);
      // console.error("Fetch error:", error);
      // alert("An error occurred.");
    }
    setSubmitting(false);
  };

  if (loading) return <div>Loading quest...</div>;

  return (
    <div className="space-y-4">
      <button onClick={onBack} className="px-4 py-2 rounded primary_button">
        ← Back to Quests
      </button>

      <h2 className="text-xl font-bold primary_text">
        Editing Quest: {formData.quest_name}
      </h2>

      <form
        onSubmit={handleSubmit}
        className="mx-auto min-h-screen p-10 primary_object"
      >
        <div className="mb-4">
          <label className="block mb-2">Quest Name:</label>
          <input
            type="text"
            name="quest_name"
            value={formData.quest_name}
            onChange={handleChange}
            className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
        </div>

        <div className="mb-4">
          <label className="block mb-2">Language:</label>
          <select
            name="quest_language"
            value={formData.quest_language}
            onChange={handleChange}
            className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          >
            <option value="Python">Python</option>
            <option value="Java">Java</option>
            <option value="CSharp">C#</option>
            <option value="JavaScript">JavaScript</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block mb-2">Difficulty:</label>
          <select
            name="quest_difficulty"
            value={formData.quest_difficulty}
            onChange={handleChange}
            className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          >
            <option value="Easy">Novice Quests</option>
            <option value="Medium">Adventurous Challenges</option>
            <option value="Hard">Epic Campaigns</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block mb-2">Condition:</label>
          <textarea
            name="quest_condition"
            value={formData.quest_condition}
            onChange={handleChange}
            className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            rows={15}
          />
        </div>

        <div className="mb-4">
          <label className="block mb-2">Function Template:</label>
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

        <div className="mb-4">
          <label className="block mb-2">Test Inputs:</label>
          <textarea
            name="quest_inputs"
            value={formData.quest_inputs}
            onChange={handleChange}
            className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            rows={10}
          />
        </div>

        <div className="mb-4">
          <label className="block mb-2">Expected Outputs:</label>
          <textarea
            name="quest_outputs"
            value={formData.quest_outputs}
            onChange={handleChange}
            className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            rows={10}
          />
        </div>

        <div className="mb-4">
          <label className="block mb-2">Example Solution:</label>
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

        <button type="submit" className="px-4 py-2 rounded primary_button">
          Update Quest
        </button>

        {message && <p className="mt-4">{message}</p>}
      </form>

      {/* Modal for Quest Edit Page */}
      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Edit Quest" message={modalMessage} />
    </div>
  );
};

export default EditQuestPage;