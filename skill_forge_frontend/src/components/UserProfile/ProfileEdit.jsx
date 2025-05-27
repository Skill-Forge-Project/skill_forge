// ProfileEdit.js
import React, { useState } from 'react';

const ProfileEdit = () => {
//   const [name, setName] = useState(user.name);
//   const [email, setEmail] = useState(user.email);
  const [avatar, setAvatar] = useState(null);

  const handleSave = () => {
    const updatedData = { name, email, avatar };
    onSave(updatedData); // Handle saving the updated profile
  };

  const handleAvatarChange = (event) => {
    const file = event.target.files[0];
    setAvatar(file);
  };

  return (
    <div>PROFILE EDIT SECTION</div>
    // <div className="mt-8 p-6 bg-white rounded-lg shadow-md">
    //   <h3 className="text-2xl font-semibold">Edit Profile</h3>
    //   <div className="mt-4">
    //     <label className="block text-lg">Name</label>
    //     <input
    //       type="text"
    //       value={name}
    //       onChange={(e) => setName(e.target.value)}
    //       className="w-full p-2 mt-2 border rounded-md"
    //     />
    //   </div>
    //   <div className="mt-4">
    //     <label className="block text-lg">Email</label>
    //     <input
    //       type="email"
    //     //   value={email}
    //       onChange={(e) => setEmail(e.target.value)}
    //       className="w-full p-2 mt-2 border rounded-md"
    //     />
    //   </div>
    //   <div className="mt-4">
    //     <label className="block text-lg">Avatar</label>
    //     <input
    //       type="file"
    //       onChange={handleAvatarChange}
    //       className="mt-2"
    //     />
    //   </div>
    //   <div className="mt-6">
    //     <button
    //       onClick={handleSave}
    //       className="bg-blue-600 text-white px-4 py-2 rounded-lg"
    //     >
    //       Save Changes
    //     </button>
    //   </div>
    // </div>
  );
};

export default ProfileEdit;