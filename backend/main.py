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

PROFESSIONAL SUMMARY:
B.Tech Computer Science & Engineering student (graduating May 2028) with hands-on experience in frontend AI engineering, full-stack web development, and responsive UI design.

TECHNICAL SKILLS:
- Languages: Python, Java, C, JavaScript, SQL
- Frontend: HTML5, CSS3, JavaScript (ES6+), React.js, Tailwind CSS
- Backend & Databases: Node.js, Flask, SQLite, MySQL
- Tools & Design: Git, GitHub, VS Code, Figma, UI/UX Design Systems

INTERNSHIPS & WORK EXPERIENCE:
- Frontend AI Engineering Intern at FlyRank AI (Jun 2026 – Present): Developed responsive web interfaces for AI-driven features and real-time user workflows.
- Web Developer Intern at InAmigos Foundation (May 2026 – Jun 2026): Built mobile-responsive components, optimized client-side performance, and refined UI designs.
- Full-Stack Web Developer Intern at Future Interns (Apr 2026 – May 2026): Delivered end-to-end web applications with JavaScript, Node.js, Flask, and SQLite, implementing client/server-side validations.

KEY PROJECTS:
- Carbon Footprint Tracker Platform: Interactive web dashboard built with JavaScript, HTML5, and Tailwind CSS to track and visualize carbon emissions.
- Mini CRM System: Full-stack solution using JavaScript, Python, Node.js, and SQLite with complete CRUD workflows for client management.
- Starcups Web Interface: Responsive digital coffee shop UI designed with modern CSS and JavaScript.
- AI Interactive Portfolio: Full-stack AI-driven personal portfolio featuring real-time conversational intelligence powered by FastAPI and Groq LLM inference.

EDUCATION & ACADEMICS:
- Bachelor of Technology (B.Tech) in Computer Science & Engineering (2024 – 2028)
  * 1st Year CGPA: 9.48
  * 2nd Year CGPA: 9.92
- Senior Secondary (Class XII): 83.00% (CBSE)
- Secondary (Class X): 93.80% (CBSE)

CERTIFICATIONS & ACHIEVEMENTS:
- Microsoft Certified: AI-901 Azure AI Fundamentals
- Simplilearn Professional Course Completion in Full-Stack Web Development
- AR/VR Seminar & Emerging Technologies Workshop Completion

ACTIVITIES, INTERESTS & HOBBIES:
- Photography, visual framing, and digital aesthetics.
- UI/UX conceptual design, prototyping, and modern interface styling.
- Exploring emerging AI tools, LLM integrations, and frontend architectures.
- Participating in technical workshops, hackathons, and collaborative open-source learning.
"""

class Experience(BaseModel):
    role: str
    company: str
    period: str
    description: str

class Resume(BaseModel):
    name: str = "Naushin"
    email: str = "naushinalam786@gmail.com"
    location: str = "Durgapur, West Bengal, India"
    summary: str = ""
    skills: list[str] = Field(default_factory=list)
    experiences: list[Experience] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)

class QueryRequest(BaseModel):
    message: str

def parse_resume(profile_text: str) -> Resume:
    prompt = f"""
Extract and structure the following profile text into valid JSON matching this schema:
{{
  "name": "Naushin",
  "email": "string",
  "phone": "string",
  "location": "string",
  "summary": "string",
  "skills": ["string"],
  "experiences": [{{"role": "string", "company": "string", "period": "string", "description": "string"}}],
  "projects": ["string"],
  "education": ["string"],
  "achievements": ["string"],
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
            summary="Computer Science & Engineering student with experience in frontend AI engineering and full-stack web development.",
            skills=["Python", "Java", "C", "JavaScript", "HTML5", "CSS3", "React.js", "Tailwind CSS", "Node.js", "Flask", "SQLite", "MySQL", "Git", "Figma"],
            experiences=[
                Experience(role="Frontend AI Engineering Intern", company="FlyRank AI", period="Jun 2026 – Present", description="Built responsive web interfaces for AI-driven features."),
                Experience(role="Web Developer Intern", company="InAmigos Foundation", period="May 2026 – Jun 2026", description="Developed mobile-responsive UI components and design systems."),
                Experience(role="Full-Stack Web Developer Intern", company="Future Interns", period="Apr 2026 – May 2026", description="Delivered full-stack web applications with Node.js, Flask, and SQLite.")
            ],
            projects=[
                "Carbon Footprint Tracker: Web platform built with JavaScript and Tailwind CSS.",
                "Mini CRM System: Full-stack solution using JavaScript, Python, and SQLite.",
                "Starcups Web Interface: Modern responsive UI designed with CSS and JavaScript.",
                "AI Interactive Portfolio: Full-stack AI-driven personal portfolio powered by FastAPI and Groq."
            ],
            education=[
                "B.Tech in Computer Science & Engineering (2024 – 2028) — 1st Year CGPA: 9.48 | 2nd Year CGPA: 9.92",
                "Senior Secondary (Class XII): 83.00% (CBSE)",
                "Secondary (Class X): 93.80% (CBSE)"
            ],
            achievements=[
                "Microsoft Certified: AI-901 Azure AI Fundamentals",
                "Simplilearn Professional Course Completion in Full-Stack Web Development",
                "AR/VR Seminar & Emerging Technologies Workshop Completion"
            ],
            interests=[
                "Photography, visual framing, and digital aesthetics",
                "UI/UX conceptual design, prototyping, and modern interface styling",
                "Exploring emerging AI tools, LLM integrations, and frontend architectures",
                "Participating in technical workshops, hackathons, and collaborative open-source learning"
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
   - "Hobbies", "Passions", "Interests", "Leisure", "Activities", "What does she do outside coding" -> Answer using Naushin's Activities, Interests & Hobbies.
   - "Achievements", "Awards", "Recognitions", "Certificates", "Credentials" -> Answer using Certifications, Honors, and Key Achievements.
   - "Stack", "Tools", "Technologies", "Tech stack", "What does she code in" -> Answer using Technical Skills and Languages.
   - "Background", "Bio", "About", "Summary", "Who is she" -> Answer using Professional Summary, Education, and Core Highlights.
   - "Work", "Jobs", "Roles", "Employment", "Experience" -> Answer using Internships and Professional Experience.
   - "Projects", "What has she built", "Innovations" -> Answer using Key Projects.

2. ACCURACY & CONSTRAINTS:
   - Always speak strictly in the third person ("Naushin is...", "Her experience includes...", "She has developed..."). Never use "I", "my", or "me".
   - Direct Scope Relevance: Answer ONLY the category asked without unnecessarily mixing unrequested sections.
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