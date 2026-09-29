# 🏭 Industrial Data Analytics & OEE Portfolio (Barcelona Market)

## 📌 Executive Summary
A professional, enterprise-grade Industrial Data Analysis project built from scratch to monitor plant performance, asset health, and maintenance costs. Designed for the Barcelona industrial sector, this project bridges the gap between IoT/plant floor operations and executive decision-making using a robust data pipeline and an interactive Power BI dashboard.

---

## 🛠️ Tech Stack & Architecture
* **Data Engineering & ETL:** Python (`sqlite3`, `csv`, `random`), simulating a 3-year continuous historical dataset (2019–2021).
* **Database Architecture:** SQLite relational database designed around a clean **Star Schema** (Fact and Dimension tables) to ensure high query performance and prevent Power BI relationship bottlenecks.
* **BI & Visualization:** Power BI Desktop (DAX measures, custom KPI formatting, and multi-page layout).

---

## 📐 Database Schema & Architecture
The database (`industrial_plant.db`) consists of:
1. **`equipment` (Dimension Table):** Contains asset metadata, unique primary keys (`equipment_id`), sectors (Stamping, Assembly, Machining, Finishing), and asset criticality.
2. **`production_logs` (Fact Table):** Daily operating records from 2019 to 2021 tracking planned vs. actual operating times, downtime (failures & maintenance), units produced, and defects.
3. **`maintenance_orders` (Fact Table):** Corrective and preventive work orders recording labor costs, parts costs, and repair downtime.

---

## 📊 Dashboard Structure (Power BI)

The report is split into three professional pages:
1. **Executive Overview:** High-level KPIs including Global Availability (OEE), Total Maintenance Cost, sectoral availability, and historical production trends (2019–2021).
2. **Operational Efficiency:** Deep dive into factory bottlenecks, featuring a downtime breakdown (Failures vs. Maintenance) by equipment and an operational performance matrix (Planned vs. Actual).
3. **Maintenance Management & Costs:** Financial analysis of maintenance types (Preventive vs. Corrective), Average MTTR (Mean Time to Repair), and an asset criticality cost ranking.

---

## 📈 Core DAX Measures
* **Global Availability (OEE):**
  ```dax
  Availability_Ratio = DIVIDE(SUM(production_logs[actual_operating_time_min]), SUM(production_logs[planned_operating_time_min]), 0)