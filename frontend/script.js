// -------------------------------------------------------------
// 1. CONFIGURATION & DOM REFERENCES
// -------------------------------------------------------------
const API_BASE = "http://localhost:8000";
let profileData = null;

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

// Render Lucide SVG icons
lucide.createIcons();

// -------------------------------------------------------------
// 2. FETCH PROFILE ON STARTUP
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
// 3. CHAT HANDLING & DOM UPDATES
// -------------------------------------------------------------
function scrollToBottom() {
  scrollContainer.scrollTop = scrollContainer.scrollHeight;
}

function addMessage(sender, text) {
  heroView.classList.add("hidden");
  messagesList.classList.remove("hidden");

  const messageRow = document.createElement("div");
  messageRow.className = `message-row ${sender}`;

  if (sender === "user") {
    messageRow.innerHTML = `<div class="message-bubble">${text}</div>`;
    historyText.textContent = text;
  } else {
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

async function askAI(userQuestion) {
  if (!userQuestion) return;

  chatInput.value = "";
  addMessage("user", userQuestion);

  typingIndicator.classList.remove("hidden");
  scrollToBottom();

  try {
    const response = await fetch(`${API_BASE}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userQuestion })
    });
    const data = await response.json();

    typingIndicator.classList.add("hidden");
    addMessage("assistant", data.reply);
  } catch (error) {
    typingIndicator.classList.add("hidden");
    addMessage("assistant", "Sorry, I am unable to connect to the backend server right now.");
  }
}

chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const question = chatInput.value.trim();
  askAI(question);
});

function sendPrompt(queryText) {
  askAI(queryText);
}

newChatBtn.addEventListener("click", () => {
  messagesList.innerHTML = "";
  messagesList.classList.add("hidden");
  heroView.classList.remove("hidden");
  historyText.textContent = "No active chat";
});

// -------------------------------------------------------------
// 4. MODALS (With interactive GitHub Repository Links)
// -------------------------------------------------------------
function openModal(category) {
  modalOverlay.classList.remove("hidden");

  if (category === "about") {
    modalBody.innerHTML = `
      <h3 class="modal-title"><i data-lucide="user"></i> About Naushin</h3>
      <p class="modal-content-text" style="font-family: monospace;">
        Email: <span style="color:#f1f5f9;">${profileData?.email || "naushinalam786@gmail.com"}</span><br>
        Location: <span style="color:#f1f5f9;">${profileData?.location || "Durgapur, West Bengal"}</span><br>
        Links: <a href="https://github.com/naushinalam1105" target="_blank" style="color:#34d399;">GitHub</a> | 
               <a href="https://linkedin.com/in/naushin-14384b375" target="_blank" style="color:#34d399;">LinkedIn</a>
      </p>
      <p class="modal-content-text" style="padding-top: 8px;">
        ${profileData?.summary || "AI Full Stack Engineer and Computer Science undergraduate specializing in high-performance web architectures, Generative AI orchestration, and asynchronous REST APIs."}
      </p>
    `;
  } 
  else if (category === "skills") {
    const skillsList = profileData?.skills
      ? profileData.skills.map(skill => `<span class="skill-badge">${skill}</span>`).join("")
      : "<p class='modal-content-text'>No skills loaded.</p>";

    modalBody.innerHTML = `
      <h3 class="modal-title"><i data-lucide="code-2"></i> Technical Stack & Tools</h3>
      <div class="chips-container">${skillsList}</div>
    `;
  } 
  else if (category === "projects") {
    const projectsList = profileData?.projects
      ? profileData.projects.map(item => `
          <div class="item-card" style="margin-top: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px;">
              <span style="font-weight: 600; color: #34d399;">${item.title}</span>
              ${item.github_url ? `
                <a href="${item.github_url}" target="_blank" style="color: #6ee7b7; font-size: 11px; display: inline-flex; align-items: center; gap: 4px; text-decoration: none; border: 1px solid rgba(52, 211, 153, 0.3); padding: 3px 8px; border-radius: 6px; background: rgba(52, 211, 153, 0.08);">
                  <i data-lucide="github" style="width: 13px; height: 13px;"></i> Code
                </a>
              ` : ''}
            </div>
            <div style="font-size: 11px; color: #64748b; font-family: monospace; margin-top: 3px;">${item.tech_stack}</div>
            <p style="font-size: 12px; color: #94a3b8; margin-top: 6px; line-height: 1.5;">${item.description}</p>
          </div>
        `).join("")
      : "<p class='modal-content-text'>No projects listed.</p>";

    modalBody.innerHTML = `
      <h3 class="modal-title"><i data-lucide="terminal"></i> Featured Projects</h3>
      <div style="margin-top: 10px;">${projectsList}</div>
    `;
  } 
  else if (category === "experience") {
    const expList = profileData?.experiences
      ? profileData.experiences.map(exp => `
          <div class="item-card" style="margin-top: 10px;">
            <div style="font-weight: 600; color: #34d399;">${exp.role} — ${exp.company}</div>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 4px; font-family: monospace;">${exp.period}</div>
            <p style="font-size: 12px; color: #94a3b8;">${exp.description}</p>
          </div>
        `).join("")
      : "<p class='modal-content-text'>No experience listed.</p>";

    modalBody.innerHTML = `
      <h3 class="modal-title"><i data-lucide="briefcase"></i> Work Experience</h3>
      <div style="margin-top: 10px;">${expList}</div>
    `;
  }
  else if (category === "certifications") {
    const certList = profileData?.certifications
      ? profileData.certifications.map(item => `<div class="item-card">${item}</div>`).join("")
      : "<p class='modal-content-text'>No certifications listed.</p>";

    modalBody.innerHTML = `
      <h3 class="modal-title"><i data-lucide="award"></i> Certifications & Credentials</h3>
      <div style="margin-top: 10px;">${certList}</div>
    `;
  }
  else if (category === "education") {
    const educationList = profileData?.education
      ? profileData.education.map(item => `<div class="item-card">${item}</div>`).join("")
      : "<p class='modal-content-text'>No education entries listed.</p>";

    modalBody.innerHTML = `
      <h3 class="modal-title"><i data-lucide="graduation-cap"></i> Education & Academics</h3>
      <div style="margin-top: 10px;">${educationList}</div>
    `;
  }

  lucide.createIcons();
}

function closeModal() {
  modalOverlay.classList.add("hidden");
}

window.addEventListener("click", (e) => {
  if (e.target === modalOverlay) closeModal();
});