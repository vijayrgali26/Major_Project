# Requirements Document

## Introduction

The AI Resume Generation feature enhances the Skill2Job Placement System by enabling students to generate personalized, job-targeted resumes. When a student specifies their dream job and expected salary (LPA), the system uses NLP-based skill scoring and template-based content generation to produce resumes that highlight relevant skills, projects, and experience aligned with their career goals. The feature maintains backward compatibility with existing resume generation for students who have not set a dream job.

## Glossary

- **System**: The Skill2Job Placement System backend application
- **AI_Resume_Service**: The service component responsible for NLP-based skill scoring and content generation
- **Resume_Generator**: The service component responsible for PDF resume creation
- **Profile_Service**: The service component responsible for student profile management
- **Student_Profile**: The database entity containing student academic and career information
- **Dream_Job**: A text field (max 150 characters) representing the student's target job role
- **Expected_LPA**: A numeric field (0.0 to 100.0) representing the student's expected salary in lakhs per annum
- **Skill_Relevance_Score**: A float value (0.0 to 1.0) indicating how relevant a skill is to a dream job
- **Career_Objective**: An AI-generated text section (50-500 characters) describing career goals
- **Professional_Summary**: An AI-generated text section highlighting relevant experience
- **Prioritized_Skills**: A list of skills reordered by relevance to the dream job
- **Project_Description**: An enhanced project description with relevance notes
- **Experience_Level**: A classification (entry/mid/senior) derived from expected LPA

## Requirements

### Requirement 1: Profile Field Storage

**User Story:** As a student, I want to specify my dream job and expected salary, so that the system can generate a personalized resume aligned with my career goals.

#### Acceptance Criteria

1. THE Student_Profile SHALL store a dream_job field as a string with maximum length 150 characters
2. THE Student_Profile SHALL store an expected_lpa field as a float
3. WHEN expected_lpa is provided, THE System SHALL validate it is between 0.0 and 100.0
4. WHEN dream_job exceeds 150 characters, THE System SHALL truncate it to 150 characters
5. THE System SHALL allow dream_job to be null or empty string
6. THE System SHALL allow expected_lpa to be null

### Requirement 2: Profile Update API

**User Story:** As a student, I want to update my profile with dream job and expected salary information, so that I can receive personalized resume content.

#### Acceptance Criteria

1. WHEN a student submits a profile update with dream_job field, THE Profile_Service SHALL accept and store the value
2. WHEN a student submits a profile update with expected_lpa field, THE Profile_Service SHALL accept and store the value
3. WHEN expected_lpa is not a valid number, THE Profile_Service SHALL return a validation error
4. WHEN expected_lpa is outside the range 0.0 to 100.0, THE Profile_Service SHALL return a validation error with message "expected_lpa must be between 0.0 and 100.0"
5. THE Profile_Service SHALL update dream_job and expected_lpa only when the respective keys are present in the request
6. THE Profile_Service SHALL preserve existing dream_job and expected_lpa values when those keys are absent from the request

### Requirement 3: Skill Relevance Scoring

**User Story:** As a student, I want my skills to be scored based on relevance to my dream job, so that the most important skills appear prominently on my resume.

#### Acceptance Criteria

1. WHEN a skill and dream_job are provided, THE AI_Resume_Service SHALL compute a Skill_Relevance_Score between 0.0 and 1.0
2. WHEN a skill appears in the job role's expected skills list, THE System SHALL contribute 0.6 to the relevance score
3. WHEN a skill's tokens overlap with job role keywords, THE System SHALL contribute up to 0.25 to the relevance score based on overlap ratio
4. WHEN SpaCy is available, THE System SHALL contribute up to 0.15 to the relevance score based on word vector similarity
5. WHEN skill or dream_job is empty or null, THE AI_Resume_Service SHALL return a score of 0.0
6. THE AI_Resume_Service SHALL clamp the final score to the range [0.0, 1.0]

### Requirement 4: Skill Prioritization

**User Story:** As a student, I want my skills to be reordered by relevance to my dream job, so that recruiters see my most relevant qualifications first.

