const USER_API = import.meta.env.VITE_USERS_SERVICE_URL;

// Get all users from the Users Service
export const getAllUsers = async () => {
  const token = localStorage.getItem("token");
  const res = await fetch(`${USER_API}/users`, {
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.message || "Failed to fetch users");
  return data;
};

// Get a single user by ID from the Users Service
export const getUserById = async (userId) => {
  const token = localStorage.getItem("token");
  const res = await fetch(`${USER_API}/users/${userId}`, {
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.message || "Failed to fetch user");
  return data;
};

// Get user avatar URL
export const getAvatarUrl = async (userId) => {
  const token = localStorage.getItem("token");
  const res = await fetch(`${USER_API}/users/${userId}/avatar`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",

    },
  });

  if (!res.ok) throw new Error("Failed to fetch avatar URL");
  return res.url;
};

// Update user information based on user ID
export const updateUser = async (userId, updatedData) => {
  const token = localStorage.getItem("token");
  const res = await fetch(`${USER_API}/update_user/${userId}`, {
    method: "PUT",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(updatedData),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || "Failed to update user");
  return data;
};
