window.onload = async () => {
  try {
    const res = await fetch("http://127.0.0.1:8000/leaderboard");
    const data = await res.json();
    const tbody = document.querySelector("#leaderboard tbody");

    data.leaderboard.forEach((entry, index) => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${index + 1}</td>
        <td>${entry.user_id}</td>
        <td>${entry.score}</td>
        <td>${entry.replay_result}</td>
        <td>${new Date(entry.timestamp).toLocaleString()}</td>
      `;

      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Error fetching leaderboard:", err);
    alert("Could not fetch leaderboard. Is the backend running?");
  }
};