#### Acceptance Criteria

1. WHEN a list of skills and dream_job are provided, THE AI_Resume_Service SHALL return a reordered list with the same elements
2. THE AI_Resume_Service SHALL sort skills in descending order by Skill_Relevance_Score
3. WHEN multiple skills have equal relevance scores, THE System SHALL preserve their original relative order
4. WHEN skills list is empty, THE AI_Resume_Service SHALL return an empty list
5. WHEN dream_job is empty or null, THE AI_Resume_Service SHALL return the original skills list unchanged

### Requirement 5: Career Objective Generation

**User Story:** As a student, I want an AI-generated career objective statement, so that my resume clearly communicates my career goals aligned with my dream job.

#### Acceptance Criteria

1. WHEN dream_job, degree, branch, and skills are provided, THE AI_Resume_Service SHALL generate a Career_Objective
2. THE Career_Objective SHALL be between 50 and 500 characters in length
3. WHEN the generated text is shorter than 50 characters, THE System SHALL append additional content to reach the minimum length
4. WHEN the generated text exceeds 500 characters, THE System SHALL truncate it to 497 characters and append "..."
5. THE Career_Objective SHALL include the top 3 most relevant skills based on Skill_Relevance_Score
6. THE Career_Objective SHALL use a template appropriate for the Experience_Level derived from expected_lpa
7. WHEN skills list is empty, THE System SHALL use "relevant technologies" as the skills reference

### Requirement 6: Professional Summary Generation

**User Story:** As a student, I want an AI-generated professional summary, so that my resume highlights my relevant experience and qualifications.

#### Acceptance Criteria

1. WHEN dream_job, skills, projects, cgpa, and graduation_year are provided, THE AI_Resume_Service SHALL generate a Professional_Summary
2. THE Professional_Summary SHALL include up to 5 prioritized skills
3. WHEN project count is greater than 0, THE Professional_Summary SHALL reference the number of projects
4. WHEN cgpa is 7.0 or higher, THE Professional_Summary SHALL include the CGPA value
5. WHEN graduation_year is provided, THE Professional_Summary SHALL include the graduation year
6. THE Professional_Summary SHALL be a non-empty string

### Requirement 7: Project Description Enhancement

**User Story:** As a student, I want my project descriptions to be enhanced with relevance notes, so that recruiters understand how my projects relate to my dream job.

#### Acceptance Criteria

1. WHEN a list of projects and dream_job are provided, THE AI_Resume_Service SHALL return an enhanced list with the same number of elements
2. WHEN a project's text overlaps with job role keywords or skills, THE System SHALL generate a relevance_note
3. THE relevance_note SHALL include up to 3 relevant terms from the overlap
4. WHEN a project has no description, THE System SHALL generate a default description based on the project title
5. THE enhanced project SHALL include title, description, technologies, and relevance_note fields
6. WHEN projects list is empty, THE AI_Resume_Service SHALL return an empty list

### Requirement 8: Experience Level Classification

**User Story:** As a student, I want the system to classify my experience level based on expected salary, so that resume content is appropriate for my career stage.

#### Acceptance Criteria

1. WHEN expected_lpa is null or less than 5.0, THE System SHALL classify Experience_Level as "entry"
2. WHEN expected_lpa is between 5.0 and 10.0 (inclusive), THE System SHALL classify Experience_Level as "mid"
3. WHEN expected_lpa is greater than 10.0, THE System SHALL classify Experience_Level as "senior"

### Requirement 9: AI Resume Content Orchestration

**User Story:** As a student, I want all AI-generated content to be coordinated in a single operation, so that my resume is consistently personalized.

#### Acceptance Criteria

1. WHEN a profile with dream_job is provided, THE AI_Resume_Service SHALL generate a complete AIResumeContent object
2. THE AIResumeContent SHALL include career_objective, professional_summary, prioritized_skills, skill_categories, project_descriptions, and experience_level
3. THE AI_Resume_Service SHALL parse skills from the profile's skills_json field
4. WHEN skills_json is invalid or empty, THE System SHALL use an empty skills list
5. THE AI_Resume_Service SHALL categorize prioritized skills into groups (Programming Languages, Web & Frameworks, Data & ML, Databases, DevOps & Cloud, Other)

