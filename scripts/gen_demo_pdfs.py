"""Generate demo resume PDFs for the three test scenarios."""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT


OUTPUT_DIR = Path(__file__).parent.parent / "demo-fixtures" / "resumes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = A4
MARGIN = 2 * cm


def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "name": ParagraphStyle(
            "name",
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1a1a2e"),
            spaceAfter=4,
        ),
        "contact": ParagraphStyle(
            "contact",
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#444444"),
            spaceAfter=12,
        ),
        "section_title": ParagraphStyle(
            "section_title",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#16213e"),
            spaceBefore=14,
            spaceAfter=4,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "body",
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#333333"),
            spaceAfter=3,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontSize=10,
            leading=15,
            leftIndent=14,
            textColor=colors.HexColor("#333333"),
            spaceAfter=2,
        ),
        "job_title": ParagraphStyle(
            "job_title",
            fontSize=10,
            leading=14,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1a1a2e"),
        ),
        "date": ParagraphStyle(
            "date",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#888888"),
            spaceAfter=4,
        ),
    }
    return styles


def section(title, styles):
    return [
        Spacer(1, 0.2 * cm),
        Paragraph(title.upper(), styles["section_title"]),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"), spaceAfter=6),
    ]


def build_pdf(filename: str, story: list):
    path = OUTPUT_DIR / filename
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )
    doc.build(story)
    print(f"  ✓  {path}")


# ──────────────────────────────────────────────────────────────────
# Scenario 1: SUCCESS  — strong Python / FastAPI backend engineer
# ──────────────────────────────────────────────────────────────────
def gen_success():
    s = make_styles()
    story = []

    story.append(Paragraph("Alice Chen", s["name"]))
    story.append(Paragraph(
        "alice.chen@example.com  ·  +1 (415) 555-0101  ·  San Francisco, CA  ·  linkedin.com/in/alicechen",
        s["contact"],
    ))

    story += section("Summary", s)
    story.append(Paragraph(
        "Senior Backend Engineer with 6 years of experience building scalable Python micro-services "
        "and AI-powered pipelines. Proficient in FastAPI, LangChain, OpenAI APIs, PostgreSQL, and "
        "Kubernetes. Passionate about applying LLMs to real-world product challenges.",
        s["body"],
    ))

    story += section("Skills", s)
    skills = [
        "Languages: Python (expert), TypeScript, SQL, Bash",
        "Frameworks: FastAPI, LangChain, LangGraph, Celery, SQLAlchemy",
        "AI/ML: OpenAI API, Embeddings, RAG pipelines, Pydantic validation",
        "Infrastructure: Docker, Kubernetes, GitHub Actions, AWS (ECS, RDS, S3)",
        "Databases: PostgreSQL, Redis, SQLite, Elasticsearch",
    ]
    for sk in skills:
        story.append(Paragraph(f"• {sk}", s["bullet"]))

    story += section("Work Experience", s)

    story.append(Paragraph("Senior Backend Engineer  —  TalentAI Inc., San Francisco", s["job_title"]))
    story.append(Paragraph("March 2022 – Present", s["date"]))
    exp1 = [
        "Designed and led the AI recruitment pipeline using FastAPI + LangGraph, processing 10,000+ applications/month.",
        "Built a resume-parsing service with pdfplumber + LLM extraction, achieving 94% field accuracy.",
        "Implemented SSE-based real-time status streaming for recruiter dashboard, reducing page load wait by 60%.",
        "Introduced Pydantic v2 schemas across all API contracts, eliminating a class of runtime type errors.",
        "Mentored 3 junior engineers; ran weekly code-review sessions focused on async patterns and testing.",
    ]
    for e in exp1:
        story.append(Paragraph(f"• {e}", s["bullet"]))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Backend Engineer  —  DataBridge Solutions, Seattle", s["job_title"]))
    story.append(Paragraph("July 2019 – February 2022", s["date"]))
    exp2 = [
        "Built RESTful microservices in Python/FastAPI serving 500K+ daily requests with 99.9% uptime.",
        "Migrated legacy Django monolith to an async FastAPI architecture; cut p95 latency by 45%.",
        "Designed ETL pipelines (Celery + PostgreSQL) processing 5M records nightly.",
        "Owned CI/CD setup on GitHub Actions; achieved < 8 min build-to-deploy cycle.",
    ]
    for e in exp2:
        story.append(Paragraph(f"• {e}", s["bullet"]))

    story += section("Education", s)
    story.append(Paragraph("B.Sc. Computer Science  —  University of Washington, Seattle", s["job_title"]))
    story.append(Paragraph("September 2015 – June 2019  |  GPA 3.8 / 4.0", s["date"]))

    story += section("Certifications", s)
    certs = [
        "AWS Certified Solutions Architect – Associate (2023)",
        "Certified Kubernetes Application Developer – CNCF (2022)",
        "Deep Learning Specialization – Coursera / deeplearning.ai (2021)",
    ]
    for c in certs:
        story.append(Paragraph(f"• {c}", s["bullet"]))

    build_pdf("resume_success.pdf", story)


