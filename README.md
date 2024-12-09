# 🌍 Real-Time Earthquake Monitoring Dashboard

Welcome to the **Real-Time Earthquake Monitoring Dashboard**! This project provides a live, interactive map showcasing earthquake data updated every hour. Leveraging data from the [USGS Earthquake API](https://earthquake.usgs.gov), this dashboard is designed to visualize and explore earthquake activity worldwide.

---

## ✨ Features

- **Real-Time Updates**: 
  - Automated API requests every hour using **Airflow**.
  - Earthquake map refreshes dynamically with the latest data.

- **Data Persistence**:
  - Earthquake data is stored securely in a **PostgreSQL database** for historical analysis.

- **Interactive Map**:
  - View earthquake locations, magnitudes, and details in an easy-to-use interface.

---

## 📚 How It Works

1. **API Integration**:
   - Fetches earthquake data from the [USGS Earthquake API](https://earthquake.usgs.gov).

2. **Data Storage**:
   - Stores structured data in a **PostgreSQL database** for efficient querying and long-term analysis.

3. **Data Pipeline**:
   - Built with **Apache Airflow** to automate API requests every hour.
   - Ensures data is always up-to-date in the database and on the dashboard.

4. **Dashboard**:
   - A sleek and responsive web app displays earthquake data on a map in real time.

---

## 🚀 Technologies Used

- **Backend**: Python, Flask, Dash
- **Database**: PostgreSQL
- **Data Pipeline**: Apache Airflow
- **Frontend**: Plotly, Dash
- **API**: USGS Earthquake API

---

## 📸 Screenshot


![app](https://github.com/user-attachments/assets/3db2a430-279b-45ef-abfe-1ff5e76af55f)


---

## 🛠️ Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/earthquake-dashboard.git
   cd earthquake-dashboard
