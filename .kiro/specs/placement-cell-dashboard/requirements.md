# Requirements Document

## Introduction

The Placement Cell Dashboard is a dedicated interface for placement officers (placement_officer role) to manage and coordinate placement activities within the Skill2Job application. This dashboard provides comprehensive oversight of placement statistics, active job openings, student applications, company engagement, and quick actions for common placement tasks. It integrates with the existing Flask backend and React frontend, following established design patterns and leveraging existing models (users, students, companies, job_roles, applications, placement_records, analytics).

## Glossary

- **Placement_Dashboard**: The React component that renders the placement officer's dashboard interface
- **Dashboard_Service**: The Flask service that aggregates placement coordination data
- **Placement_Officer**: A user with the placement_officer role who coordinates placement activities
- **Job_Opening**: An active JobRole record with is_active=true
- **Application_Status**: The status field in Shortlist records (pending, shortlisted, rejected, placed)
- **Placement_Metric**: Aggregated statistics about placement activities (counts, percentages, trends)
- **Quick_Action**: A dashboard button that triggers common placement tasks
- **Real_Time_Update**: Dashboard data refreshed automatically or on-demand
- **Company_Engagement**: Metrics tracking company participation (active jobs, shortlists, placements)
- **Student_Application**: A Shortlist record linking a student profile to a job role

## Requirements

### Requirement 1: Dashboard Overview Statistics

**User Story:** As a placement officer, I want to see key placement statistics at a glance, so that I can quickly understand the current placement status.

#### Acceptance Criteria

1. THE Placement_Dashboard SHALL display the total count of active Job_Openings
2. THE Placement_Dashboard SHALL display the total count of Student_Applications with status "pending"
3. THE Placement_Dashboard SHALL display the total count of Student_Applications with status "shortlisted"
4. THE Placement_Dashboard SHALL display the total count of placement records for the current academic year
5. THE Placement_Dashboard SHALL display the placement percentage (placed students / total eligible students * 100)
6. THE Placement_Dashboard SHALL display the count of companies with active Job_Openings
7. FOR ALL Placement_Metrics, the displayed values SHALL match the database state within 5 seconds of page load

### Requirement 2: Active Job Openings Management

**User Story:** As a placement officer, I want to view and manage active job openings, so that I can coordinate placement activities effectively.

#### Acceptance Criteria

1. THE Placement_Dashboard SHALL display a list of all Job_Openings where is_active is true
2. WHEN a Job_Opening is displayed, THE Placement_Dashboard SHALL show the job title, company name, required skills, CGPA threshold, and creation date
3. THE Placement_Dashboard SHALL display the count of Student_Applications for each Job_Opening
4. THE Placement_Dashboard SHALL provide a button to view detailed shortlist for each Job_Opening
5. THE Placement_Dashboard SHALL provide a button to deactivate a Job_Opening
6. WHEN the deactivate button is clicked, THE Dashboard_Service SHALL set is_active to false for that Job_Opening
7. THE Placement_Dashboard SHALL support pagination for Job_Openings with 10 items per page
8. THE Placement_Dashboard SHALL support search filtering by job title or company name

### Requirement 3: Student Application Tracking

**User Story:** As a placement officer, I want to track student applications across all job openings, so that I can monitor application progress and identify bottlenecks.

#### Acceptance Criteria

1. THE Placement_Dashboard SHALL display a summary of Student_Applications grouped by Application_Status
2. THE Placement_Dashboard SHALL display a list of recent Student_Applications sorted by shortlisted_at descending
3. WHEN a Student_Application is displayed, THE Placement_Dashboard SHALL show student name, job title, company name, compatibility score, and Application_Status
4. THE Placement_Dashboard SHALL provide a button to view student profile for each Student_Application
5. THE Placement_Dashboard SHALL provide a button to update Application_Status for each Student_Application
6. WHEN Application_Status is updated, THE Dashboard_Service SHALL validate the new status is one of (pending, shortlisted, rejected, placed)
7. THE Placement_Dashboard SHALL support filtering Student_Applications by Application_Status
8. THE Placement_Dashboard SHALL support filtering Student_Applications by Job_Opening

### Requirement 4: Company Engagement Monitoring

**User Story:** As a placement officer, I want to monitor company engagement metrics, so that I can identify active companies and follow up with inactive ones.

#### Acceptance Criteria

1. THE Placement_Dashboard SHALL display a list of companies with active Job_Openings
2. WHEN a company is displayed, THE Placement_Dashboard SHALL show company name, industry, location, and contact information
3. THE Placement_Dashboard SHALL display the count of active Job_Openings for each company
4. THE Placement_Dashboard SHALL display the count of Student_Applications for each company
5. THE Placement_Dashboard SHALL display the count of placement records for each company in the current academic year
6. THE Placement_Dashboard SHALL calculate and display Company_Engagement score as (active_jobs * 2 + applications + placements * 5)
7. THE Placement_Dashboard SHALL sort companies by Company_Engagement score descending by default

### Requirement 5: Quick Actions for Common Tasks

**User Story:** As a placement officer, I want quick access to common placement tasks, so that I can perform routine operations efficiently.

#### Acceptance Criteria

