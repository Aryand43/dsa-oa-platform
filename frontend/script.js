// Toggle dark mode
document.getElementById("darkToggle").addEventListener("click", () => {
  document.body.classList.toggle("dark");
});

// Fetch leaderboard and inject into table
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

    confetti({
      particleCount: 120,
      spread: 70,
      origin: { y: 0.6 }
    });

  } catch (err) {
    console.error("Error fetching leaderboard:", err);
    alert("Could not fetch leaderboard. Is the backend running?");
  }
};