# ──────────────────────────────────────────────────────────────────
# Scenario 2: MATCH FAILED  — graphic designer, irrelevant background
# ──────────────────────────────────────────────────────────────────
def gen_match_failed():
    s = make_styles()
    story = []

    story.append(Paragraph("Marco Rivera", s["name"]))
    story.append(Paragraph(
        "marco.rivera@example.com  ·  +34 612 345 678  ·  Barcelona, Spain",
        s["contact"],
    ))

    story += section("Summary", s)
    story.append(Paragraph(
        "Creative Graphic Designer and Illustrator with 8 years of experience in brand identity, "
        "editorial design, and digital illustration. Passionate about visual storytelling and "
        "human-centered aesthetics. No programming background.",
        s["body"],
    ))

    story += section("Skills", s)
    skills = [
        "Design Tools: Adobe Illustrator (expert), Photoshop, InDesign, Figma, Procreate",
        "Disciplines: Brand Identity, Typography, Editorial Layout, Motion Graphics",
        "Other: Color Theory, UX Wireframing (conceptual), Client Presentations",
    ]
    for sk in skills:
        story.append(Paragraph(f"• {sk}", s["bullet"]))

    story += section("Work Experience", s)

    story.append(Paragraph("Senior Graphic Designer  —  Vivid Studio, Barcelona", s["job_title"]))
    story.append(Paragraph("January 2020 – Present", s["date"]))
    exp1 = [
        "Led visual identity projects for 30+ clients across fashion, hospitality, and FMCG sectors.",
        "Produced editorial illustrations for monthly magazine circulation of 200,000 copies.",
        "Directed junior designers on multi-brand campaigns and maintained brand guidelines.",
    ]
    for e in exp1:
        story.append(Paragraph(f"• {e}", s["bullet"]))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Junior Illustrator  —  Pixel & Ink Agency, Madrid", s["job_title"]))
    story.append(Paragraph("August 2016 – December 2019", s["date"]))
    exp2 = [
        "Created character illustrations and storyboards for advertising campaigns.",
        "Collaborated with copywriters to produce cohesive print and digital assets.",
    ]
    for e in exp2:
        story.append(Paragraph(f"• {e}", s["bullet"]))

    story += section("Education", s)
    story.append(Paragraph("B.F.A. Graphic Design  —  Escola Massana, Barcelona", s["job_title"]))
    story.append(Paragraph("September 2012 – June 2016", s["date"]))

    build_pdf("resume_match_failed.pdf", story)


# ──────────────────────────────────────────────────────────────────
# Scenario 3: MISSING REQUIRED FIELD  — missing email address
# ──────────────────────────────────────────────────────────────────
def gen_missing_required():
    s = make_styles()
    story = []

    story.append(Paragraph("Jordan Kim", s["name"]))
    # Intentionally omit email; only phone and location
    story.append(Paragraph(
        "+82 10-5555-7890  ·  Seoul, South Korea  ·  github.com/jordankim",
        s["contact"],
    ))

    story += section("Summary", s)
    story.append(Paragraph(
        "Full-stack developer with 4 years of experience in React and Node.js. "
        "Comfortable working across the stack with a focus on clean component architecture "
        "and RESTful API design.",
        s["body"],
    ))

    story += section("Skills", s)
    skills = [
        "Frontend: React, TypeScript, Next.js, Tailwind CSS, Vite",
        "Backend: Node.js, Express, REST APIs",
        "Databases: MongoDB, MySQL",
        "Tools: Git, GitHub Actions, Vercel, Figma",
    ]
    for sk in skills:
        story.append(Paragraph(f"• {sk}", s["bullet"]))

    story += section("Work Experience", s)

    story.append(Paragraph("Frontend Developer  —  Shopify Partner Agency, Seoul", s["job_title"]))
    story.append(Paragraph("June 2021 – Present", s["date"]))
    exp1 = [
        "Built and maintained Shopify storefronts using React + Liquid for 15+ e-commerce clients.",
        "Reduced page bundle size by 35% through code splitting and lazy loading.",
        "Implemented CI pipelines on GitHub Actions for automated testing and preview deployments.",
    ]
    for e in exp1:
        story.append(Paragraph(f"• {e}", s["bullet"]))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Junior Web Developer  —  KDigital Lab, Seoul", s["job_title"]))
    story.append(Paragraph("March 2020 – May 2021", s["date"]))
    exp2 = [
        "Developed internal admin dashboards with React and Node.js/Express.",
        "Integrated third-party APIs (payments, logistics) and wrote integration tests.",
    ]
    for e in exp2:
        story.append(Paragraph(f"• {e}", s["bullet"]))

    story += section("Education", s)
    story.append(Paragraph("B.Eng. Software Engineering  —  Korea University, Seoul", s["job_title"]))
    story.append(Paragraph("March 2016 – February 2020", s["date"]))

    story += section("Note", s)
    story.append(Paragraph(
        "Contact email intentionally omitted from this resume to simulate a 'missing required field' "
        "scenario in the AI recruitment pipeline validation flow.",
        s["body"],
    ))

    build_pdf("resume_missing_required.pdf", story)


if __name__ == "__main__":
    print("Generating demo PDFs …")
    gen_success()
    gen_match_failed()
    gen_missing_required()
    print("Done. Files saved to demo-fixtures/resumes/")
