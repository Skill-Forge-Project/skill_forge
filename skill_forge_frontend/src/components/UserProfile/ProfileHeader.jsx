import { format } from 'date-fns';

const ProfileHeader = ( {user, avatarUrl} ) => {

  const formattedDate = user?.last_seen_date
    ? format(new Date(user.last_seen_date), 'dd-MM-yyyy HH:mm')
    : '';

  if (!user) return <div className="text-white">No user data...</div>;

  return (
    <div className="grid gap-6 px-4 primary_object">
      <div className="">
        <div className="shadow rounded-lg p-6">
          <div className="flex flex-col items-center">
            <img
              className="inline-block w-48 h-48 rounded-full avatar_border"
              src={avatarUrl}
              id="avatarPreview"
              alt="Avatar"
            />
            <h1 className="text-xl font-bold">{user.username}</h1>
            <p className="text-l">{user.first_name} {user.last_name}</p>
            <p className="flex flex-row mt-2 text-xl"><p className="bold text-xl mr-1 text-gray-400">Rank:</p> {user.rank}</p>

            <div className="mt-6 flex flex-wrap gap-4 justify-center">
              <div className="" id="onlineStatusDiv">
                {user.user_online_status === "Offline" ? (
                  <>
                    <p className="">Last seen</p>
                    <p className="">{formattedDate}</p>
                  </>
                ) : (
                  <p className="text-xl">USER STATUS</p> // Modify this to show the actual status
                )}
              </div>
            </div>
          </div>

          <hr className="my-6 border-t border-gray-300" />

          <p className="text-s">Level: {user.level}</p>
          <div
            className="flex w-full h-4 bg-gray-200 rounded-full overflow-hidde"
            role="progressbar"
            aria-valuenow={user.level_percentage || 50}  // Use user data for progress bar
            aria-valuemin="0"
            aria-valuemax="100"
          >
            <div
              className="flex flex-col justify-center rounded-full overflow-hidden text-xs text-white text-center whitespace-nowrap dark:bg-blue-500 transition duration-500"
              style={{ width: `${user.level_percentage || 50}%` }}  // Use user data for progress bar width
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileHeader;