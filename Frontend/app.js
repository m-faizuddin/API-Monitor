const BASE_URL = "http://127.0.0.1:8000";
// const BASE_URL = "http://localhost:8000";

window.onload = function() {
   loadAPIS();
}

function loadAPIS(){
   const container = document.getElementById("apis-container");
   fetch(`${BASE_URL}/apis`)
   .then(res => res.json())
   .then(apis => {
    if(apis.length === 0)
    {
      container.innerHTML = "<p>No APIs added yet</p>";

      return;
    }
    container.innerHTML = "";

    apis.forEach(api => {
      const card = document.createElement("div");
      card.classList.add("api-card");
      card.id = `card-${api.id}`;

      card.innerHTML = `
    <div class = "card-top">
      <div class="info">
        <h3>${api.name}</h3>
        <p>${api.url}</p>
      </div>
      <div class="actions">
          <span class="${api.is_active ? "badge-active" : "badge-inactive"}">
          ${api.is_active ? "Active" : "Inactive"}
          </span>

          <button class="btn-stats" onclick="toggleStats(${api.id})">
            Stats
          </button>
          <button class="btn-toggle" onclick="toggleStatus(${api.id}, ${api.is_active})">
            ${api.is_active ? "Deactivate" : "Activate"}
          </button>
      </div>
    </div>
      `;

      const statsBox = document.createElement("div");
      statsBox.className = "stats-box";
      statsBox.id = `stats-${api.id}`;

      card.appendChild(statsBox);

      container.appendChild(card);


     
    })
   })


   
}

async function addAPI(){
  const name = document.getElementById("api-name").value.trim(); 
  const url = document.getElementById("api-url").value.trim();

  if(!name || !url){
    alert("Please provide both name and URL for the API.");
    return;
  }

  await fetch(`${BASE_URL}/apis`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ name, url })
  });

  document.getElementById("api-name").value = "";
  document.getElementById("api-url").value = "";

  loadAPIS(); 

}

async function toggleStatus(id, currentStatus){
  await fetch(`${BASE_URL}/apis/${id}/status`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ is_active: !currentStatus })  

  });
  loadAPIS();
}

async function toggleStats(id){
  const statsBox = document.getElementById(`stats-${id}`);

  if(statsBox.style.display === "block"){
    statsBox.style.display = "none";
    return;
  }

  fetch(`${BASE_URL}/apis/${id}/stats`)
  .then(res => res.json())
  .then(stats => {
    statsBox.innerHTML = `
      <h4>Stats</h4>
      <p>Total Checks: ${stats.total_checks}</p>
      <p>Uptime Percentage: ${stats.uptime_percentage}</p>
      <p>Average Response Time: ${stats.avg_response_time_ms}ms</p>
    `;
    statsBox.style.display = "block";
  });



}