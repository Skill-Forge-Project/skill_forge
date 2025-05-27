// Fetch the user avatar from the server


export async function getAvatarUrl(userId, token, userApiBase) {
    try {
      const response = await fetch(`${userApiBase}/users/${userId}/avatar`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      if (!response.ok) throw new Error("Failed to fetch avatar");
  
      const blob = await response.blob();
      return URL.createObjectURL(blob);
    } catch (err) {
      console.error("Error fetching avatar:", err);
      return null;
    }
  }