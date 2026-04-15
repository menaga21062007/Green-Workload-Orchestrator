import { useEffect, useState } from "react";

const BASE_URL = "https://green-backend.onrender.com";

function App() {
  const [tasks, setTasks] = useState([]);
  const [carbon, setCarbon] = useState(null);
  const [savings, setSavings] = useState(0);

  const [name, setName] = useState("");
  const [type, setType] = useState("background");

  useEffect(() => {
    const interval = setInterval(() => {
      fetch(`${BASE_URL}/tasks`)
        .then(res => res.json())
        .then(data => setTasks(data.tasks));

      fetch(`${BASE_URL}/carbon`)
        .then(res => res.json())
        .then(data => setCarbon(data));

      fetch(`${BASE_URL}/savings`)
        .then(res => res.json())
        .then(data => setSavings(data.co2_saved));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const addTask = () => {
    if (!name) return;

    fetch(`${BASE_URL}/task`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, type }),
    }).then(() => setName(""));
  };

  return (
    <div style={{ fontFamily: "Arial", padding: "20px" }}>
      
      <h1 style={{ textAlign: "center" }}>
        🌱 Green Workload Orchestrator
      </h1>

      <div style={{ display: "flex", justifyContent: "center", gap: "20px", marginTop: "20px" }}>
        
        <div style={{
          padding: "20px",
          borderRadius: "10px",
          background: "#f5f5f5",
          width: "250px",
          textAlign: "center"
        }}>
          <h3>Carbon Intensity</h3>
          {carbon && (
            <>
              <h2>{carbon.carbon_intensity}</h2>
              <p style={{ color: carbon.status === "GREEN" ? "green" : "red" }}>
                {carbon.status}
              </p>
            </>
          )}
        </div>

        <div style={{
          padding: "20px",
          borderRadius: "10px",
          background: "#e8f5e9",
          width: "250px",
          textAlign: "center"
        }}>
          <h3>CO₂ Saved</h3>
          <h2 style={{ color: "green" }}>{savings}</h2>
        </div>

      </div>

      <div style={{ textAlign: "center", marginTop: "30px" }}>
        <input
          type="text"
          placeholder="Task Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ padding: "8px", width: "200px" }}
        />

        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          style={{ marginLeft: "10px", padding: "8px" }}
        >
          <option value="background">Background</option>
          <option value="critical">Critical</option>
        </select>

        <button
          onClick={addTask}
          style={{
            marginLeft: "10px",
            padding: "8px 15px",
            background: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer"
          }}
        >
          Add Task
        </button>
      </div>

      <table
        style={{
          width: "80%",
          margin: "30px auto",
          borderCollapse: "collapse",
          textAlign: "center"
        }}
      >
        <thead style={{ background: "#333", color: "white" }}>
          <tr>
            <th style={{ padding: "10px" }}>Task Name</th>
            <th>Type</th>
            <th>Status</th>
            <th>Carbon</th>
          </tr>
        </thead>

        <tbody>
          {tasks.map((task, index) => (
            <tr key={index} style={{ borderBottom: "1px solid #ddd" }}>
              <td style={{ padding: "10px" }}>{task.name}</td>
              <td>{task.type}</td>
              <td style={{
                color: task.status === "RUNNING" ? "green" : "orange",
                fontWeight: "bold"
              }}>
                {task.status}
              </td>
              <td>{task.carbon_at_submission}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;