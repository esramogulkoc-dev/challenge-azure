## Cloud Architecture Overview

This project uses two separate Azure Function Apps to clearly separate
real-time data access from data storage and analysis.

### Function App 1 – Live Departure Board
- Built directly in Azure Portal
- HTTP-triggered
- Fetches live train data from the iRail API
- Returns data directly to the user/dashboard
- Does NOT write to the database

### Function App 2 – Data Ingestion
- Developed in VS Code and deployed to Azure
- Fetches train connections between Leuven and Gent-Sint-Pieters
- Stores historical data in Azure SQL Database
- Used for analysis and dashboard aggregation

### Database
- Azure SQL Database (`irail-db`)
- Shared by both local and cloud functions
- Central storage for all historical train data
