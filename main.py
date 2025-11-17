import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List

from database import db, create_document, get_documents
from schemas import (
    Inquiry,
    Jobapplication,
    Service,
    Project,
    Testimonial,
    Blogpost,
    Opening,
)

app = FastAPI(title="Flames Site API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Flames API running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": [],
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, "name") else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:20]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


# Helper: ensure demo content exists for first run
DEFAULT_SERVICES = [
    {
        "name": "Web Development",
        "slug": "web-development",
        "summary": "High-performance websites using modern stacks.",
        "features": [
            "Responsive UI",
            "SEO-friendly",
            "CMS integration",
            "Performance optimized",
        ],
        "icon": "Globe",
    },
    {
        "name": "App Development",
        "slug": "app-development",
        "summary": "iOS/Android apps with native performance.",
        "features": ["React Native / Flutter", "App Store / Play Store", "Analytics"],
        "icon": "Smartphone",
    },
    {
        "name": "Digital Marketing",
        "slug": "digital-marketing",
        "summary": "Growth-focused SEO, SEM and social campaigns.",
        "features": ["SEO Audits", "Paid Ads", "Content Strategy"],
        "icon": "Megaphone",
    },
    {
        "name": "Software Development",
        "slug": "software-development",
        "summary": "Custom software and integrations for your business.",
        "features": ["APIs", "Internal tools", "Automation"],
        "icon": "Code2",
    },
    {
        "name": "Cloud & DevOps",
        "slug": "cloud-devops",
        "summary": "Infra, CI/CD, scaling and reliability.",
        "features": ["AWS/GCP", "Docker/K8s", "Monitoring"],
        "icon": "Cloud",
    },
    {
        "name": "AI & Automation",
        "slug": "ai-automation",
        "summary": "AI copilots, data pipelines and process automation.",
        "features": ["LLM apps", "RAG", "Workflow automation"],
        "icon": "Bot",
    },
]

DEFAULT_TESTIMONIALS = [
    {
        "author": "Alex Morgan",
        "role": "CTO",
        "company": "FinEdge",
        "quote": "They delivered a blazing-fast product ahead of schedule.",
        "rating": 5,
    },
    {
        "author": "Priya Sharma",
        "role": "Founder",
        "company": "Wellnest",
        "quote": "Our growth doubled after the new website and campaigns.",
        "rating": 5,
    },
]

DEFAULT_PROJECTS = [
    {
        "title": "E‑commerce Revamp",
        "slug": "ecommerce-revamp",
        "summary": "+38% conversion with headless storefront",
        "results": "+38% conversion | 1.8s LCP",
        "tags": ["Next.js", "Stripe", "Headless"],
    },
    {
        "title": "AI Support Copilot",
        "slug": "ai-support-copilot",
        "summary": "Reduced ticket time by 42%",
        "results": "42% faster responses",
        "tags": ["Python", "LLM", "RAG"],
    },
]

DEFAULT_BLOGPOSTS = [
    {
        "title": "Choosing the Right Web Stack in 2025",
        "slug": "choosing-the-right-web-stack-2025",
        "excerpt": "SPA vs. MPA, SSR vs. SSG — what actually matters.",
        "content": "Long-form content...",
        "tags": ["Web", "Architecture"],
        "author": "Team",
    }
]

DEFAULT_OPENINGS = [
    {
        "title": "Frontend Engineer",
        "department": "Engineering",
        "location": "Remote",
        "type": "Full-time",
        "description": "React, TypeScript, Tailwind",
        "requirements": ["3+ years experience", "Strong UX sense"],
    }
]


def ensure_defaults():
    if db is None:
        return
    try:
        if db["service"].count_documents({}) == 0:
            db["service"].insert_many(DEFAULT_SERVICES)
        if db["testimonial"].count_documents({}) == 0:
            db["testimonial"].insert_many(DEFAULT_TESTIMONIALS)
        if db["project"].count_documents({}) == 0:
            db["project"].insert_many(DEFAULT_PROJECTS)
        if db["blogpost"].count_documents({}) == 0:
            db["blogpost"].insert_many(DEFAULT_BLOGPOSTS)
        if db["opening"].count_documents({}) == 0:
            db["opening"].insert_many(DEFAULT_OPENINGS)
    except Exception:
        pass


ensure_defaults()


@app.get("/schema")
def get_schema() -> Dict[str, Any]:
    # Return schema info for the admin viewer
    models = [Inquiry, Jobapplication, Service, Project, Testimonial, Blogpost, Opening]
    return {m.__name__.lower(): m.model_json_schema() for m in models}


# Content queries
@app.get("/services", response_model=List[Service])
def list_services():
    docs = get_documents("service") if db else DEFAULT_SERVICES
    return [Service(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


@app.get("/services/{slug}", response_model=Service)
def get_service(slug: str):
    if db is None:
        for d in DEFAULT_SERVICES:
            if d["slug"] == slug:
                return Service(**d)
        raise HTTPException(status_code=404, detail="Service not found")
    doc = db["service"].find_one({"slug": slug})
    if not doc:
        raise HTTPException(status_code=404, detail="Service not found")
    doc.pop("_id", None)
    return Service(**doc)


@app.get("/projects", response_model=List[Project])
def list_projects():
    docs = get_documents("project") if db else DEFAULT_PROJECTS
    return [Project(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


@app.get("/testimonials", response_model=List[Testimonial])
def list_testimonials():
    docs = get_documents("testimonial") if db else DEFAULT_TESTIMONIALS
    return [Testimonial(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


@app.get("/blogposts", response_model=List[Blogpost])
def list_blogposts():
    docs = get_documents("blogpost") if db else DEFAULT_BLOGPOSTS
    return [Blogpost(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


@app.get("/blogposts/{slug}", response_model=Blogpost)
def get_blogpost(slug: str):
    if db is None:
        for d in DEFAULT_BLOGPOSTS:
            if d["slug"] == slug:
                return Blogpost(**d)
        raise HTTPException(status_code=404, detail="Post not found")
    doc = db["blogpost"].find_one({"slug": slug})
    if not doc:
        raise HTTPException(status_code=404, detail="Post not found")
    doc.pop("_id", None)
    return Blogpost(**doc)


@app.get("/openings", response_model=List[Opening])
def list_openings():
    docs = get_documents("opening") if db else DEFAULT_OPENINGS
    return [Opening(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


# Lead capture
@app.post("/inquiries")
def create_inquiry(payload: Inquiry):
    try:
        _id = create_document("inquiry", payload)
        return {"status": "ok", "id": _id}
    except Exception as e:
        # Still accept in demo mode without DB
        if db is None:
            return {"status": "ok", "id": "demo"}
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/jobapplications")
def create_job_application(payload: Jobapplication):
    try:
        _id = create_document("jobapplication", payload)
        return {"status": "ok", "id": _id}
    except Exception as e:
        if db is None:
            return {"status": "ok", "id": "demo"}
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
