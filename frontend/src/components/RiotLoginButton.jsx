import React from "react";

export default function RiotLoginButton() {
  const handleLogin = () => {
    // Redirect to backend endpoint that starts Riot OAuth flow
    window.location.href = "http://127.0.0.1:8000/api/riot/oauth/login/";
  };

  return (
    <button
      onClick={handleLogin}
      className="bg-red-500 hover:bg-red-600 text-white font-semibold px-4 py-2 rounded-xl transition duration-200 shadow-md"
    >
      Connect Riot Account
    </button>
  );
}
