import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import ProfilePage from "./pages/Profilepage";
import LanguageQuestsPage from "./pages/LanguageQuestsPage";
import QuestPage from "./pages/QuestPage";
import AdminPanel from "./pages/AdminPanel";
import Navbar from "./components/Layout/Navbar";
import EditQuestPage from "./components/Admin/EditQuestPage";
import UnderworldPage from "./pages/Underworld/Underworld";
import BossChallengePage from "./pages/Underworld/BossChallenge";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        {/* Users Routes */}
        <Route path="/profile" element={<ProfilePage />} />
        {/* Quests Routes */}
        <Route path="/quests/:language" element={<LanguageQuestsPage />} />
        <Route path="/quest/:questId" element={<QuestPage />} />
        {/* Admin Routes */}
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/admin/edit_quest/:questId" element={<EditQuestPage />} />
        {/* Underworld Routes */}
        <Route path="/underworld" element={<UnderworldPage />} />
        <Route path="/underworld/challenge/:bossId" element={<BossChallengePage />} />
      </Routes>
    </BrowserRouter>
  );
}