import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../../components/Layout/Navbar";
import { getBossById } from "../../services/underworldService";
import { generateChallenge } from "../../services/underworldService";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "github-markdown-css/github-markdown.css";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import LoadingSpinner from "../../components/Layout/LoadingSpinner";



const BossChallengePage = () => {
  const { bossId } = useParams();
  const [boss, setBoss] = useState(null);
  const [challenge, setChallenge] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBossAndChallenge = async () => {
      try {
        // Fetch boss details by bossId
        const bossData = await getBossById(bossId);
        setBoss(bossData);

        // Fetch challenge for this boss
        const challengeData = await generateChallenge(bossId);
        setChallenge(challengeData);
      } catch (error) {
        console.error("Failed to fetch boss or challenge:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchBossAndChallenge();
  }, [bossId]);

  if (loading) return <LoadingSpinner message={`Generating a new challenge for you, please wait.\nDo NOT reload or close this page!`} />;

  // WIP: Implement 404 page
  if (!boss || !challenge) return <p>Failed to load challenge.</p>;

  return (
    <>
      <Navbar />
      <form method="POST" className="container mx-auto center py-8">
        <div className="grid grid-cols-1 sm:grid-cols-12 gap-6 px-4">
          {/* Left Column: Boss Info */}
          <div className="col-span-12 sm:col-span-3">
            <div className="shadow rounded-lg p-6 underworld_boss_container underworld_secondary_text">
              <div className="flex flex-col items-center">
                <img
                  src={`/src/assets/img/underworld_realm/${boss.boss_name}.png`}
                  alt={boss.boss_name}
                  className="w-64 rounded-2xl mx-auto mb-4"
                />
                <h1 className="text-xl font-bold mb-0">{boss.boss_name}</h1>
                <p className="text-gray-400 m-0">{boss.boss_title}</p>
                <p className="mt-2 text-center">
                  <strong>{boss.boss_description}</strong>
                </p>
              </div>
              <hr className="my-6 border-t border-gray-300" />
              <div className="flex flex-col">
                <span className="text-gray-400 uppercase font-bold tracking-wider mb-2">
                  Boss Stats
                </span>
                <p>Language: <strong>{boss.boss_language}</strong></p>
                <p>Specialty: <strong>{boss.boss_specialty}</strong></p>
                <p>Difficulty: <strong>{boss.boss_difficulty}</strong></p>
              </div>
            </div>
          </div>

          {/* Right Column: Challenge Content */}
          <div className="col-span-12 sm:col-span-9 space-y-6">
            {/* Timer (Optional) */}
            <div className="shadow rounded-lg p-6 underworld_boss_container underworld_primary_text">
              <h3 className="font-bold mb-1">Time Remaining</h3>
              <div className="count">
                <div className="timer" id="timer">⏳</div>
              </div>
            </div>

            {/* Challenge Section */}
            <div className="shadow rounded-lg p-6 underworld_boss_container">
              <h2 className="font-bold text-xl mb-3 underworld_primary_text">My Challenge for you</h2>
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  code({ node, inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || "");
                    return !inline && match ? (
                      <SyntaxHighlighter
                        style={oneDark}
                        language={match[1]}
                        className="underworld_secondary_text"
                        PreTag="div"
                        customStyle={{
                          padding: "1rem",
                          borderRadius: "0.5rem",
                          fontSize: "0.9rem",
                          lineHeight: "1.5",
                        }}
                        {...props}
                      >
                        {String(children).replace(/\n$/, "")}
                      </SyntaxHighlighter>
                    ) : (
                      <code
                        className="bg-gray-100 text-red-600 px-1 py-0.5 rounded text-sm font-mono"
                        {...props}
                      >
                        {children}
                      </code>
                    );
                  },
                  pre({ node, ...props }) {
                    return <div className="my-4 underworld_secondary_text">{props.children}</div>;
                  },
                  p({ node, children }) {
                    return <p className="mb-2 text-gray-500 underworld_secondary_text">{children}</p>;
                  },
                }}
              >
                {challenge}
              </ReactMarkdown>
            </div>

            {/* User Answer */}
            <div className="shadow rounded-lg p-6 underworld_boss_container">
              <h2 className="font-bold mb-2 underworld_primary_text">Your Answer</h2>
              <textarea
                name="user_answer"
                rows="10"
                placeholder="Provide your answer"
                className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>

            {/* Submit Button */}
            <div className="flex justify-end">
              <button
                type="submit"
                className="px-6 py-2 rounded-lg transition underworld_button"
              >
                Submit Challenge
              </button>
            </div>
          </div>
        </div>
      </form>
    </>
  );
};

export default BossChallengePage;