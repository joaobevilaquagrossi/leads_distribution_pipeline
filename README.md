# Leads Distribution Data Pipeline

## Project Overview

This project consolidates lead distribution data from multiple sources into a centralized MySQL table.

The original CRM API only provided recent records, while historical data existed in two separate sources:

- Microsoft Access database
- SharePoint CSV export
- CRM API endpoint

The goal was to migrate and unify all historical and recent lead distribution records into a MySQL table named `leads_distribuicao`, using `id_log` as the unique identifier.

## Business Context

The Marketing and Sales team needed a reliable historical database for lead distribution analysis.

Before this project, lead distribution data was fragmented across different files and systems, making it difficult to analyze historical performance, broker assignment, sales team distribution, and lead flow over time.

This project created a unified dataset that can be used for SQL analysis, Power BI dashboards, and recurring CRM API updates.

## Data Sources

| Source | Type | Purpose |
|---|---|---|
| CRM API | REST API | Recent and recurring lead distribution data |
| Access database | `.accdb` | Historical lead distribution data |
| SharePoint export | `.csv` | Additional historical lead distribution data |
| MySQL | Database | Centralized storage and analytics source |

## Final Database Table

The final table used in MySQL is:

```sql
cvdw.leads_distribuicao