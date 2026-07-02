"""Resume parser for extracting text from PDF and DOCX files.

Uses pdfplumber for PDF text extraction and python-docx for DOCX.
Includes basic heuristic extraction of name, email, phone, education
and experience sections from raw text.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

import pdfplumber
from docx import Document


class ResumeParser:
    """Extract structured data from resume files (PDF / DOCX)."""

    # Regex patterns for contact info
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
    PHONE_PATTERN = re.compile(
        r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"
    )

    # Section headers used for heuristic section splitting
    EXPERIENCE_HEADERS = [
        "experience", "work experience", "professional experience",
        "employment history", "work history", "career history",
        "professional background",
    ]
    EDUCATION_HEADERS = [
        "education", "academic background", "qualifications",
        "academic qualifications", "educational background",
        "degrees", "certifications",
    ]

    def extract_text(self, file_path: str) -> str:
        """Extract raw text from a PDF or DOCX file.

        Args:
            file_path: Absolute or relative path to the resume file.

        Returns:
            Extracted raw text as a single string.

        Raises:
            ValueError: If the file format is not supported.
        """
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return self._extract_pdf(path)
        elif suffix in (".docx", ".doc"):
            return self._extract_docx(path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    def _extract_pdf(self, path: Path) -> str:
        """Extract text from a PDF file using pdfplumber."""
        pages_text: List[str] = []
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
        return "\n".join(pages_text)

    def _extract_docx(self, path: Path) -> str:
        """Extract text from a DOCX file using python-docx."""
        doc = Document(str(path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)

    def parse(self, file_path: str) -> Dict:
        """Parse a resume file and extract structured information.

        Returns a dictionary with keys:
            raw_text, name, email, phone, experience, education
        """
        raw_text = self.extract_text(file_path)
        return self.parse_text(raw_text)

    def parse_text(self, raw_text: str) -> Dict:
        """Parse raw resume text into structured fields."""
        name = self._extract_name(raw_text)
        email = self._extract_email(raw_text)
        phone = self._extract_phone(raw_text)
        experience = self._extract_section(raw_text, self.EXPERIENCE_HEADERS)
        education = self._extract_section(raw_text, self.EDUCATION_HEADERS)

        return {
            "raw_text": raw_text,
            "name": name,
            "email": email,
            "phone": phone,
            "experience": experience,
            "education": education,
        }

    def _extract_name(self, text: str) -> str:
        """Heuristic: first non-empty line is usually the candidate's name."""
        lines = text.strip().split("\n")
        for line in lines:
            cleaned = line.strip()
            # Skip lines that look like email, phone, or URLs
            if cleaned and not self.EMAIL_PATTERN.search(cleaned) and \
               not cleaned.startswith("http") and len(cleaned) < 80:
                # Likely a name if it doesn't have too many words
                words = cleaned.split()
                if 1 <= len(words) <= 5:
                    return cleaned
        return "Unknown Candidate"

    def _extract_email(self, text: str) -> Optional[str]:
        """Extract first email address from text."""
        match = self.EMAIL_PATTERN.search(text)
        return match.group(0) if match else None

    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract first phone number from text."""
        match = self.PHONE_PATTERN.search(text)
        return match.group(0).strip() if match else None

    def _extract_section(self, text: str, headers: List[str]) -> List[str]:
        """Extract content lines under a matching section header.

        This is a heuristic approach: find lines matching known headers,
        then collect lines until the next section header or end of text.
        """
        lines = text.split("\n")
        result: List[str] = []
        capturing = False

        # Pre-compute all known section header keywords
        all_headers = set(self.EXPERIENCE_HEADERS + self.EDUCATION_HEADERS + [
            "skills", "technical skills", "projects", "summary",
            "objective", "certifications", "awards", "publications",
            "languages", "interests", "references", "hobbies",
            "achievements", "volunteer", "activities",
        ])

        for line in lines:
            stripped = line.strip()
            lower = stripped.lower().rstrip(":")

            if lower in [h.lower() for h in headers]:
                capturing = True
                continue

            if capturing:
                # Stop capturing if we hit another section header
                if lower in all_headers:
                    break
                if stripped:
                    result.append(stripped)

        return result
