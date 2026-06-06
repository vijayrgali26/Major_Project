"""Job Role Knowledge Base for the Skill2Job Placement System.

Provides role-specific skills, keywords, and experience level classification
to support AI-powered resume generation and job matching.

Requirements: 3.2, 8.1-8.3
"""


class JobRoleKnowledgeBase:
    """Knowledge base mapping job roles to expected skills and keywords."""

    def __init__(self):
        """Initialize the knowledge base with role data."""
        self.ROLE_ALIAS_MAP = {
            "machine learning engineer": "ml engineer",
            "machine learning developer": "ml engineer",
            "backend engineer": "backend developer",
            "frontend engineer": "frontend developer",
            "software developer": "software engineer",
            "web developer": "full stack developer",
        }

        self.JOB_ROLE_DATABASE = {
            "full stack developer": {
                "skills": [
                    "JavaScript", "React", "Node.js", "Python", "Flask",
                    "Django", "SQL", "MongoDB", "HTML", "CSS", "Git",
                    "REST API", "TypeScript", "Express"
                ],
                "keywords": [
                    "web development", "frontend", "backend", "database",
                    "api", "responsive", "deployment", "testing"
                ]
            },
            "data scientist": {
                "skills": [
                    "Python", "Machine Learning", "Pandas", "NumPy",
                    "Scikit-learn", "TensorFlow", "Statistics", "SQL",
                    "Data Visualization", "Jupyter", "Matplotlib", "Seaborn"
                ],
                "keywords": [
                    "data", "data analysis", "predictive modeling", "statistical analysis",
                    "deep learning", "nlp", "computer vision", "big data"
                ]
            },
            "backend developer": {
                "skills": [
                    "Python", "Java", "Node.js", "SQL", "PostgreSQL",
                    "MongoDB", "REST API", "Microservices", "Docker",
                    "Redis", "Flask", "Django", "Spring Boot"
                ],
                "keywords": [
                    "server-side", "database design", "api development",
                    "scalability", "performance", "security", "authentication"
                ]
            },
            "frontend developer": {
                "skills": [
                    "javascript", "react", "angular", "vue.js", "html",
                    "css", "typescript", "webpack", "sass", "responsive design",
                    "redux", "git"
                ],
                "keywords": [
                    "user interface", "user experience", "responsive",
                    "accessibility", "cross-browser", "performance optimization"
                ]
            },
            "devops engineer": {
                "skills": [
                    "docker", "kubernetes", "aws", "azure", "terraform",
                    "jenkins", "git", "linux", "python", "bash",
                    "ci/cd", "ansible"
                ],
                "keywords": [
                    "automation", "infrastructure", "deployment", "monitoring",
                    "cloud computing", "containerization", "orchestration"
                ]
            },
            "ml engineer": {
                "skills": [
                    "python", "tensorflow", "pytorch", "machine learning",
                    "deep learning", "scikit-learn", "pandas", "numpy",
                    "docker", "kubernetes", "mlops", "git"
                ],
                "keywords": [
                    "model deployment", "training pipelines", "feature engineering",
                    "model optimization", "production ml", "scalability"
                ]
            },
            "software engineer": {
                "skills": [
                    "python", "java", "javascript", "c++", "git",
                    "data structures", "algorithms", "sql", "testing",
                    "debugging", "version control"
                ],
                "keywords": [
                    "software development", "problem solving", "code quality",
                    "design patterns", "agile", "collaboration"
                ]
            },
            "mobile developer": {
                "skills": [
                    "react native", "flutter", "swift", "kotlin", "java",
                    "android", "ios", "rest api", "git", "firebase"
                ],
                "keywords": [
                    "mobile applications", "cross-platform", "app store",
                    "user experience", "performance", "offline support"
                ]
            },
            "qa engineer": {
                "skills": [
                    "selenium", "pytest", "junit", "test automation",
                    "manual testing", "api testing", "sql", "git",
                    "jira", "postman"
                ],
                "keywords": [
                    "quality assurance", "test cases", "bug tracking",
                    "regression testing", "performance testing", "ci/cd"
                ]
            },
            "cloud engineer": {
                "skills": [
                    "aws", "azure", "gcp", "terraform", "docker",
                    "kubernetes", "python", "linux", "networking",
                    "security", "ci/cd"
                ],
                "keywords": [
                    "cloud infrastructure", "scalability", "high availability",
                    "cost optimization", "migration", "serverless"
                ]
            }
        }

    def get_role_skills(self, dream_job: str) -> list[str]:
        """Get expected skills for a job role.

        Args:
            dream_job: The target job role (case-insensitive).

        Returns:
            List of expected skill names for the role.
            Returns empty list if role is not found.
        """
        if not dream_job:
            return []

        matched_role = self.match_role(dream_job)
        if not matched_role:
            return []

        return self.JOB_ROLE_DATABASE.get(matched_role, {}).get("skills", [])

    def get_role_keywords(self, dream_job: str) -> list[str]:
        """Get keywords associated with a job role.

        Args:
            dream_job: The target job role (case-insensitive).

        Returns:
            List of keywords associated with the role.
            Returns empty list if role is not found.
        """
        if not dream_job:
            return []

        matched_role = self.match_role(dream_job)
        if not matched_role:
            return []

        return self.JOB_ROLE_DATABASE.get(matched_role, {}).get("keywords", [])

    def get_experience_level(self, expected_lpa: float | None) -> str:
        """Classify experience level based on expected salary.

        Args:
            expected_lpa: Expected salary in lakhs per annum (or None).

        Returns:
            One of "entry", "mid", or "senior".

        Classification:
            - entry: expected_lpa is None or <= 6.0
            - mid: 6.0 < expected_lpa <= 15.0
            - senior: expected_lpa > 15.0
        """
        if expected_lpa is None or expected_lpa <= 6.0:
            return "entry"
        elif expected_lpa <= 15.0:
            return "mid"
        else:
            return "senior"

    def match_role(self, dream_job: str) -> str | None:
        """Match a user-provided job title to a known role in the database.

        Performs fuzzy matching using:
        1. Exact match (case-insensitive)
        2. Substring match (role contained in input)
        3. Token overlap match (shared words)

        Args:
            dream_job: The user-provided job title.

        Returns:
            The matched role key from the database, or None if no match found.
        """
        if not dream_job or not dream_job.strip():
            return None

        normalized_input = dream_job.lower().strip()

        # 1. Exact match
        if normalized_input in self.JOB_ROLE_DATABASE:
            return normalized_input

        # 1b. Alias match - known synonyms and variants
        if normalized_input in self.ROLE_ALIAS_MAP:
            return self.ROLE_ALIAS_MAP[normalized_input]

        # 2. Substring match - check if any known role is contained in the input
        for role_key in self.JOB_ROLE_DATABASE:
            if role_key in normalized_input:
                return role_key

        # 3. Token overlap match - find role with most overlapping words
        input_tokens = set(normalized_input.split())
        best_match = None
        best_overlap = 0

        for role_key in self.JOB_ROLE_DATABASE:
            role_tokens = set(role_key.split())
            overlap = len(input_tokens & role_tokens)
            if overlap > best_overlap and overlap > 0:
                best_overlap = overlap
                best_match = role_key

        return best_match
