import React from "react";

const LoadingSpinner = ({ message }) => {
  return (
    <div className="flex items-center justify-center min-h-screen underworld_boss_container">
      <div className="text-center underworld_primary_text">
        <div className="w-16 h-16 border-4 border-red-400 border-dashed rounded-full animate-spin mx-auto mb-4"></div>
        <p className="font-semibold underworld_primary_text">{message}</p>
      </div>
    </div>
  );
};

export default LoadingSpinner;