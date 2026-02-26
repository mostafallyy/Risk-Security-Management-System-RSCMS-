Risk & Security Control Management System (RSCMS)
A Backend REST API & Relational Database for Enterprise Risk Governance

Overview
RSCMS is a centralized backend platform designed to bridge the gap between low-level system states and high-level organizational risk management. It provides a robust RESTful API and a normalized PostgreSQL database to track security controls, incident trends, and compliance metrics (MTTR/MTTD) in real-time.

Core Features
RESTful Backend: Built with Flask, featuring endpoints for real-time incident lifecycle management and complex data filtering.

Advanced Risk Analytics: Dedicated logic to calculate Mean Time to Resolve (MTTR) and Mean Time to Detect (MTTD), critical for financial infrastructure stability.

Relational Architecture: A normalized SQL schema mapping Users to Risks and Controls, ensuring referential integrity and audit readiness.

Data Visualization: Automated telemetry pipeline designed to feed Power BI dashboards for stakeholder reporting.

High-Volume Testing: Includes a simulation engine capable of generating 5,000+ incidents to validate backend performance and scalability.

Technical Stack
Languages: Python, SQL (PostgreSQL)

Frameworks: Flask, Psycopg2

Architecture: RESTful API, Microservices-ready

Documentation: Draw.io (Workflow & Schema Design)

Analytics: Power BI

Project Structure
Plaintext

├── app.py                # Main Flask API with REST endpoints
├── db/                   # Database Layer
│   ├── schema.sql        # Normalized table structures and constraints
│   ├── SEED.sql          # Initial security control data
│   └── analytics.sql     # Complex queries for MTTR and trend analysis
├── generateFakeData.py   # Performance testing & simulation engine
├── RCMS.drawio           # Full architectural system diagram
└── requirements.txt      # Project dependencies
API Usage Examples
Get Incidents by Severity:
GET /analytics/incidents/by-severity

Create New Security Incident:
POST /incidents

JSON

{
  "title": "Unauthorized Access Attempt",
  "severity": "High",
  "occurred_at": "2026-02-26T14:30:00"
}
Engineering Focus: Audit & Compliance
The RSCMS was engineered with IT Compliance as a primary goal. By mapping technical controls directly to organizational risks, the system facilitates automated evidence collection, reducing the time required for internal audits and ensuring alignment with frameworks such as NIST and PHIPA.
