import React from "react";
import { Link } from "react-router-dom";
import "../../assets/styling/underworld.css";
import Navbar from "../../components/Layout/Navbar";
import { useEffect, useState } from 'react';
import { getAllBosses } from '../../services/underworldService';

const UnderworldPage = () => {
  const [bosses, setBosses] = useState([]);

  useEffect(() => {
    const fetchBosses = async () => {
      try {
        const data = await getAllBosses();
        setBosses(data);
      } catch (error) {
        console.error("Failed to fetch bosses:", error);
      }
    };

    fetchBosses();
  }, []);

  return (
    <>
      <Navbar />

      <div className="min-h-screen p-6">
        <h2 className="font-bold text-center mb-4 underworld_primary_text">
          Welcome, Brave Soul, to the Underworld Realm!
        </h2>
        <p className="font-bold text-center mb-4 underworld_secondary_text">
          In this enchanted domain, where shadows dance and whispers of ancient
          knowledge echo, prepare to face the mightiest bosses of lore. Gather
          your wits, summon your courage, and embark on a quest filled with
          trials and triumphs. May fortune favor the bold as you delve into the
          depths of the Underworld!
        </p>

        <div className="bg-overlay p-6 rounded-lg">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {bosses.length > 0 ? (
              bosses.map((boss) => (
                <div
                  key={boss.boss_id}
                  className="rounded-lg shadow-md p-0 hover:shadow-xl transition-shadow duration-300 flex flex-col underworld_boss_container"
                >
                  <img
                    src={`/src/assets/img/underworld_realm/${boss.boss_name}.png`}
                    alt={boss.boss_name}
                    className="w-52 rounded-2xl mx-auto mb-4"
                  />
                  <h3 className="text-xl font-semibold text-center mb-0 underworld_secondary_text">
                    {boss.boss_name}
                  </h3>
                  <p className="font-bold text-center mt-0 mb-3 underworld_secondary_text">
                    {boss.boss_title}
                  </p>
                  <p className="text-center underworld_secondary_text">
                    Language: <strong>{boss.boss_language}</strong>
                  </p>
                  <p className="text-center underworld_secondary_text">
                    Specialty: <strong>{boss.boss_specialty}</strong>
                  </p>
                  <p className="text-center underworld_secondary_text">
                    Difficulty: <strong>{boss.boss_difficulty}</strong>
                  </p>
                  <div className="flex-grow"></div>
                  <Link
                    to={`/underworld/challenge/${boss.id}`}
                    className="text-center mt-4 underworld_button"
                  >
                    Challenge!
                  </Link>
                </div>
              ))
            ) : (
              <div className="col-span-1 sm:col-span-2 md:col-span-3 lg:col-span-4 text-center">
                <p className="text-gray-600 underworld_secondary_text">
                  All bosses are currenly resting
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default UnderworldPage;
