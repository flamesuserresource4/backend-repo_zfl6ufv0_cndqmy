"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogpost" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List

# Core marketing website schemas

class Inquiry(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    subject: Optional[str] = Field(None, description="Subject of inquiry")
    message: str = Field(..., description="Message body")
    service: Optional[str] = Field(None, description="Service of interest")
    source: Optional[str] = Field(None, description="Lead source, e.g., website, whatsapp")

class Opening(BaseModel):
    title: str
    department: str
    location: str = Field("Remote")
    type: str = Field("Full-time", description="Employment type")
    description: Optional[str] = None
    requirements: List[str] = Field(default_factory=list)

class Jobapplication(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str = Field(..., description="Role applied for")
    resume_url: Optional[HttpUrl] = Field(None, description="Link to resume (Drive/Dropbox)")
    portfolio_url: Optional[HttpUrl] = None
    cover_letter: Optional[str] = None

class Blogpost(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: str
    tags: List[str] = Field(default_factory=list)
    author: Optional[str] = Field("Team")

class Service(BaseModel):
    name: str
    slug: str
    summary: str
    features: List[str] = Field(default_factory=list)
    icon: Optional[str] = Field(None, description="Icon name from lucide-react")

class Project(BaseModel):
    title: str
    slug: str
    summary: str
    results: Optional[str] = None
    before_image: Optional[HttpUrl] = None
    after_image: Optional[HttpUrl] = None
    tags: List[str] = Field(default_factory=list)

class Testimonial(BaseModel):
    author: str
    role: Optional[str] = None
    company: Optional[str] = None
    quote: str
    rating: Optional[int] = Field(5, ge=1, le=5)

# Legacy examples kept for reference
class User(BaseModel):
    name: str
    email: EmailStr
    address: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: bool = Field(True)

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category: str
    in_stock: bool = Field(True)
