# Implementation Plan

## Overview

This implementation plan covers the AI Resume Generation feature that personalizes student resumes based on their dream job and expected salary. The feature uses NLP-based skill scoring and template-based content generation to produce tailored resumes. Most backend services are already implemented; this plan focuses on testing, validation, and frontend integration.

## Tasks

## 1. Implement Job Role Knowledge Base Service
[Requirements: Req 3, Req 8]

Create the JobRoleKnowledgeBase service that provides role-specific skills, keywords, and experience level classification for AI resume generation.

- Create `backend/app/services/job_role_knowledge_base.py`
- Implement `get_role_skills(dream_job)` returning list of expected skills for the role
- Implement `get_role_keywords(dream_job)` returning list of keywords associated with the role
- Implement `get_experience_level(expected_lpa)` returning "entry"/"mid"/"senior" based on LPA
- Add role data for common job titles: Full Stack Developer, Data Scientist, Backend Developer, Frontend Developer, DevOps Engineer, ML Engineer
- Handle case-insensitive role matching and return empty lists for unknown roles
- Experience level: <5.0 LPA = "entry", 5.0-10.0 = "mid", >10.0 = "senior"

## 2. Write Unit Tests for AIResumeService
[Requirements: Req 3, Req 4, Req 5, Req 6, Req 7, Req 9]

Write comprehensive unit tests for all AIResumeService methods to verify NLP-based skill scoring and content generation.

- Create `backend/tests/unit/test_ai_resume_service.py`
- Test `score_skill_relevance()` returns values in [0.0, 1.0] range
- Test `prioritize_skills()` maintains all elements and sorts by relevance
- Test `generate_career_objective()` produces text between 50-500 characters
- Test `generate_professional_summary()` includes relevant skills and project count
- Test `generate_project_descriptions()` adds relevance notes for matching projects
- Test `generate_ai_content()` orchestrates all content generation
- Test `_categorize_skills()` groups skills into correct categories
- Test edge cases: empty inputs, null values, missing SpaCy

## 3. Write Property-Based Tests for Skill Scoring
[Requirements: Req 3, Req 4]

Write property-based tests using Hypothesis to verify skill scoring and prioritization invariants hold across random inputs.

- Create `backend/tests/property/test_ai_resume_properties.py`
- Property: `score_skill_relevance()` always returns float in [0.0, 1.0]
- Property: `prioritize_skills()` preserves all input elements (no additions/deletions)
- Property: `prioritize_skills()` maintains stable sort (equal scores keep original order)
- Property: `_categorize_skills()` preserves all skills across categories
- Generate random skill lists (0-50 skills) and job titles
- Run 100+ examples per property test

## 4. Write Integration Tests for Resume Generation
[Requirements: Req 10, Req 11]

Write integration tests for the complete resume generation flow with AI content and backward compatibility.

- Create `backend/tests/integration/test_ai_resume_generation.py`
- Test resume generation with dream_job set (AI path)
- Test resume generation without dream_job (template path)
- Test AI generation failure fallback to template
- Verify PDF contains AI sections: Career Objective, Professional Summary
- Verify skills are prioritized in AI-generated resume
- Verify project relevance notes appear in AI-generated resume
- Mock AIResumeService for controlled testing

## 5. Write Profile Service Validation Tests
[Requirements: Req 2]

Write tests for profile service validation of dream_job and expected_lpa fields.

- Add tests to `backend/tests/unit/test_profile_service.py`
- Test dream_job truncation at 150 characters
- Test expected_lpa range validation (0.0-100.0)
- Test expected_lpa type validation (must be numeric)
- Test null/empty values are accepted for both fields
- Test field preservation when keys are absent from request
- Test error messages match requirement specifications

## 6. Add Database Migration for Profile Fields
[Requirements: Req 1]

Create and run database migration to add dream_job and expected_lpa columns to student_profile table.

- Create Alembic migration script in `backend/migrations/versions/`
- Add `dream_job` VARCHAR(150) nullable column
- Add `expected_lpa` FLOAT nullable column
- Run migration on development database: `flask db upgrade`
- Verify columns exist with correct types using database inspection
- Ensure existing data is preserved

## 7. Enhance Frontend Profile Form Validation
[Requirements: Req 14]

Add client-side validation and UX improvements for dream_job and expected_lpa fields in the Profile form.

- Update `frontend/src/pages/student/Profile.tsx`
- Add character counter for dream_job showing "X/150 characters"
- Add range validation for expected_lpa (0.0-100.0) with inline error
- Display validation errors below each field
- Add helper text: "Set your dream job to get an AI-tailored resume"
- Test form submission with invalid values (out of range, too long)

## 8. Update Resume Page with AI Indicator
[Requirements: Req 10]

Update the Resume page to show when AI-enhanced resume generation is available based on dream_job setting.

- Update `frontend/src/pages/student/Resume.tsx`
- Fetch dream_job from profile on component mount
- Display success alert when dream_job is set: "AI-Enhanced Resume — Your resume will be tailored for: {dream_job}"
- Display info message when dream_job is not set: "💡 Set your dream job in your profile to get an AI-tailored resume"
- Add link to profile page in the info message
- Update success message after generation to mention AI enhancement

## 9. Write End-to-End Resume Generation Test
[Requirements: Req 10, Req 12]

Write end-to-end test for complete AI resume generation workflow from profile to PDF.

- Create `backend/tests/integration/test_resume_e2e.py`
- Create test profile with dream_job="Full Stack Developer" and expected_lpa=8.5
- Add skills, projects, and certifications to profile
- Call `/resume/generate` API endpoint
- Download generated PDF via `/resume/download`
- Verify PDF contains AI sections (Career Objective, Professional Summary)
- Verify skills are prioritized (relevant skills appear first)
- Test with missing required fields (should return validation error)

## 10. Update Project Documentation
[Requirements: All]

Update project documentation to describe the AI Resume Generation feature and its usage.

- Update `README.md` with AI Resume Generation section
- Document dream_job and expected_lpa profile fields
- Add API endpoint documentation for profile update
- Include example request/response for profile with AI fields
- Document SpaCy dependency as optional (feature degrades gracefully)
- Add troubleshooting section for common issues
- Include screenshots of Profile and Resume pages with AI features

## Task Dependency Graph

```json
{
  "waves": [
    ["1", "5", "6"],
    ["2", "3", "4", "7", "8"],
    ["9"],
    ["10"]
  ]
}
```

## Notes

- Tasks 1-5 focus on backend implementation and testing
- Task 6 is a prerequisite for frontend tasks (7-8) as it adds required database columns
- Tasks 7-8 enhance the frontend user experience
- Task 9 validates the complete end-to-end workflow
- Task 10 documents the feature for users and developers
- The AIResumeService is already implemented; tasks focus on supporting infrastructure and testing
