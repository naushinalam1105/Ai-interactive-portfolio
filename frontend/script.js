// -------------------------------------------------------------
// 1. CONFIGURATION & DOM ELEMENTS
// -------------------------------------------------------------
const API_BASE = "http://localhost:8000";
let profileData = null;

// Grab all necessary HTML elements
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const heroView = document.getElementById("heroView");
const messagesList = document.getElementById("messagesList");
const typingIndicator = document.getElementById("typingIndicator");
const scrollContainer = document.getElementById("scrollContainer");
const newChatBtn = document.getElementById("newChatBtn");
const historyText = document.getElementById("historyText");

const modalOverlay = document.getElementById("modalOverlay");
const modalBody = document.getElementById("modalBody");

// Render Lucide SVG icons on page load
lucide.createIcons();


// -------------------------------------------------------------
// 2. FETCH CANDIDATE PROFILE DATA
// -------------------------------------------------------------
async function loadProfile() {
  try {
    const response = await fetch(`${API_BASE}/profile`);
    profileData = await response.json();
  } catch (error) {
    console.error("Failed to load candidate profile:", error);
  }
}
loadProfile();


// -------------------------------------------------------------
// 3. CHAT LOGIC & DOM UPDATES
// -------------------------------------------------------------
function scrollToBottom() {
  scrollContainer.scrollTop = scrollContainer.scrollHeight;
}

// Function to add a chat bubble (User or AI)
function addMessage(sender, text) {
  // Hide the hero welcome box and show the messages list
  heroView.classList.add("hidden");
  messagesList.classList.remove("hidden");

  // Create a message container div
  const messageRow = document.createElement("div");
  messageRow.className = `message-row ${sender}`;

  if (sender === "user") {
    messageRow.innerHTML = `
      <div class="message-bubble">${text}</div>
    `;
    historyText.textContent = text;
  } else {
    // Convert Markdown from AI into HTML using Marked.js
    const htmlContent = marked.parse(text);
    messageRow.innerHTML = `
      <div class="avatar-small">
        <img src="profile.jpg" alt="Avatar" class="avatar-img" onerror="this.style.display='none';" />
      </div>
      <div class="message-bubble">${htmlContent}</div>
    `;
  }

  messagesList.appendChild(messageRow);
  scrollToBottom();
}

// Function to call the FastAPI backend
async function askAI(userQuestion) {
  if (!userQuestion) return;

  // 1. Clear input & show user message immediately
  chatInput.value = "";
  addMessage("user", userQuestion);

  // 2. Show loading dots
  typingIndicator.classList.remove("hidden");
  scrollToBottom();

  // 3. Send request to backend
  try {
    const response = await fetch(`${API_BASE}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userQuestion })
    });
    const data = await response.json();

    // 4. Hide loading dots & display AI reply
    typingIndicator.classList.add("hidden");
    addMessage("assistant", data.reply);
  } catch (error) {
    typingIndicator.classList.add("hidden");
    addMessage("assistant", "Sorry, I am unable to connect to the backend server right now.");
  }
}

// Form Submit Event (Pressing Enter or clicking Send)
chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const question = chatInput.value.trim();
  askAI(question);
});

// Quick Prompt Card Click
function sendPrompt(queryText) {
  askAI(queryText);
}

// New Chat Button Click
newChatBtn.addEventListener("click", () => {
  messagesList.innerHTML = "";
  messagesList.classList.add("hidden");
  heroView.classList.remove("hidden");
  historyText.textContent = "No active chat";
});


// -------------------------------------------------------------
// 4. MODAL POPUPS (About, Skills, Projects, Education)
// -------------------------------------------------------------
function openModal(category) {
  modalOverlay.classList.remove("hidden");

  if (category === "about") {
    modalBody.innerHTML = `
      <h3 class="modal-title"><i data-lucide="user"></i> About Naushin</h3>
      <p class="modal-content-text" style="font-family: monospace;">
        Email: <span style="color:#f1f5f9;">${profileData?.email || "naushinalam786@gmail.com"}</span><br>
        Location: <span style="color:#f1f5f9;">Durgapur, West Bengal</span>
      </p>
      <p class="modal-content-text" style="padding-top: 8px;">
        Computer Science & Engineering student with experience in frontend AI engineering, full-stack web development, and GenAI learner.
      </p>
    `;
  } 
  else if (category === "skills") {
    const skillsList = profileData?.skills
      ? profileData.skills.map(skill => `<span class="skill-badge">${skill}</span>`).join("")
      : "<p class='modal-content-text'>No skills loaded.</p>";

    modalBody.innerHTML = `
      <h3 class="modal-title"><i data-lucide="code-2"></i> Technical Stack</h3>
      <div class="chips-container">${skillsList}</div>
    `;
  } 
  else if (category === "projects") {
    const projectsList = profileData?.projects
      ? profileData.projects.map(item => `<div class="item-card">${item}</div>`).join("")
      : "<p class='modal-content-text'>No projects listed.</p>";

    modalBody.innerHTML = `
      <h3 class="modal-title"><i data-lucide="terminal"></i> Key Projects</h3>
      <div style="margin-top: 10px;">${projectsList}</div>
    `;
  } 
  else if (category === "education") {
    const educationList = profileData?.education
      ? profileData.education.map(item => `<div class="item-card">${item}</div>`).join("")
      : "<p class='modal-content-text'>No education entries listed.</p>";

    modalBody.innerHTML = `
      <h3 class="modal-title"><i data-lucide="graduation-cap"></i> Education & Qualifications</h3>
      <div style="margin-top: 10px;">${educationList}</div>
    `;
  }

  // Re-run Lucide icons for icons injected inside modal HTML
  lucide.createIcons();
}

function closeModal() {
  modalOverlay.classList.add("hidden");
}

// Close modal if user clicks outside the modal box
window.addEventListener("click", (e) => {
  if (e.target === modalOverlay) {
    closeModal();
  }
});