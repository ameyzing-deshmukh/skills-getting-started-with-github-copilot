document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = type;
    messageDiv.classList.remove("hidden");
    setTimeout(() => {
      messageDiv.classList.add("hidden");
    }, 5000);
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message and reset dropdown
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;
      const participants = Array.isArray(details.participants) ? details.participants : [];
      const participantsHtml = participants.length
        ? `<div class="participants-section">
             <strong>Participants:</strong>
             <ul>
               ${participants
                 .map((participant) => `
                   <li class="participant-item">
                     <span class="participant-name">${participant}</span>
                     <button
                       type="button"
                       class="participant-delete"
                       data-activity="${encodeURIComponent(name)}"
                       data-email="${encodeURIComponent(participant)}"
                       aria-label="Remove ${participant}"
                     >🗑️</button>
                   </li>`)
                 .join("")}
             </ul>
           </div>`
        : `<div class="participants-section participants-empty">No participants signed up yet.</div>`;

      activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          ${participantsHtml}
        `;

      // Add option to select dropdown
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      activitySelect.appendChild(option);
      activitiesList.appendChild(activityCard);

      activityCard.querySelectorAll(".participant-delete").forEach((button) => {
        button.addEventListener("click", async () => {
          const activityName = decodeURIComponent(button.dataset.activity);
          const email = decodeURIComponent(button.dataset.email);

          try {
            const response = await fetch(
              `/activities/${encodeURIComponent(activityName)}/participants?email=${encodeURIComponent(email)}`,
              { method: "DELETE" }
            );
            const result = await response.json();

            if (response.ok) {
              showMessage(result.message, "success");
              fetchActivities();
            } else {
              showMessage(result.detail || "Failed to remove participant", "error");
            }
          } catch (error) {
            console.error("Error removing participant:", error);
            showMessage("Failed to remove participant.", "error");
          }
        });
      });
    });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message, "success");
        signupForm.reset();
        fetchActivities();
      } else {
        showMessage(result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage("Failed to sign up. Please try again.", "error");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
