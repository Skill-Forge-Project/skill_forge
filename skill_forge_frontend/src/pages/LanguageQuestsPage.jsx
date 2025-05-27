import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import QuestsTable  from "../components/Quests/QuestsTable";
import Navbar from "../components/Layout/Navbar";
import { getQuestsByLanguage } from "../services/questsServices";

const QuestsPage = () => {
  const { language } = useParams(); // get language from URL
  const [quests, setQuests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchQuests = async () => {
      try {
        const questsData = await getQuestsByLanguage(language);
        setQuests(questsData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchQuests();
  }, [language]);

  return (
    <>
      <Navbar />
      <div className="mx-auto min-h-screen p-10 bg-gradient-to-b from-[#141e30] to-[#123556] text-white">
        <QuestsTable mode="view" quests={quests} />
      </div>
    </>
  );
};

export default QuestsPage;
