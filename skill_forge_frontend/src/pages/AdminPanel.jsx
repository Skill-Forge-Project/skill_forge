import React, {useState, useEffect} from "react";
import Navbar from "../components/Layout/Navbar";
import { getAllQuests } from "../services/questsServices";


// Admin Dashboard Components
import Dashboard from "../components/Admin/Dashboard";
import AddQuest from "../components/Admin/AddQuest";
import EditQuest from "../components/Admin/EditQuest";
import NewBoss from "../components/Admin/NewBoss";
import QuestsLogs from "../components/Admin/QuestsLogs";

const AdminPanel = () => {
  const [activeSection, setActiveSection] = useState("dashboard");
  const [quests, setQuests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");



  const renderSection = () => {
    // if (loading) return <p>Loading quests...</p>;
    // if (error) return <p className="text-red-500">{error}</p>;

    switch (activeSection) {
      case "add_quest":
        return <AddQuest />;
      case "edit_quest":
        return <EditQuest />;
      case "underworld_boss":
        return <NewBoss />;
      case "quests_logs":
        return <QuestsLogs />;
      case "dashboard":
      default:
        return <Dashboard />;
    }
  };

  return (
    <>
      <Navbar />
      <div className="min-h-screen flex bg-gradient-to-b from-[#141e30] to-[#123556] text-white">
        {/* Sidebar */}
        <aside className="w-64 shadow-md">
          <div className="p-6 text-xl font-bold border-b primary_text">
            Admin Panel
          </div>
          <nav className="mt-6">
            <ul className="space-y-2 px-2">
            <li>
                <button
                  onClick={() => setActiveSection("dashboard")}
                  className="w-full text-left py-2 px-4 rounded primary_button"
                >
                  Dashboard
                </button>
              </li>
              <li>
                <button
                  onClick={() => setActiveSection("add_quest")}
                  className="w-full text-left py-2 px-4 rounded primary_button"
                >
                  Add Quest
                </button>
              </li>
              <li>
                <button
                  onClick={() => setActiveSection("edit_quest")}
                  className="w-full text-left py-2 px-4 rounded primary_button"
                >
                  Edit Quest
                </button>
              </li>
              <li>
                <button
                  onClick={() => setActiveSection("underworld_boss")}
                  className="w-full text-left py-2 px-4 rounded primary_button"
                >
                  Create New Underworld Boss
                </button>
              </li>
              <li>
                <button
                  onClick={() => setActiveSection("quests_logs")}
                  className="w-full text-left py-2 px-4 rounded primary_button"
                >
                  Quests Logs
                </button>
              </li>
            </ul>
          </nav>
        </aside>
        {/* Main Content */}
        <main className="flex-1 p-10 shadow-2xl">
          <div className="container mx-auto">
            {renderSection()}
          </div>
        </main>
        </div>
    </>
  );
};

export default AdminPanel;
