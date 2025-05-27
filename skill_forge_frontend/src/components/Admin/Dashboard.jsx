const Dashboard = () => {
    return (
      <>
        <h1 className="text-3xl font-semibold mb-6 primary_text">Welcome, Admin</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="shadow rounded p-4 primary_object">
            <h2 className="text-xl font-semibold">Total Users</h2>
            <p className="mt-2 text-3xl">2 / 124</p>
          </div>
          <div className="shadow rounded p-4 primary_object">
            <h2 className="text-xl font-semibold">Active Quests</h2>
            <p className="mt-2 text-3xl">58</p>
          </div>
          <div className="shadow rounded p-4 primary_object">
            <h2 className="text-xl font-semibold">Reported Quests</h2>
            <p className="mt-2 text-3xl">3</p>
          </div>
        </div>
      </>
    );
  };
  
  export default Dashboard;