1. THE Placement_Dashboard SHALL provide a Quick_Action button to create a new Job_Opening
2. THE Placement_Dashboard SHALL provide a Quick_Action button to view all companies
3. THE Placement_Dashboard SHALL provide a Quick_Action button to view all students
4. THE Placement_Dashboard SHALL provide a Quick_Action button to generate placement analytics report
5. WHEN a Quick_Action button is clicked, THE Placement_Dashboard SHALL navigate to the appropriate page or open a modal dialog
6. THE Placement_Dashboard SHALL provide a Quick_Action button to export Student_Applications as CSV
7. WHEN the export CSV button is clicked, THE Dashboard_Service SHALL generate a CSV file with columns (student_name, student_email, job_title, company_name, status, compatibility_score, shortlisted_at)

### Requirement 6: Real-Time Dashboard Updates

**User Story:** As a placement officer, I want the dashboard to refresh automatically, so that I always see current placement data without manual page reloads.

#### Acceptance Criteria

1. THE Placement_Dashboard SHALL fetch dashboard data from Dashboard_Service on component mount
2. THE Placement_Dashboard SHALL provide a manual refresh button to reload all dashboard data
3. WHEN the refresh button is clicked, THE Placement_Dashboard SHALL display a loading indicator during data fetch
4. IF data fetch fails, THEN THE Placement_Dashboard SHALL display an error message with retry option
5. THE Placement_Dashboard SHALL cache dashboard data in component state to prevent unnecessary re-renders
6. WHEN any Quick_Action modifies data, THE Placement_Dashboard SHALL automatically refresh affected sections

### Requirement 7: Role-Based Access Control

**User Story:** As a system administrator, I want the placement dashboard to be accessible only to placement officers, so that sensitive placement data is protected.

#### Acceptance Criteria

1. THE Dashboard_Service SHALL require JWT authentication for all placement dashboard endpoints
2. THE Dashboard_Service SHALL verify the user role is "placement_officer" or "admin" before returning dashboard data
3. IF the user role is "student", THEN THE Dashboard_Service SHALL return HTTP 403 Forbidden
4. THE Placement_Dashboard SHALL use the ProtectedRoute component with required role "placement_officer"
5. IF an unauthenticated user attempts to access the dashboard, THEN THE Placement_Dashboard SHALL redirect to the login page
6. THE Placement_Dashboard SHALL display the authenticated Placement_Officer name in the dashboard header

### Requirement 8: Dashboard Service Backend Integration

**User Story:** As a backend developer, I want a dedicated service to aggregate placement dashboard data, so that the frontend receives optimized, pre-computed metrics.

#### Acceptance Criteria

1. THE Dashboard_Service SHALL implement a method get_placement_officer_summary that returns all Placement_Metrics
2. THE Dashboard_Service SHALL query the database to count active Job_Openings where is_active is true
3. THE Dashboard_Service SHALL query the database to count Student_Applications grouped by Application_Status
4. THE Dashboard_Service SHALL query the database to count placement records for the current academic year
5. THE Dashboard_Service SHALL calculate placement percentage as (placement_count / eligible_student_count * 100)
6. THE Dashboard_Service SHALL query the database to aggregate Company_Engagement metrics
7. THE Dashboard_Service SHALL return all metrics as a JSON object with keys (active_jobs, pending_applications, shortlisted_applications, placements, placement_percentage, active_companies, company_engagement)
8. THE Dashboard_Service SHALL execute all queries within 2 seconds for datasets up to 10,000 records

### Requirement 9: Dashboard UI Component Structure

**User Story:** As a frontend developer, I want a well-structured dashboard component, so that the code is maintainable and follows existing design patterns.

#### Acceptance Criteria

1. THE Placement_Dashboard SHALL be implemented as a React functional component with TypeScript
2. THE Placement_Dashboard SHALL use the existing SummaryCard component to display Placement_Metrics
3. THE Placement_Dashboard SHALL use the existing LoadingSkeleton component during data fetch
4. THE Placement_Dashboard SHALL follow the existing CSS design system with variables from global.css
5. THE Placement_Dashboard SHALL implement responsive layout that adapts to mobile, tablet, and desktop viewports
6. THE Placement_Dashboard SHALL use the existing api.ts service for all HTTP requests
7. THE Placement_Dashboard SHALL handle loading, error, and success states consistently with other admin pages
8. THE Placement_Dashboard SHALL be added to the admin navigation menu with label "Placement Cell"

### Requirement 10: Dashboard Route Configuration

**User Story:** As a developer, I want the placement dashboard routes properly configured, so that the feature integrates seamlessly with the existing application.

#### Acceptance Criteria

1. THE backend SHALL register a new route GET /api/dashboard/placement-officer in dashboard_routes.py
2. THE route SHALL be protected with @jwt_required and @role_required("placement_officer")
3. THE route SHALL call Dashboard_Service.get_placement_officer_summary and return JSON response
4. THE frontend SHALL add a new route /admin/placement-cell in App.tsx
5. THE route SHALL use ProtectedRoute with allowedRoles ["placement_officer", "admin"]
6. THE route SHALL render the Placement_Dashboard component
7. THE frontend SHALL add a navigation link to /admin/placement-cell in the admin sidebar
8. THE navigation link SHALL be visible only to users with role "placement_officer" or "admin"

