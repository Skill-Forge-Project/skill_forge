import React, { useState } from "react";
import { Link } from "react-router-dom";
import { updateUser } from "../../services/usersService";

// Import Social Media Icons
import FacobookIcon from "../../assets/img/social_media_icons/facebook.png";
import InstagramIcon from "../../assets/img/social_media_icons/instagram.png";
import GithubIcon from "../../assets/img/social_media_icons/github.svg";
import DiscordIcon from "../../assets/img/social_media_icons/discord.svg";
import LinkedInIcon from "../../assets/img/social_media_icons/linkedin.png";

const ProfileMain = ({ user, setModalOpen, setModalMessage }) => {
  const [formData, setFormData] = useState({
    about_me: user.about_me || "",
    first_name: user.first_name || "",
    last_name: user.last_name || "",
    email: user.email || "",
    facebook_profile: user.facebook_profile || "",
    instagram_profile: user.instagram_profile || "",
    github_profile: user.github_profile || "",
    discord_id: user.discord_id || "",
    linked_in: user.linked_in || "",
  });
  const [avatarFile, setAvatarFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const updatedUser = await updateUser(user.id, formData);
      setModalMessage("Profile updated successfully!");
      setModalOpen(true);
    } catch (err) {
      setModalMessage("Failed to update profile.");
      setModalOpen(true);
    }
  };

  const handleAvatarChange = (e) => {
    setAvatarFile(e.target.files[0]);
  };

  const handleAvatarUpload = async (e) => {
    e.preventDefault();
    if (!avatarFile) return;

    const token = localStorage.getItem("token");
    const form = new FormData();
    form.append("avatar", avatarFile);

    try {
      const res = await fetch(
        `${import.meta.env.VITE_USERS_SERVICE_URL}/update_user/${user.id}/avatar`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: form,
        }
      );

      const data = await res.json();
      if (!res.ok) throw new Error(data.message || "Upload failed");
      setModalMessage("Avatar updated successfully!");
      setModalOpen(true);
    } catch (err) {
      setModalMessage("Avatar upload failed.");
      setModalOpen(true);
    }
    // Redirect to the profile page
    window.location.reload();
  };

  return (
    <div className="shadow rounded-lg p-6 primary_object">
      <h2 className="text-xl font-bold mb-4 primary_text">About Me</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="about_me" className="block mb-2 font-medium">
          Bio
        </label>
        <textarea
          id="about_me"
          rows="7"
          placeholder="Share your story or interests. What makes you unique?"
          className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          value={formData.about_me}
          onChange={(e) =>
            setFormData({ ...formData, about_me: e.target.value })
          }
        />

        {/* Personal Information */}
        <div className="grid gap-6 my-6 md:grid-cols-2">
          <div>
            <label htmlFor="first_name" className="block mb-2 font-medium">
              First name
            </label>
            <input
              type="text"
              id="first_name"
              required
              className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              value={formData.first_name}
              onChange={(e) =>
                setFormData({ ...formData, first_name: e.target.value })
              }
            />
          </div>
          <div>
            <label htmlFor="last_name" className="block mb-2 font-medium">
              Last name
            </label>
            <input
              type="text"
              id="last_name"
              required
              className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              value={formData.last_name}
              onChange={(e) =>
                setFormData({ ...formData, last_name: e.target.value })
              }
            />
          </div>
        </div>

        {/* Email Input */}
        <div className="mb-6">
          <label htmlFor="email" className="block mb-2 font-medium">
            Email address
          </label>
          <input
            type="email"
            id="email"
            required
            className="text-gray-900 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            value={formData.email}
            onChange={(e) =>
              setFormData({ ...formData, email: e.target.value })
            }
          />
        </div>

        {/* Social Media Links */}
        <label className="mb-2 block font-medium">Social Media Links</label>
        {/* Iterate over the social media fields */}
        {[
          { name: "facebook_profile", placeholder: "Facebook Profile", icon: FacobookIcon },
          { name: "instagram_profile", placeholder: "Instagram Profile", icon: InstagramIcon },
          { name: "github_profile", placeholder: "GitHub Profile", icon: GithubIcon },
          { name: "discord_id", placeholder: "Discord ID", icon: DiscordIcon },
          { name: "linked_in", placeholder: "LinkedIn Profile", icon: LinkedInIcon },
        ].map((field) => (
          <div key={field.name} className="relative flex items-center my-2">
          <img src={field.icon} alt={`${field.name} icon`} className="absolute left-4 w-4" />

            <input
              type="text"
              placeholder={field.placeholder}
              className="pl-14 pr-4 py-3 text-gray-900 rounded-lg block w-full dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              value={formData[field.name] || ""}
              onChange={(e) =>
                setFormData({ ...formData, [field.name]: e.target.value })
              }
            />
          </div>
        ))}

        {/* Save Profile Button */}
        <div className="mt-6">
          <button
            type="submit"
            className="py-2 px-6 rounded-lg primary_button"
          >
            Save Profile
          </button>
        </div>
      </form>

      {/* Avatar Upload */}
      <div className="mt-8">
        <form
          onSubmit={handleAvatarUpload}
          className="flex flex-col space-y-4"
        >
          <input
            type="file"
            accept="image/*"
            onChange={handleAvatarChange}
            className="ca-3"
          />
          <button
            type="submit"
            name="update_avatar"
            className="ca-4 primary_button"
          >
            Update Avatar
          </button>
        </form>
      </div>
    </div>
  );
};

export default ProfileMain;