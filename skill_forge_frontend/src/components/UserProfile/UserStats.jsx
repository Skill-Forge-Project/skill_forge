import React from "react";
import { format } from "date-fns";

const UserStats = ( {user} ) => {
  if (!user) return null;
  console.log("User " + user.first_name);
  const formatDate = (dateString) => {
    if (!dateString) return 'Invalid date';

    try {
      return format(new Date(dateString), 'dd-MM-yyyy HH:mm');
    } catch (err) {
      console.error('Invalid date:', err);
      return '';
    }
  };


  return (
    <div className="shadow rounded-lg p-6 mt-8 primary_object">
      <h2 className="text-xl font-bold mb-4 primary_text">My Stats</h2>
      <div className="space-y-1 secondary_text">
        <div className="flex justify-between">
          <p className="">Date Registration:</p>
          <p className="">{formatDate(user.registration_date)}</p>
        </div>
        <hr style={{ backgroundColor: "white", margin: 0 }} />

        <div className="flex justify-between">
          <p className="">Total Solved Quests:</p>
          <p className="">{user.total_solved_quests}</p>
        </div>
        <hr style={{ backgroundColor: "white", margin: 0 }} />

        <div className="pl-4">
          <div className="flex justify-between">
            <p className="">Python:</p>
            <p className="">{user.total_python_quests}</p>
          </div>
          <hr style={{ backgroundColor: "white", margin: 0 }} />

          <div className="flex justify-between">
            <p className="">Java:</p>
            <p className="">{user.total_java_quests}</p>
          </div>
          <hr style={{ backgroundColor: "white", margin: 0 }} />

          <div className="flex justify-between">
            <p className="">JavaScript:</p>
            <p className="">{user.total_javascript_quests}</p>
          </div>
          <hr style={{ backgroundColor: "white", margin: 0 }} />

          <div className="flex justify-between">
            <p className="">C# Quests:</p>
            <p className="">{user.total_csharp_quests}</p>
          </div>
          <hr style={{ backgroundColor: "white", margin: 0 }} />
        </div>

        <div className="flex justify-between">
          <p className="">Total Submitted Quests:</p>
          <p className="">{user.total_submited_quests}</p>
        </div>
        <hr style={{ backgroundColor: "white", margin: 0 }} />

        <div className="pl-4">
          <div className="flex justify-between">
            <p className="">Approved:</p>
            <p className="">{user.total_approved_submited_quests}</p>
          </div>
          <hr style={{ backgroundColor: "white", margin: 0 }} />

          <div className="flex justify-between">
            <p className="">Rejected:</p>
            <p className="">{user.total_rejected_submited_quests}</p>
          </div>
          <hr style={{ backgroundColor: "white", margin: 0 }} />
        </div>
      </div>
    </div>
  );
};

export default UserStats;