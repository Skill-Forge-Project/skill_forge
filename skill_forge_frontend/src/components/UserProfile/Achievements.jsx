// Achievements.js
import React from 'react';

const Achievements = ({ achievements }) => {
  return (
    <div className="mt-4 p-6 bg-white rounded-lg shadow-md primary_object">
      <h3 className="text-2xl font-semibold">Achievements</h3>
      <div className="mt-4 grid grid-cols-3 gap-4">
          <div
            key="{index}"
            className="p-4 border rounded-lg shadow-md bg-gray-100 text-center"
          >
            <h4 className="font-semibold">Name</h4>
            <p>Description</p>
          </div>
      </div>
    </div>
  );
};

export default Achievements;