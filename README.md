# CRM Data Audit & Customer Segmentation (Demo)

This interactive Streamlit app demonstrates a real-world CRM data audit and customer segmentation using Python and machine learning.

🔗 **Live App**: [Open Streamlit Demo](https://crm-audit-demo-svquqx4kpxechxtrdvj9wg.streamlit.app)  
📁 **Repository**: [View on GitHub](https://github.com/jhdatastudio/crm-audit-demo)

---

## 🚀 Project Overview

This demo analyzes a real CRM export dataset to:
- Identify missing values, duplicates, and invalid records
- Visualize key metrics such as monthly activity and top countries
- Segment customers using **RFM (Recency, Frequency, Monetary)** analysis
- Apply **KMeans clustering** with silhouette validation
- Assign actionable labels (e.g. VIP, Loyal, At Risk)
- Recommend retention strategies per segment

---

## 🛠️ Technologies Used

- **Python** (Pandas, scikit-learn, Matplotlib, Seaborn)
- **Streamlit** for interactive web app
- **OpenPyXL** to handle Excel input
- Cached processing for fast, reusable deployment

---

## 📊 App Features

- 🔍 **Data Quality Audit**: Explore missing data, duplicates, invalid transactions
- 📅 **Sales Trends**: Monthly invoice volumes and top customer regions
- 📈 **Clustering**: Optimal `k` detection using elbow + silhouette methods
- 🎯 **Segment Profiles**: Mean RFM values and customer counts per group
- 🧭 **Strategy Tab**: Actionable marketing recommendations by segment

---

## 📂 Project Structure

- 📁 data/ # CRM dataset
- 📁 notebooks/ # Exploratory notebook version
- 📄 streamlit_app.py # Main app file within the notebooks folder
- 📄 requirements.txt # Dependencies for Streamlit Cloud

## 🌐 About JH Data Studio

JH Data Studio offers tailored data consulting services across AI, analytics, and automation — empowering businesses to make smarter decisions faster.

👉 Visit jhdatastudio.com to learn more or book a discovery call.