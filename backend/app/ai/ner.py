"""Named Entity Recognition and skill extraction using spaCy + PhraseMatcher.

Loads en_core_web_sm and builds a PhraseMatcher with 200+ skill patterns.
Used to extract skills from both job descriptions and resume text.
Also infers experience level from text heuristics.
"""

import re
from typing import Dict, List, Set, Tuple

import spacy
from spacy.matcher import PhraseMatcher

# ────────────────────────────────────────────────────────────────────────
# Comprehensive skill patterns (200+)
# ────────────────────────────────────────────────────────────────────────
SKILL_PATTERNS: List[str] = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust",
    "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "Perl", "Lua",
    "Haskell", "Erlang", "Clojure", "Elixir", "Dart", "Julia",
    "Objective-C", "MATLAB", "SAS", "SPSS", "Stata",
    # Frontend Frameworks
    "React", "Angular", "Vue.js", "Svelte", "Next.js", "Nuxt.js",
    "HTML", "CSS", "Tailwind CSS", "Bootstrap", "Sass", "LESS",
    "jQuery", "Webpack", "Vite",
    # Backend Frameworks
    "Django", "Flask", "FastAPI", "Spring Boot", "Node.js", "Express.js",
    ".NET", "ASP.NET", "Ruby on Rails", "Laravel", "Gin", "Fiber",
    "NestJS", "Actix",
    # AI / ML / Data Science
    "Machine Learning", "Deep Learning", "NLP",
    "Natural Language Processing", "Computer Vision",
    "TensorFlow", "PyTorch", "Scikit-learn", "Keras",
    "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn",
    "NLTK", "spaCy", "Hugging Face", "OpenCV",
    "Reinforcement Learning", "Generative AI", "LLM",
    "Large Language Models", "GPT", "BERT", "Transformers",
    "Data Analysis", "Data Science", "Data Engineering",
    "Data Visualization", "Statistical Modeling",
    "Feature Engineering", "Model Deployment",
    "MLOps", "A/B Testing",
    # Databases
    "SQL", "PostgreSQL", "MongoDB", "MySQL", "Redis",
    "Elasticsearch", "SQLite", "Oracle", "Cassandra",
    "DynamoDB", "Neo4j", "MariaDB", "CouchDB",
    "Firebase", "Supabase",
    # Big Data
    "ETL", "Apache Spark", "Apache Kafka", "Hadoop",
    "Apache Flink", "Apache Airflow", "Databricks",
    "Snowflake", "BigQuery", "Redshift", "Hive",
    "Presto", "dbt",
    # Cloud Platforms
    "AWS", "Amazon Web Services", "Azure", "GCP",
    "Google Cloud", "Google Cloud Platform",
    "Heroku", "DigitalOcean", "Vercel", "Netlify",
    # DevOps & Infrastructure
    "Docker", "Kubernetes", "CI/CD", "Terraform",
    "Jenkins", "Git", "GitHub Actions", "GitLab CI",
    "Ansible", "Puppet", "Chef", "Vagrant",
    "Linux", "Unix", "Bash", "Shell Scripting",
    "Nginx", "Apache", "Prometheus", "Grafana",
    "ELK Stack", "Datadog", "New Relic",
    "Infrastructure as Code", "DevOps", "SRE",
    "Site Reliability Engineering",
    # APIs & Architecture
    "REST API", "RESTful", "GraphQL", "gRPC",
    "Microservices", "Serverless", "Event-Driven Architecture",
    "Message Queues", "RabbitMQ", "WebSocket",
    "OAuth", "JWT", "API Gateway",
    "System Design", "Design Patterns",
    # Security
    "Cybersecurity", "Penetration Testing",
    "Network Security", "OWASP", "Encryption",
    "Identity Management", "SSO",
    # Mobile Development
    "Mobile Development", "Android", "iOS",
    "React Native", "Flutter", "SwiftUI",
    "Xamarin", "Ionic", "Cordova",
    # BI & Visualization
    "Power BI", "Tableau", "Excel", "Looker",
    "Google Analytics", "Metabase",
    # Design & UX
    "Figma", "UI/UX", "Sketch", "Adobe XD",
    "Wireframing", "Prototyping",
    "User Research", "Usability Testing",
    "Adobe Photoshop", "Adobe Illustrator",
    "Premiere Pro", "After Effects",
    "Final Cut Pro", "Blender",
    # Project & Product Management
    "Agile", "Scrum", "Kanban",
    "Project Management", "Product Management",
    "JIRA", "Confluence", "Slack", "Notion", "Trello",
    "Asana", "Monday.com", "Linear",
    # Enterprise Software
    "SAP", "Salesforce", "HubSpot",
    "Zendesk", "ServiceNow",
    # Emerging Tech
    "Blockchain", "IoT", "AR/VR",
    "Web3", "Solidity", "Smart Contracts",
    "Edge Computing", "Quantum Computing",
    # Game / 3D
    "Unity", "Unreal Engine",
    # CAD / Engineering
    "AutoCAD", "SolidWorks", "CATIA",
    # Soft Skills
    "Leadership", "Communication", "Problem Solving",
    "Team Leadership", "Critical Thinking",
    "Time Management", "Collaboration",
    "Mentoring", "Strategic Planning",
    "Stakeholder Management",
    # Writing & Content
    "Technical Writing", "Public Speaking",
    "LaTeX", "Documentation",
    "Content Strategy", "Copywriting",
    # Sales & Marketing
    "Negotiation", "Sales", "Marketing",
    "SEO", "SEM", "Email Marketing",
    "Social Media Marketing", "Growth Hacking",
    "Google Ads", "Facebook Ads",
    # Testing
    "Unit Testing", "Integration Testing",
    "Test Automation", "Selenium", "Cypress",
    "Jest", "pytest", "JUnit",
    "Load Testing", "Performance Testing",
    "QA", "Quality Assurance",
]