### Requirement 10: Resume Generation with AI Content

**User Story:** As a student, I want my generated resume to use AI-personalized content when I have set a dream job, so that my resume is tailored to my career goals.

#### Acceptance Criteria

1. WHEN a student has a non-empty dream_job, THE Resume_Generator SHALL use AI_Resume_Service to generate content
2. WHEN AI_Resume_Service fails, THE Resume_Generator SHALL fall back to template-based generation
3. THE Resume_Generator SHALL log AI generation failures and continue with fallback
4. THE AI-generated resume SHALL include Career Objective and Professional Summary sections
5. THE AI-generated resume SHALL display skills in prioritized order with categories
6. THE AI-generated resume SHALL include project relevance notes when available

### Requirement 11: Backward Compatibility

**User Story:** As a student who has not set a dream job, I want to generate a resume using the existing template-based approach, so that I can still create professional resumes.

#### Acceptance Criteria

1. WHEN dream_job is null or empty string, THE Resume_Generator SHALL use template-based generation
2. THE template-based resume SHALL include a Career Summary section
3. THE template-based resume SHALL display skills grouped by category without prioritization
4. THE template-based resume SHALL include project descriptions without relevance notes
5. THE Resume_Generator SHALL validate required fields (name, institution, degree, branch, skills) regardless of generation method

### Requirement 12: Resume Validation

**User Story:** As a student, I want to be notified of missing required information before resume generation, so that I can complete my profile.

#### Acceptance Criteria

1. WHEN required fields are missing, THE Resume_Generator SHALL raise a ValueError with a list of missing field names
2. THE required fields SHALL include name, institution, degree, branch, and skills
3. WHEN skills_json is not a non-empty JSON array, THE System SHALL consider skills as missing
4. THE Resume_Generator SHALL validate the profile before attempting AI or template-based generation

### Requirement 13: Skill Categorization

**User Story:** As a student, I want my skills to be automatically categorized, so that my resume is well-organized and easy to read.

#### Acceptance Criteria

1. WHEN skills are provided, THE AI_Resume_Service SHALL group them into predefined categories
2. THE System SHALL recognize Programming Languages category for skills like python, java, javascript, c, c++
3. THE System SHALL recognize Web & Frameworks category for skills like react, angular, flask, django, node.js
4. THE System SHALL recognize Data & ML category for skills like machine learning, tensorflow, pandas, numpy
5. THE System SHALL recognize Databases category for skills like sql, mysql, postgresql, mongodb
6. THE System SHALL recognize DevOps & Cloud category for skills like docker, kubernetes, aws, azure, git
7. WHEN a skill does not match any category, THE System SHALL place it in the "Other" category

### Requirement 14: Frontend Form Fields

**User Story:** As a student, I want to see form fields for dream job and expected salary in the profile editor, so that I can easily provide this information.

#### Acceptance Criteria

1. THE profile form SHALL include a text input field for dream_job
2. THE profile form SHALL include a numeric input field for expected_lpa
3. THE dream_job field SHALL have a maximum length of 150 characters
4. THE expected_lpa field SHALL accept decimal values
5. THE form SHALL display validation errors for expected_lpa outside the range 0.0 to 100.0
6. THE form SHALL allow dream_job and expected_lpa to be optional (empty)

### Requirement 15: API Response Format

**User Story:** As a frontend developer, I want the profile API to return dream_job and expected_lpa fields, so that I can display and edit them in the UI.

#### Acceptance Criteria

1. WHEN a profile is retrieved, THE Profile_Service SHALL include dream_job in the response
2. WHEN a profile is retrieved, THE Profile_Service SHALL include expected_lpa in the response
3. THE dream_job field SHALL be null when not set
4. THE expected_lpa field SHALL be null when not set
5. THE profile response SHALL maintain the existing structure with additional fields
