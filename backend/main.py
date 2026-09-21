import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=GROQ_API_KEY)
model = "openai/gpt-oss-120b"
app = FastAPI(title="Naushin AI Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PERSONAL_PROFILE = """
CANDIDATE: Naushin
EMAIL: naushinalam786@gmail.com
LOCATION: Durgapur, West Bengal, India
LINKS: linkedin.com/in/naushin-14384b375 | github.com/naushinalam1105

PROFESSIONAL SUMMARY:
Results-driven AI Full Stack Engineer and Computer Science undergraduate specializing in high-performance web architectures, Generative AI orchestration, and scalable cloud microservices. Hands-on expertise building asynchronous REST APIs using Python, FastAPI, Pydantic, and Uvicorn, alongside responsive, modern frontends with React.js and Tailwind CSS. Adept at LLM integration (Groq API, prompt engineering), full-stack data persistence, and end-to-end pipeline deployment.

EDUCATION & ACADEMICS:
- Dr. B.C. Roy Engineering College, Durgapur, WB: B.Tech in Computer Science & Engineering (Expected Graduation: May 2028)
  * 1st Year CGPA: 9.48
  * 2nd Year CGPA: 9.92
- Kendriya Vidyalaya (CBSE):
  * Senior Secondary (Class XII): 83.00%
  * Secondary (Class X): 93.80%

TECHNICAL SKILLS:
- Languages: Python, JavaScript (ES6+), Java, C, SQL, HTML5, CSS3
- AI & Machine Learning: Groq LLM API, Prompt Engineering, Agentic AI, REST API LLM Inference, Context Optimization
- Backend & Runtimes: FastAPI, Uvicorn, Pydantic, Node.js, Express.js, Flask
- Frontend Technologies: React.js, Vite, Tailwind CSS (v4), Recharts Data Visualization, Lucide React
- Databases & Cloud: MongoDB Atlas, MySQL, SQLite, Render, Vercel, Microsoft Azure
- Tools & Core Engineering: Data Structures & Algorithms (DSA), Git, GitHub, UI/UX (Figma), AutoCAD (3D Printing)

PROFESSIONAL EXPERIENCE:
- Frontend AI Engineering Intern at FlyRank AI (Jun 2026 – Sep 2026):
  * Developed and maintained scalable, responsive client interfaces for AI workflows, converting Figma system designs into modular React components.
  * Integrated asynchronous client-side applications with high-throughput backend endpoints, reducing latency in interactive AI features.
  * Conducted performance audits and DOM render optimizations to accelerate user interactions across dynamic AI interfaces.
- Web Developer Intern (Hybrid) at InAmigos Foundation (IAF) (May 2026 – Jun 2026):
  * Built mobile-first responsive web modules, enhancing platform layout consistency and visual accessibility across diverse viewports.
  * Partnered with UI/UX teams to modernize core page components, streamlining CSS utility layouts for faster overall load speeds.

KEY PROJECTS:
- Carbon Footprint & Eco-Impact Tracker Platform:
  * Tech Stack: React, Vite, Tailwind CSS v4, Recharts, Lucide React
  * GitHub: https://github.com/naushinalam1105/carbon-footprint-tracker
  * Details: Real-time environmental tracking dashboard tracking transit profiles, electricity metrics, dietary models, and domestic waste with Recharts sandboxes.
- AI-Powered Interactive Portfolio & Assistant:
  * Tech Stack: Python, FastAPI, Uvicorn, Pydantic, Groq LLM, JavaScript
  * GitHub: https://github.com/naushinalam1105/Ai-interactive-portfolio
  * Details: Full-stack AI portfolio with an integrated conversational agent driven by Groq LLM API, strict Pydantic schema validation, and sub-400ms latency.
- Full-Stack Mini CRM Platform:
  * Tech Stack: React.js, Vite, Tailwind CSS, Node.js, Express.js, MongoDB Atlas
  * GitHub: https://github.com/naushinalam1105/fullstack_MiniCRM
  * Details: End-to-end MERN architecture handling client pipeline management with full CRUD operations, lead conversion tracking, and multi-cloud deployment.

CERTIFICATIONS:
- Agentic AI Foundation Associate – Oracle
- Microsoft Certified: Azure AI Fundamentals – Microsoft
- Google Prompting Essentials – Google
- 3D Printing & Additive Manufacturing (160 Hours) – C-DAC, MeitY
- Data Visualisation: Empowering Business – Tata (Forage)
- Cybersecurity Job Simulation – Deloitte (Forage)

ACHIEVEMENTS & LEADERSHIP:
- Secretary at Dezinova Club (Jul 2025 – Present): Lead departmental project showcases, schedule tech events, and coordinate operational student logistics.
- 2nd Rank at Horizon Techfest: Achieved 2nd place in the Virtual Visionary Battles technical competition.

ACTIVITIES, INTERESTS & HOBBIES:
- UI/UX conceptual design, design systems, and prototyping in Figma.
- 3D printing and digital fabrication exploring AutoCAD models.
- Generative AI architectures, prompt optimization, and agentic workflows.
- Technical leadership, organizing student hackathons, and departmental tech fests.
"""

class Experience(BaseModel):
    role: str
    company: str
    period: str
    description: str

class Project(BaseModel):
    title: str
    tech_stack: str
    description: str
    github_url: str

class Resume(BaseModel):
    name: str = "Naushin"
    email: str = "naushinalam786@gmail.com"
    location: str = "Durgapur, West Bengal, India"
    summary: str = ""
    skills: list[str] = Field(default_factory=list)
    experiences: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)

class QueryRequest(BaseModel):
    message: str

def parse_resume(profile_text: str) -> Resume:
    prompt = f"""
Extract and structure the following candidate profile text into valid JSON strictly matching this schema:
{{
  "name": "Naushin",
  "email": "string",
  "location": "string",
  "summary": "string",
  "skills": ["string"],
  "experiences": [{{"role": "string", "company": "string", "period": "string", "description": "string"}}],
  "projects": [{{"title": "string", "tech_stack": "string", "description": "string", "github_url": "string"}}],
  "education": ["string"],
  "achievements": ["string"],
  "certifications": ["string"],
  "interests": ["string"]
}}

Profile Text:
{profile_text}

Return ONLY clean, valid JSON with no markdown formatting or extra text.
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a precise data extraction system that outputs valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        return Resume.model_validate_json(content)
    except Exception:
        return Resume(
            name="Naushin",
            email="naushinalam786@gmail.com",
            location="Durgapur, West Bengal, India",
            summary="AI Full Stack Engineer and Computer Science undergraduate specializing in high-performance web architectures, Generative AI orchestration, asynchronous REST APIs (FastAPI), and modern frontends (React.js, Tailwind CSS).",
            skills=[
                "Python", "JavaScript (ES6+)", "Java", "C", "SQL", "HTML5", "CSS3",
                "FastAPI", "Uvicorn", "Pydantic", "Node.js", "Express.js", "Flask",
                "React.js", "Vite", "Tailwind CSS v4", "Recharts", "Lucide React",
                "MongoDB Atlas", "MySQL", "SQLite", "Render", "Vercel", "Microsoft Azure",
                "Groq LLM API", "Prompt Engineering", "Agentic AI", "Figma", "AutoCAD (3D Printing)"
            ],
            experiences=[
                Experience(
                    role="Frontend AI Engineering Intern",
                    company="FlyRank AI",
                    period="Jun 2026 – Sep 2026",
                    description="Developed and maintained scalable client interfaces for AI workflows, converting Figma designs to React and optimizing DOM rendering."
                ),
                Experience(
                    role="Web Developer Intern (Hybrid)",
                    company="InAmigos Foundation (IAF)",
                    period="May 2026 – Jun 2026",
                    description="Engineered mobile-first responsive web modules and modernized core page components for improved load performance."
                )
            ],
            projects=[
                Project(
                    title="Carbon Footprint & Eco-Impact Tracker Platform",
                    tech_stack="React, Vite, Tailwind CSS v4, Recharts, Lucide React",
                    description="Real-time environmental calculation dashboard tracking emissions with live Recharts offset simulation models.",
                    github_url="https://github.com/naushinalam1105/carbon-footprint-tracker"
                ),
                Project(
                    title="AI-Powered Interactive Portfolio & Assistant",
                    tech_stack="Python, FastAPI, Uvicorn, Pydantic, Groq LLM, Vanilla JS",
                    description="Full-stack AI portfolio with an integrated conversational agent driven by Groq LLM API and sub-400ms latency.",
                    github_url="https://github.com/naushinalam1105/Ai-interactive-portfolio"[cite: 2]
                ),
                Project(
                    title="Full-Stack Mini CRM Platform",
                    tech_stack="React.js, Vite, Tailwind CSS, Node.js, Express.js, MongoDB Atlas",
                    description="End-to-end MERN architecture handling client pipeline management with complete CRUD operations and conversion analytics.",
                    github_url="https://github.com/naushinalam1105/fullstack_MiniCRM"
                )
            ],
            education=[
                "B.Tech in Computer Science & Engineering, Dr. B.C. Roy Engineering College (2024 – 2028) — 1st Yr CGPA: 9.48 | 2nd Yr CGPA: 9.92",
                "Senior Secondary (Class XII), Kendriya Vidyalaya: 83.00%",
                "Secondary (Class X), Kendriya Vidyalaya: 93.80%"
            ],
            certifications=[
                "Agentic AI Foundation Associate – Oracle",
                "Microsoft Certified: Azure AI Fundamentals – Microsoft",
                "Google Prompting Essentials – Google",
                "3D Printing & Additive Manufacturing (160 Hours) – C-DAC, MeitY",
                "Data Visualisation: Empowering Business – Tata (Forage)",
                "Cybersecurity Job Simulation – Deloitte (Forage)"
            ],
            achievements=[
                "Secretary – Dezinova Club (Jul 2025 – Present): Lead departmental showcases and student tech events.",
                "2nd Rank – Horizon Techfest: Virtual Visionary Battles technical competition."
            ],
            interests=[
                "UI/UX conceptual design, system styling, and prototyping in Figma",
                "3D printing, CAD modeling, and digital additive manufacturing",
                "Generative AI orchestration and Agentic AI architectures",
                "Technical leadership and tech community event organization"
            ]
        )

PARSED_RESUME_DATA = parse_resume(PERSONAL_PROFILE)

def ask_candidate(question: str, resume: Resume) -> str:
    system_prompt = f"""
You are the official AI Assistant representing Naushin (The candidate's name is strictly spelled "Naushin").

Candidate Knowledge Base:
{resume.model_dump_json(indent=2)}

Core Operating Guidelines:
1. SEMANTIC SYNONYM MATCHING & INTENT UNDERSTANDING:
   - "Projects", "Portfolio", "What has she built", "Code", "GitHub repo", "Repositories" -> Provide details on her key projects and ALWAYS include the project's direct clickable markdown link (e.g. [View GitHub Repository](url)).
   - "CGPA", "GPA", "Marks", "Grades", "Academic performance", "College", "Schooling" -> Answer using Naushin's B.Tech CGPAs (1st Year: 9.48, 2nd Year: 9.92) and CBSE scores (Class XII: 83%, Class X: 93.8%).
   - "Hobbies", "Passions", "Interests", "Leisure", "Activities" -> Answer using Naushin's Interests, Club Leadership (Dezinova Club), and 3D printing pursuits.
   - "Certifications", "Credentials", "Licenses", "Courses" -> Answer using her official certifications.
   - "Achievements", "Awards", "Competitions", "Rank" -> Answer using her Horizon Techfest 2nd Rank and Dezinova Club Secretary leadership.
   - "Stack", "Tools", "Technologies", "Tech stack" -> Answer using her technical skills categorized by Languages, AI/ML, Backend, Frontend, and Cloud/Databases.
   - "Background", "Bio", "About", "Summary" -> Answer using Professional Summary, College, and Core Engineering Focus.
   - "Work", "Jobs", "Roles", "Employment", "Internships" -> Answer using FlyRank AI and InAmigos Foundation.

2. ACCURACY & CONSTRAINTS:
   - Always speak strictly in the third person ("Naushin is...", "Her experience includes..."). Never use "I", "my", or "me".
   - Direct Scope Relevance: Answer only the category asked without mixing unrequested sections.
   - Format responses cleanly with concise bullet points and bold key terms.
   - If a topic has zero related context in the profile, politely reply: "I don't have information regarding that in Naushin's profile."
"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

@app.get("/")
def root():
    return {"status": "online", "candidate": "Naushin", "agent": "Naushin AI Portfolio Assistant"}

@app.get("/profile")
def get_profile():
    return PARSED_RESUME_DATA

@app.post("/generate")
def generate_answer(req: QueryRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Query message cannot be empty.")
    reply = ask_candidate(req.message, PARSED_RESUME_DATA)
    return {"reply": reply}