# Experience level keywords
EXPERIENCE_LEVELS: Dict[str, List[str]] = {
    "entry": [
        "entry level", "junior", "intern", "internship",
        "graduate", "fresh graduate", "0-1 years", "0-2 years",
        "entry-level", "fresher",
    ],
    "mid": [
        "mid level", "mid-level", "intermediate",
        "2-5 years", "3-5 years", "2-4 years",
        "3+ years", "4+ years",
    ],
    "senior": [
        "senior", "lead", "principal", "staff",
        "5+ years", "5-10 years", "7+ years",
        "8+ years", "10+ years",
    ],
    "executive": [
        "director", "vp", "vice president", "c-level",
        "cto", "ceo", "cfo", "cio", "head of",
        "chief", "executive", "15+ years",
    ],
}

# Adjacency map for experience matching
EXPERIENCE_ADJACENCY: Dict[str, Set[str]] = {
    "entry": {"mid"},
    "mid": {"entry", "senior"},
    "senior": {"mid", "executive"},
    "executive": {"senior"},
}


class NERExtractor:
    """Extract skills and experience level from text using spaCy + PhraseMatcher."""

    def __init__(self) -> None:
        """Load spaCy model and build the PhraseMatcher."""
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(skill) for skill in SKILL_PATTERNS]
        self.matcher.add("SKILLS", patterns)

    def extract_skills(self, text: str) -> List[str]:
        """Extract unique skills from text using PhraseMatcher.

        Args:
            text: Raw text to extract skills from.

        Returns:
            Sorted list of unique skill names.
        """
        doc = self.nlp(text)
        matches = self.matcher(doc)

        found_skills: Set[str] = set()
        for match_id, start, end in matches:
            span_text = doc[start:end].text
            # Normalize to the canonical skill name (case-insensitive lookup)
            canonical = self._canonicalize(span_text)
            if canonical:
                found_skills.add(canonical)

        return sorted(found_skills)

    def _canonicalize(self, found: str) -> str:
        """Map a found phrase back to its canonical skill pattern name."""
        lower = found.lower()
        for pattern in SKILL_PATTERNS:
            if pattern.lower() == lower:
                return pattern
        return found

    def extract_experience_level(self, text: str) -> str:
        """Infer experience level from text using keyword matching.

        Args:
            text: Raw text (job description or resume).

        Returns:
            One of: 'entry', 'mid', 'senior', 'executive', or 'unknown'.
        """
        lower_text = text.lower()

        # Score each level by keyword matches
        scores: Dict[str, int] = {}
        for level, keywords in EXPERIENCE_LEVELS.items():
            score = 0
            for keyword in keywords:
                if keyword in lower_text:
                    score += 1
            scores[level] = score

        # Pick the level with the highest score
        best_level = max(scores, key=scores.get)  # type: ignore
        if scores[best_level] == 0:
            return "unknown"
        return best_level

    def extract_all(self, text: str) -> Dict:
        """Extract both skills and experience level from text.

        Returns:
            Dict with 'skills' (list) and 'experience_level' (str).
        """
        skills = self.extract_skills(text)
        experience_level = self.extract_experience_level(text)
        return {
            "skills": skills,
            "experience_level": experience_level,
        }

    @staticmethod
    def compute_experience_score(job_level: str, candidate_level: str) -> float:
        """Compute experience match score between job and candidate.

        Returns:
            1.0 for exact match, 0.5 for adjacent levels, 0.0 otherwise.
        """
        if job_level == "unknown" or candidate_level == "unknown":
            return 0.5  # Neutral when unknown

        if job_level == candidate_level:
            return 1.0

        adjacent = EXPERIENCE_ADJACENCY.get(job_level, set())
        if candidate_level in adjacent:
            return 0.5

        return 0.0
