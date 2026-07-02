"""Export service — generates CSV downloads of ranking results."""

import csv
import io
import os
import uuid
from pathlib import Path
from typing import Dict, List

from app.core.config import settings


class ExportService:
    """Service for exporting ranking data to CSV files."""

    @staticmethod
    def generate_csv(
        job_title: str,
        rankings: List[Dict],
    ) -> str:
        """Generate a CSV file from ranking data and return the file path.

        Args:
            job_title: Title of the job for the filename.
            rankings: List of ranking dicts from RankingService.get_rankings.

        Returns:
            Absolute path to the generated CSV file.
        """
        export_dir = Path(settings.EXPORT_DIR)
        export_dir.mkdir(parents=True, exist_ok=True)

        # Create a safe filename
        safe_title = "".join(
            c if c.isalnum() or c in (" ", "-", "_") else "_"
            for c in job_title
        ).strip().replace(" ", "_")
        filename = f"rankings_{safe_title}_{uuid.uuid4().hex[:8]}.csv"
        file_path = export_dir / filename

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Header row
            writer.writerow([
                "Rank",
                "Candidate Name",
                "Candidate Email",
                "Overall Score",
                "Semantic Score",
                "Skill Score",
                "Matched Skills",
                "Missing Skills",
                "Explanation",
            ])

            # Data rows
            for r in rankings:
                matched = ", ".join(r.get("matched_skills", []))
                missing = ", ".join(r.get("missing_skills", []))

                writer.writerow([
                    r.get("rank", ""),
                    r.get("candidate_name", ""),
                    r.get("candidate_email", ""),
                    f"{r.get('overall_score', 0):.4f}",
                    f"{r.get('semantic_score', 0):.4f}",
                    f"{r.get('skill_score', 0):.4f}",
                    matched,
                    missing,
                    r.get("explanation", ""),
                ])

        return str(file_path.resolve())

    @staticmethod
    def generate_csv_bytes(
        job_title: str,
        rankings: List[Dict],
    ) -> bytes:
        """Generate CSV content as bytes (for streaming response).

        Args:
            job_title: Title of the job.
            rankings: List of ranking dicts.

        Returns:
            CSV content as UTF-8 bytes.
        """
        output = io.StringIO()
        writer = csv.writer(output)

        # Header row
        writer.writerow([
            "Rank",
            "Candidate Name",
            "Candidate Email",
            "Overall Score",
            "Semantic Score",
            "Skill Score",
            "Matched Skills",
            "Missing Skills",
            "Explanation",
        ])

        for r in rankings:
            matched = ", ".join(r.get("matched_skills", []))
            missing = ", ".join(r.get("missing_skills", []))

            writer.writerow([
                r.get("rank", ""),
                r.get("candidate_name", ""),
                r.get("candidate_email", ""),
                f"{r.get('overall_score', 0):.4f}",
                f"{r.get('semantic_score', 0):.4f}",
                f"{r.get('skill_score', 0):.4f}",
                matched,
                missing,
                r.get("explanation", ""),
            ])

        return output.getvalue().encode("utf-8")
