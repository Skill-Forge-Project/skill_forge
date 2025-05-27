import React, { useState } from 'react';
import Modal from "../Layout/Modal";

const NewBoss = () => {
  const UNDERWORLD_API_URL = import.meta.env.VITE_UNDERWORLD_SERVICE_URL;
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMessage, setModalMessage] = useState("");

  const [formData, setFormData] = useState({
    boss_name: '',
    boss_title: '',
    boss_language: '',
    boss_specialty: '',
    boss_difficulty: 'Easy',
    boss_description: ''
  });

  const difficulties = ['Easy', 'Medium', 'Hard'];

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
      const response = await fetch(`${UNDERWORLD_API_URL}/bosses`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          boss_name: formData.boss_name,
          boss_title: formData.boss_title,
          boss_language: formData.boss_language,
          boss_specialty: formData.boss_specialty,
          boss_difficulty: formData.boss_difficulty,
          boss_description: formData.boss_description,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setModalMessage("Boss created successfully!");
        setModalOpen(true);
      } else {
        setModalMessage("Boss creation failed: " + (data.message || "Unknown error"));
        setModalOpen(true);
      }
    } catch (error) {
      setModalMessage("Boss creation failed: " + (data.message || "Unknown error"));
      setModalOpen(true);
    }
  };

  return (
    <div className="mx-auto p-6 rounded-lg shadow primary_object">
      <h2 className="text-2xl font-bold mb-4 text-center">Create New Underworld Boss</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          name="boss_name"
          value={formData.boss_name}
          onChange={handleChange}
          className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:text-white"
          placeholder="Boss Name"
          required
        />
        <input
          type="text"
          name="boss_title"
          value={formData.boss_title}
          onChange={handleChange}
          className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:text-white"
          placeholder="Boss Title"
          required
        />
        <input
          type="text"
          name="boss_language"
          value={formData.boss_language}
          onChange={handleChange}
          className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:text-white"
          placeholder="Boss Language"
          required
        />
        <input
          name="boss_specialty"
          value={formData.boss_specialty}
          onChange={handleChange}
          className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:text-white"
          placeholder="Boss Specialty"
          required
        />
        <select
          name="boss_difficulty"
          value={formData.boss_difficulty}
          onChange={handleChange}
          className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:text-white"
        >
          {difficulties.map((diff) => (
            <option key={diff} value={diff}>{diff}</option>
          ))}
        </select>
        <textarea
          name="boss_description"
          value={formData.boss_description}
          onChange={handleChange}
          className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:text-white"
          placeholder="Boss Description"
          required
          rows={4}
        />
        <button
          type="submit"
          className="w-full p-2 rounded primary_button"
        >
          Create Boss
        </button>
      </form>
      {/* Modal for create new boss */}
      <Modal isOpen={modalOpen} 
        onClose={() => setModalOpen(false)} 
        title="Create New Boss" 
        message={modalMessage} 
      />
    </div>
    
  );
};

export default NewBoss;