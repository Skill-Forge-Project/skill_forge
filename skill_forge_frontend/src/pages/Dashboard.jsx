import { Link } from 'react-router-dom';
import Navbar from "../components/Layout/Navbar";



export default function Dashboard() {


  return (
    <>
      <Navbar />
      <div>
        <div className="p-6 bg-gradient-to-b from-[#141e30] to-[#123556] min-h-screen">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-3xl font-bold primary_text">
              Welcome to Skill Forge!
            </h1>
            <p className="text-gray-300 mt-2 secondary_text">
              Discover a world of coding challenges and quests designed to
              enhance your programming skills. Whether you're a beginner or an
              expert, Skill Forge offers a variety of quests in different
              languages to help you grow and succeed. Join our community, track
              your progress, and compete with others!
            </p>

            {/* Quests Cards */}
            <div className="grid md:grid-cols-4 gap-8 mt-20">
              {/* Python Card */}
              <Link to={`/quests/Python`}>
                <div className="relative p-3 mb-20 rounded-lg shadow-lg primary_object overflow-hidden python_button">
                  <img
                    src="src/assets/img/achievements-icons/Python/python-6.png"
                    alt="Python Background"
                    className="absolute inset-0 w-full h-50 object-cover opacity-40"
                  />

                  <div className="relative z-10">
                    <div className="mt-20 mb-0 py-1 px-4 rounded-lg text-xl">
                      Python Quests
                    </div>
                  </div>
                </div>
              </Link>

              {/* JavaScript Card */}
              <Link to={`/quests/JavaScript`}>
                <div className="relative p-3 mb-20 rounded-lg shadow-lg primary_object overflow-hidden js_button">
                  <img
                    src="src/assets/img/achievements-icons/JavaScript/javascript-1.png"
                    alt="JavaScript Background"
                    className="absolute inset-0 w-full h-full object-cover opacity-20"
                  />
                  <div className="relative z-10">
                    <div className="mt-20 mb-0 py-1 px-4 rounded-lg text-xl">
                      JavaScript Quests
                    </div>
                  </div>
                </div>
              </Link>

              {/* Java Card */}
              <Link to={`/quests/Java`}>
                <div className="relative p-3 mb-20 rounded-lg shadow-lg primary_object overflow-hidden java_button">
                  <img
                    src="src/assets/img/achievements-icons/Java/java-5.png"
                    alt="Java Background"
                    className="absolute inset-0 w-full h-full object-cover opacity-20"
                  />
                  <div className="relative z-10">
                    <div className="mt-20 mb-0 py-1 px-4 rounded-lg text-xl">
                      Java Quests
                    </div>
                  </div>
                </div>
              </Link>

              {/* C# Card */}
              <Link to={`${"/quests/Csharp"}`}>
                <div className="relative p-3 mb-0 rounded-lg shadow-lg primary_object overflow-hidden csharp_button">
                  <img
                    src="src/assets/img/achievements-icons/CS/cs-1.png"
                    alt="CSharp Background"
                    className="absolute inset-0 w-full h-full object-cover opacity-20"
                  />
                  <div className="relative z-10">
                    <div className="mt-20 mb-0 py-1 px-4 rounded-lg text-xl">
                      C# Quests
                    </div>
                  </div>
                </div>
              </Link>
            </div>

            <div className="grid md:grid-cols-4 gap-8 mt-8">
              {/* Leaderboard Section */}
              <div className="mt-2">
                <Link to="/leaderboard">
                  <div
                    className="p-6 w-100 h-100 rounded-lg shadow-lg mt-6 bg-cover bg-center primary_object"
                    style={{
                      backgroundImage: "url('src/assets/img/stats_avatar.png')",
                      width: "300px",
                      height: "150px",
                    }}
                  />
                </Link>
                <h2 className="text-2xl font-semibold primary_text">
                  Leaderboard
                </h2>
              </div>

              {/* Underworld Section */}
              <div className="mt-2">
                <Link to="/underworld">
                  <div
                    className="p-6 w-100 h-100 rounded-lg shadow-lg mt-6 bg-cover bg-center primary_object"
                    style={{
                      backgroundImage:
                        "url('src/assets/img/underworld_realm/Underworld.png')",
                      width: "300px",
                      height: "150px",
                    }}
                  />
                </Link>
                <h2 className="text-2xl font-semibold primary_text">
                  Underworld
                </h2>
              </div>

              {/* Trivia Section */}
              <div className="mt-2">
                <Link to="/underworld">
                  <div
                    className="p-6 w-100 h-100 rounded-lg shadow-lg mt-6 bg-cover bg-center primary_object"
                    style={{
                      backgroundImage:
                        "url('src/assets/img/construction_worker.png')",
                      width: "300px",
                      height: "150px",
                    }}
                  />
                </Link>
                <h2 className="text-2xl font-semibold primary_text">
                Trivia
                </h2>
              </div>

            </div>

            {/* Stats Section */}
            <div className="mt-12">
              <h2 className="text-2xl font-semibold text-white">Your Stats</h2>
              <div className="grid md:grid-cols-2 gap-8 mt-6">
                <div className="bg-white p-6 rounded-lg shadow-lg">
                  <h4 className="text-lg font-semibold text-slate-800">
                    XP Points
                  </h4>
                  <p className="text-slate-600 mt-2">Current XP: 1200</p>
                  <div className="w-full h-2 bg-blue-100 mt-4 rounded-full">
                    <div
                      className="h-full bg-blue-600"
                      style={{ width: "80%" }}
                    ></div>
                  </div>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-lg">
                  <h4 className="text-lg font-semibold text-slate-800">
                    Completed Challenges
                  </h4>
                  <p className="text-slate-600 mt-2">
                    You have completed 15 out of 20 challenges.
                  </p>
                  <div className="w-full h-2 bg-blue-100 mt-4 rounded-full">
                    <div
                      className="h-full bg-blue-600"
                      style={{ width: "75%" }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Section */}
            <div className="mt-12 flex justify-center gap-6">
              <button className="bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 focus:outline-none transition duration-300">
                Start a New Quest
              </button>
              <button className="bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 focus:outline-none transition duration-300">
                Level Up!
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
