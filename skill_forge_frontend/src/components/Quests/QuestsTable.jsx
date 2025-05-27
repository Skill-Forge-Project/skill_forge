import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import { getCorrectSolutionsByUserId } from "../../services/questsServices";

const QuestsTable = ({ quests, mode, onQuestClick }) => {

  const userId = localStorage.getItem("userId");
  const [difficultyFilter, setDifficultyFilter] = useState("All");
  const [solvedFilter, setSolvedFilter] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [solvedQuests, setSolvedQuests] = useState([]);

  useEffect(() => {
    const fetchSolvedQuests = async () => {
      try {
        const solved = await getCorrectSolutionsByUserId(userId); // Fetch solved quests by user ID
        const solvedQuests = solved.map((s) => s.quest_id);
        setSolvedQuests(solvedQuests);
      } catch (err) {
        console.error("Failed to fetch solved quests", err);
      }
    };
    fetchSolvedQuests();
  }, [userId]);

  const filteredQuests = quests
    .map((quest) => ({
      ...quest,
      is_solved: solvedQuests.includes(quest.id)
    }))
    .filter((quest) => {
      const matchesDifficulty =
        difficultyFilter === "All" || quest.difficulty === difficultyFilter;

      const matchesSolved =
        solvedFilter === "All" ||
        (solvedFilter === "Solved" && quest.is_solved) ||
        (solvedFilter === "Unsolved" && !quest.is_solved);

      const query = searchQuery.toLowerCase();
      const matchesSearch =
        quest.quest_name.toLowerCase().includes(query) ||
        quest.difficulty.toLowerCase().includes(query) ||
        quest.quest_author.toLowerCase().includes(query);

      return matchesDifficulty && matchesSolved && matchesSearch;
    });

  return (
    <div className="antialiased font-sans bg-gray-200 w-full px-4 sm:px-8 primary_object">
      <div className="py-8">
        <div>
          <h2 className="text-2xl font-semibold leading-tight">Quests</h2>
        </div>

        {/* Filter and search controls */}
        <div className="my-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex flex-row gap-2">
            <select
              value={difficultyFilter}
              onChange={(e) => setDifficultyFilter(e.target.value)}
              className="rounded border py-2 px-4 text-sm focus:outline-none"
            >
              <option>All</option>
              <option>Novice Quests</option>
              <option>Adventurous Challenges</option>
              <option>Epic Campaigns</option>
            </select>

            <select
              value={solvedFilter}
              onChange={(e) => setSolvedFilter(e.target.value)}
              className="rounded border py-2 px-4 text-sm focus:outline-none"
            >
              <option>All</option>
              <option>Solved</option>
              <option>Unsolved</option>
            </select>
          </div>
          <div className="relative w-full sm:w-1/3">
            <span className="absolute inset-y-0 left-0 pl-2 flex items-center">
              <svg viewBox="0 0 24 24" className="h-4 w-4 fill-current">
                <path d="M10 4a6 6 0 100 12 6 6 0 000-12zm-8 6a8 8 0 1114.32 4.906l5.387 5.387a1 1 0 01-1.414 1.414l-5.387-5.387A8 8 0 012 10z" />
              </svg>
            </span>
            <input
              type="text"
              placeholder="Search"
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-8 pr-4 py-2 border text-sm rounded w-full focus:outline-none"
            />
          </div>
        </div>

        {/* Table */}
        <div className="-mx-4 sm:-mx-8 px-4 sm:px-8 py-4 overflow-x-auto">
          <div className="inline-block min-w-full shadow rounded-lg overflow-hidden">
            <table className="min-w-full leading-normal">
              <thead className="primary_object">
                <tr>
                  <th className="px-5 py-3 border-b-2 text-left text-xs font-semibold uppercase tracking-wider">
                    Quest
                  </th>
                  <th className="px-5 py-3 border-b-2 text-left text-xs font-semibold uppercase tracking-wider">
                    Difficulty
                  </th>
                  <th className="px-5 py-3 border-b-2 text-left text-xs font-semibold uppercase tracking-wider">
                    Author
                  </th>
                  <th className="px-5 py-3 border-b-2 text-left text-xs font-semibold uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody>
                {filteredQuests.length > 0 ? (
                  filteredQuests.map((quest) => (
                    <tr key={quest.quest_id}>
                      <td className="px-5 py-5 border-b text-sm">
                        <div className="flex items-center">
                          <div className="ml-3">
                            {mode === "edit" ? (
                              <span
                                className="text-blue-500 font-medium hover:underline cursor-pointer"
                                onClick={() => onQuestClick(quest.id)}
                              >
                                {quest.quest_name}
                              </span>
                            ) : (
                              <Link
                                to={`/quest/${quest.id}`}
                                className="text-blue-500 font-medium hover:underline"
                              >
                                {quest.quest_name}
                              </Link>
                            )}
                          </div>
                        </div>
                      </td>
                      <td className="px-5 py-5 border-b text-sm capitalize">
                        {quest.difficulty}
                      </td>
                      <td className="px-5 py-5 border-b text-sm">
                        <Link
                          to={`/profile/${quest.quest_author}`}
                          className="text-blue-500 hover:underline"
                        >
                          {quest.quest_author}
                        </Link>
                      </td>
                      <td className="px-5 py-5 border-b text-sm">
                        {quest.is_solved ? (
                          <span className="relative inline-block px-3 py-1 font-semibold text-green-900 leading-tight">
                            <span className="absolute inset-0 bg-green-200 opacity-60 rounded-full"></span>
                            <span className="relative">Solved</span>
                          </span>
                        ) : (
                          <span className="relative inline-block px-3 py-1 font-semibold text-red-900 leading-tight">
                            <span className="absolute inset-0 bg-red-200 opacity-60 rounded-full"></span>
                            <span className="relative">Unsolved</span>
                          </span>
                        )}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="text-center py-4">
                      No quests match the filter.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuestsTable;
