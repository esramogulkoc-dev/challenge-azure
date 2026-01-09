# Challenge Azure – Belgium Train Data Project

## Project Overview

This project demonstrates a real-world data pipeline using **Microsoft Azure** and the **iRail API** to fetch live train data in Belgium. The pipeline normalizes the data and stores it in an **Azure SQL Database**, which is then visualized in a **Power BI dashboard**.

The project is part of a learning challenge, and the focus is on building a **cloud-native, serverless data pipeline** with Python Azure Functions.

---

## Repository Structure (`challenge-azure`)

```
challenge-azure/
│
├─ fetch_connection1/ # HTTP-triggered function to fetch train connections
│ ├─ init.py
│ └─ function.json
│
├─ fetch_connections_timer_v2/ # Timer-triggered function for automatic connection fetch
│ ├─ init.py
│ └─ function.json
│
├─ fetch_liveboard/ # HTTP-triggered function to fetch liveboard departures
│ ├─ init.py
│ └─ function.json
│
├─ fetch_liveboard_timer/ # Timer-triggered function for automatic liveboard fetch
│ ├─ init.py
│ └─ function.json
│
├─ host.json # Azure Functions host configuration
└─ local.settings.json # Local environment variables (ignored by git)

│
├─ images/ HTTP function test run.png
           SQL data table.png
           Power BI dashboard.png
           
## Must-Have Features

* **Azure Function App** (Python) deployed via **VS Code** to Azure
* **Azure SQL Database** to store normalized train data
* Functions can be triggered **manually via HTTP** or **automatically via Timer Trigger**
* Secrets (SQL credentials) are stored in **Azure App Settings**; `local.settings.json` is ignored in GitHub

---

## Nice-to-Have Features

* **Automated fetching** using Timer Trigger every hour
* **Power BI dashboard** connected to Azure SQL Database:
## Power BI Dashboard

The Power BI dashboard is included in this repository as a `.pbix` file and can be opened locally in Power BI Desktop; it cannot be viewed directly on GitHub.

You can download the Power BI dashboard here:  
challenge-azure-powerBI.pbix

Recommended visuals:

- Line chart: train departures over time
- Column chart: trains per station
- Table: detailed train info
- Slicers: dropdown filters for stations and date


  * Line chart showing train departures over time
  * Column chart showing train distribution per station
  * Table with detailed train information (`from_station`, `to_station`, `vehicle`, departure & arrival times)
  * Slicers to filter by station and date
* SQL timestamps converted from Unix format to DateTime for visualization

---

## Setup Instructions

1. Clone this repository:

```bash
git clone https://github.com/esramogulkoc-dev/challenge-azure.git
cd challenge-azure
```

> **Note:** `local.settings.json` is ignored in GitHub for security.

3. Deploy to Azure using VS Code:

```bash
func azure functionapp publish train-info-db
```

4. Test manually via the HTTP endpoints or wait for the Timer Trigger to fetch automatically.


## Screenshots / Deliverables
challenge-azure/
│
├─ images/

* Screenshot of **HTTP function test run** from Azure Portal
  HTTP function test run.png

* Screenshot of **SQL data table**
  SQL data table.png

* Screenshot of **Power BI dashboard**
  Power BI dashboard.png

## License

This project is for **learning purposes** as part of the Azure Challenge at BeCode.




