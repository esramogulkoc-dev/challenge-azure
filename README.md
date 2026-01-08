# Challenge Azure – Belgium Train Data Project

## Project Overview

This project demonstrates a real-world data pipeline using **Microsoft Azure** and the **iRail API** to fetch live train data in Belgium. The pipeline normalizes the data and stores it in an **Azure SQL Database**, which is then visualized in a **Power BI dashboard**.

The project is part of a learning challenge, and the focus is on building a **cloud-native, serverless data pipeline** with Python Azure Functions.

---

## Repository Structure (`challenge-azure`)

```
challenge-azure/
│
├─ fetch_connection1/              # HTTP-triggered function to fetch train connections
│   ├─ __init__.py
│   └─ function.json
│
├─ fetch_liveboard/                # HTTP-triggered function to fetch liveboard departures
│   ├─ __init__.py
│   └─ function.json
│
├─ fetch_connection1_timer/        # Timer-triggered function for automatic connection fetch
│   ├─ __init__.py
│   └─ function.json
│
├─ fetch_liveboard_timer/          # Timer-triggered function for automatic liveboard fetch
│   ├─ __init__.py
│   └─ function.json
│
├─ host.json                       # Azure Functions host configuration
└─ local.settings.json             # Local environment variables (ignored by git)
```

---

## Must-Have Features

* **Azure Function App** (Python) deployed via **VS Code** to Azure
* **Azure SQL Database** to store normalized train data
* Functions can be triggered **manually via HTTP** or **automatically via Timer Trigger**
* Secrets (SQL credentials) are stored in **Azure App Settings**; `local.settings.json` is ignored in GitHub

---

## Nice-to-Have Features

* **Automated fetching** using Timer Trigger every hour
* **Power BI dashboard** connected to Azure SQL Database:

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

---

## Power BI Dashboard

* Connect **Power BI Desktop / Service** to your **Azure SQL Database**.
* Recommended visuals:

### 1️⃣ Line Chart – Train Count Over Time

* **X axis:** `departure_datetime`
* **Y axis:** Count of `departure_time`
* **Tooltip:** `from_station`, `to_station`
* **Purpose:** See the number of trains departing per hour/day

### 2️⃣ Column Chart – Trains per Station

* **X axis:** `from_station` or `to_station`
* **Y axis:** Count of rows
* **Purpose:** Identify the busiest train routes

### 3️⃣ Table – Detailed Train Information

* **Fields:** `from_station`, `to_station`, `vehicle`, `departure_datetime`, `arrival_datetime`
* **Purpose:** Show detailed list of train departures

### 4️⃣ Slicers

* Filter by `from_station`, `to_station`, and date
* **Purpose:** Allow dynamic dashboard filtering

### Layout Example

```
-------------------------------------------------
| Line chart (train count over time)          |
-------------------------------------------------
| Slicer (Left) | Column chart (Right)       |
-------------------------------------------------
| Table (Bottom, full width)                 |
-------------------------------------------------
```

> **Note:** Convert Unix timestamps to DateTime using Power Query or DAX in Power BI.
> Example DAX:

```DAX
DepartureDateTime = DATETIME(1970,1,1,0,0,0) + ([departure_time]/86400)
```

---

## Screenshots / Deliverables

* Screenshot of **HTTP function test run** from Azure Portal
* Screenshot of **SQL data table**
* Screenshot of **Power BI dashboard**

---

## Future Improvements / Hardcore Level

* CI/CD pipelines for automatic deployment
* Advanced monitoring with **Azure Application Insights**
* Infrastructure as Code (Terraform / Azure CLI)
* Containerization (Docker) for Azure Functions

---

## License

This project is for **learning purposes** as part of the Azure Challenge at BeCode.

```
```
