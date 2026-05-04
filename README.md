# Thokala_SiriChandana_COMP_699_D```markdown
# Deadline Negotiation as a Service (DNaaS)

## Author
Siri Chandana Thokala

## Course
COMP-699-D Professional Seminar  
Spring 2026

## Overview
This project presents the Deadline Negotiation as a Service (DNaaS) system, which is designed to help teams manage project deadlines in a more structured and intelligent way. The system focuses on analyzing workload, detecting conflicts, and supporting deadline negotiation between stakeholders. :contentReference[oaicite:0]{index=0}  

The main goal of this system is to reduce unrealistic deadlines, improve planning, and support better decision making using data-driven analysis instead of assumptions.

## Problem Statement
In many organizations, deadlines are assigned without properly analyzing workload and team capacity. This leads to overlapping tasks, missed deadlines, and increased pressure on contributors. :contentReference[oaicite:1]{index=1}  

There is also no structured system to detect conflicts or suggest better alternatives. Most teams depend on manual communication, which is time-consuming and not always effective. This project addresses these issues by introducing an automated and analytical approach to deadline management.

## Key Features

### Project and Task Management
- Managers can create projects and define constraints such as deadlines and priorities  
- Contributors can create tasks with effort, deadlines, and priority levels  
- Tasks can be updated, reassigned, and managed dynamically  

### Workload and Capacity Planning
- Contributors can define availability and working hours  
- System calculates workload based on assigned tasks  
- Managers can analyze workload distribution across team members  

### Conflict Detection and Analysis
- Detects scheduling conflicts automatically  
- Identifies overload situations and overlapping tasks  
- Provides feasibility analysis for project timelines  

### Deadline Negotiation System
- Generates alternative deadline proposals based on workload and priority  
- Allows contributors to submit counter-proposals  
- Supports approval, rejection, and escalation of deadlines  

### Audit and Reporting
- Maintains audit logs for all actions and decisions  
- Provides reports on workload, risks, and negotiation history  
- Ensures transparency and accountability in decision making  

## System Architecture
The system follows a structured layered approach:

- User Management Layer (Manager, Contributor, Client, Administrator)  
- Project and Task Management Layer  
- Analysis Engine for workload and conflict detection  
- Negotiation Management for deadline proposals  
- Audit and Reporting Layer for tracking system activity  

The system is designed in a client-server model where users interact through a web interface and backend processes handle analysis and data operations. :contentReference[oaicite:2]{index=2}  

## Technologies Used
- Python (Object-Oriented Programming)  
- SQLite / Relational Database  
- Streamlit or Web Interface (for UI)  
- UML for system design (Use Case, Class, Sequence diagrams)  

## File Structure
- `dnaas_system.py` – Main application file  
- Modules for task, project, analysis, proposal, and logging  
- Unit tests included for validation  

## How to Run

1. Install required dependencies:
```

pip install streamlit

```

2. Run the application:
```

streamlit run dnaas_system.py

```

3. Open in browser:
```

[http://localhost:8501](http://localhost:8501)

```

## System Workflow
1. Manager creates a project and defines constraints  
2. Contributor creates tasks and sets availability  
3. System calculates workload and detects conflicts  
4. Manager generates deadline proposals  
5. Contributors submit counter-proposals if needed  
6. Deadlines are approved, rejected, or escalated  
7. All actions are recorded in audit logs  

## Key Benefits
- Reduces deadline conflicts and delays  
- Improves team coordination and planning  
- Automates conflict detection and resolution  
- Provides transparency through audit logs  
- Supports better decision making with data analysis  

## Limitations
- Simplified authentication for demonstration  
- Limited external integrations  
- Designed mainly for academic and small-scale environments  

## Conclusion
The DNaaS system provides a structured approach to managing deadlines by combining workload analysis, conflict detection, and negotiation workflows. It improves planning accuracy, reduces manual effort, and helps teams achieve realistic and achievable deadlines.

## References
Dennis, A., Wixom, B. H., & Tegarden, D. (2021). Systems analysis and design: An object-oriented approach with UML.  
Sommerville, I. (2016). Software engineering.  
Pressman, R. S., & Maxim, B. R. (2020). Software engineering: A practitioner’s approach.  
Fowler, M. (2004). UML distilled.  
```
