import React, { use, useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../components/Layout/Navbar";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "github-markdown-css/github-markdown.css";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import CodeEditor from "../components/Layout/CodeEditor";
import { getQuestById } from "../services/questsServices";
import { getUserById } from "../services/usersService";

const QuestPage = () => {
  const { questId } = useParams();
  const [user, setUser] = useState(null);
  const [quest, setQuest] = useState(null);
  const [avatarUrl, setAvatarUrl] = useState(null);
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMessage, setModalMessage] = useState("");
  const [editorInstance, setEditorInstance] = useState(null);
  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState("# Write your code here");
  const [executionResults, setExecutionResults] = useState(null);
  const [cooldown, setCooldown] = useState(0);

  const userId = localStorage.getItem("userId");
  const token = localStorage.getItem("token");
  const USER_API = import.meta.env.VITE_USERS_SERVICE_URL;
  const QUEST_API = import.meta.env.VITE_QUESTS_SERVICE_URL;

  // Fetch quest data
  useEffect(() => {
    const fetchQuest = async () => {
      try {
        const questData = await getQuestById(questId);
        setQuest(questData);
      } catch (err) {
        console.error("Error fetching quest:", err.message);
      }
    };

    fetchQuest();
  }, [questId, editorInstance]);

  // Fetch user data
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userData = await getUserById(userId);
        setUser(userData);
      } catch (err) {
        console.error("Error fetching user data:", err.message);
      }
    };

    const fetchAvatarUrl = async () => {
      try {
        const response = await fetch(`${USER_API}/users/${userId}/avatar`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch avatar");
        }

        // Convert blob to object URL
        const imageBlob = await response.blob();
        const imageObjectUrl = URL.createObjectURL(imageBlob);
        setAvatarUrl(imageObjectUrl);
      } catch (err) {
        console.error("Error fetching avatar URL:", err.message);
      }
    };

    if (userId && token) {
      fetchUserData();
      fetchAvatarUrl();
    }
  }, [USER_API, userId, token]);

  // Handle loading all the comments
  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await fetch(`${QUEST_API}/comments/${questId}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error("Failed to fetch comments");
        }
        const data = await response.json();
        setComments(data);
      } catch (error) {
        console.error("Error fetching comments:", error);
      }
    };
    fetchComments();
  }, [QUEST_API, questId, token]);

  // Handle comment submission
  const handleCommentSubmit = () => {
    if (!comment.trim()) {
      alert("Please write a comment before submitting.");
      return;
    }
    const data = {
      quest_id: questId,
      user_id: userId,
      comment: comment,
    };
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    };
    fetch(`${QUEST_API}/comments/${questId}`, options)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to submit quest");
        }
        return response.json();
      })
      .then((data) => {

        // console.log("Quest submitted successfully:", data);
        window.location.reload(); 
      })
      .catch((error) => {
        // console.error("Error submitting quest:", error);
        alert("Error submitting quest. Please try again.");
      });
  };

  // Handle quest submission
  const handleSubmit = () => {
    if (!code.trim()) {
      alert("Please write a solution before submitting.");
      return;
    }
    const data = {
      quest_id: questId,
      user_id: userId,
      language: language,
      code: code,
      difficulty: quest.difficulty,
    };

    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    };
    fetch(`${QUEST_API}/submit/${questId}`, options)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to submit quest");
        }
        return response.json();
      })
      .then((data) => {
        // console.log("Quest submitted successfully:", data);
        setCooldown(30);
        setExecutionResults(data);
        // alert("Quest submitted successfully!");
      })
      .catch((error) => {
        // console.error("Error submitting quest:", error);
        alert("Error submitting quest. Please try again.");
      });
  };

  // Handle cooldown
  useEffect(() => {
    if (cooldown === 0) return;
  
    const interval = setInterval(() => {
      setCooldown((prev) => prev - 1);
    }, 1000);
  
    return () => clearInterval(interval); // Cleanup
  }, [cooldown]);

  // Implement the 404 error handling
  if (!quest) return <div className="text-center mt-10">Loading Quest...</div>;

  return (
    <>
      <Navbar />
      <div className="mx-auto min-h-screen p-10 bg-gradient-to-b from-[#141e30] to-[#123556]">
        <div className="container mt-5 mx-auto">
          <h2 className="text-3xl font-bold p-2 primary_object">
            Quest: {quest.quest_name}
          </h2>
          <div className="flex flex-col sm:flex-row gap-5 mt-5 p-2 text-xl primary_object">
            <p>
              <strong className="text-cyan-400">Language:</strong>{" "}
              {quest.language}
            </p>
            <p>
              <strong className="text-cyan-400">Difficulty:</strong>{" "}
              {quest.difficulty}
            </p>
            <p>
              <strong className="text-cyan-400">XP:</strong> {quest.xp}
            </p>
            <p>
              <strong className="text-cyan-400">Author:</strong>{" "}
              <a
                href={`/profile/${quest.quest_author}`}
                className="text-blue-500"
              >
                {quest.quest_author}
              </a>
            </p>
          </div>

          {/* // Quest Description */}
          <div className="mt-3">
            <h4 className="p-2 text-lg primary_object primary_text">
              Task Description:
            </h4>
            <div className="p-2 mt-2 text-l primary_object">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  code({ node, inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || "");
                    return !inline && match ? (
                      <SyntaxHighlighter
                        style={oneDark}
                        language={match[1]}
                        PreTag="div"
                        {...props}
                      >
                        {String(children).replace(/\n$/, "")}
                      </SyntaxHighlighter>
                    ) : (
                      <code
                        className="bg-gray-700 px-1 py-0.5 rounded"
                        {...props}
                      >
                        {children}
                      </code>
                    );
                  },
                }}
              >
                {quest.condition}
              </ReactMarkdown>
            </div>
          </div>

          <div className="mt-6">
            <div className="p-2 primary_object">
              <CodeEditor language={language} code={code} onChange={setCode} />
            </div>
          </div>
          
          <div className="flex flox-row gap-3">
            {/* Submit Button */}
            <div className="mt-4">
              <button
                onClick={handleSubmit}
                className="primary_button"
                disabled={cooldown > 0}
              >
                {cooldown > 0 ? `Resubmit in ${cooldown}s` : "Submit Quest"}
              </button>
            </div>

            {/* Report Quest Button */}
            <div className="mt-4">
              <button
                onClick={() => {
                  setModalOpen(true);
                  setModalMessage("This feature is not implemented yet.");
                }}
                className="primary_button"
              >
                Report Quest
              </button>
            </div>
          </div>


          {/* Show Execution Results if available */}
          {executionResults && (
            <div className="mt-4 bg-gray-100 p-4 rounded shadow-sm primary_object">
              <h3 className="text-lg font-semibold mb-2">
                {executionResults.message}
              </h3>
              <p className="text-lg">
                ✅ Passed: <strong>{executionResults.successful_tests}</strong>
              </p>
              <p className="text-lg">
                ❌ Failed:{" "}
                <strong>{executionResults.unsuccessful_tests}</strong>
              </p>

              <div className="mt-2">
                <h4 className="font-medium text-s mb-1">Zero Test:</h4>
                <pre className="text-m rounded overflow-x-auto">
                  Input: {JSON.stringify(executionResults.zero_tests, null, 2)}
                </pre>
                <pre className="text-m rounded overflow-x-auto">
                  Your Output:{" "}
                  {JSON.stringify(executionResults.zero_tests_outputs, null, 2)}
                </pre>
              </div>
            </div>
          )}

          {/* Comments Section */}
          <div className="mt-10 p-2 primary_object">
            <h5>Comments</h5>
            <div className="d-flex align-items-center mt-3">
              <img
                src={avatarUrl}
                alt="User Avatar"
                className="rounded-full w-12 h-12 mr-3"
              />
              <textarea
                className="form-control w-full mt-4 rounded p-2 primary_text_area"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Enter your comment..."
              />
            </div>
            <button
              onClick={handleCommentSubmit}
              className="mt-2 primary_button"
            >
              Submit Comment
            </button>

            {/* Comments List */}
            {comments.map((c, index) => (
              <div key={index} className="mt-3 p-3 rounded primary_text_area">
                <div className="flex justify-between items-center">
                  <a href={`/profile/${c.username}`} className="text-gray-400">
                    {c.username}
                  </a>
                  <span className="text-sm text-gray-100">
                    {new Date(c.date_added).toLocaleString()}
                  </span>
                </div>
                <p className="mt-1">{c.comment}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
};

export default QuestPage;
