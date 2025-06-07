import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

st.set_page_config(page_title="CRM Audit", layout="wide")
st.title("📊 CRM Data Audit & Customer Segmentation")

# Load data
df = pd.read_excel("data/Online Retail.xlsx")
df['Total'] = df['Quantity'] * df['UnitPrice']
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Clean data
df_clean = df.dropna(subset=['CustomerID'])
df_clean = df_clean[df_clean['Quantity'] >= 0]
df_clean = df_clean.drop_duplicates()
df_clean['Total'] = df_clean['Quantity'] * df_clean['UnitPrice']
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
df_clean['Month'] = df_clean['InvoiceDate'].dt.to_period("M")

# RFM Calculation
rfm = df_clean.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (df_clean['InvoiceDate'].max() - x.max()).days,
    'InvoiceNo': 'nunique',
    'Total': 'sum'
}).rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'Total': 'Monetary'
})

# Standardize
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)

# Fit final model
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm['Segment'] = kmeans.fit_predict(rfm_scaled)

# Label segments
segment_labels = {
    0: "At Risk",
    1: "VIP",
    2: "Inactive",
    3: "Loyal"
}
rfm['SegmentLabel'] = rfm['Segment'].map(segment_labels)

# Sidebar navigation
tabs = st.sidebar.radio("📂 Select Page", ["Data Audit", "Segmentation", "Strategy"])

if tabs == "Data Audit":
    st.subheader("🔍 Initial Data Snapshot")
    st.dataframe(df.head())

    st.markdown("### 📈 Data Overview")
    st.write(f"**Total Rows:** {df.shape[0]}")
    st.write(f"**Total Columns:** {df.shape[1]}")
    st.write("**Missing Values by Column:**")
    st.dataframe(df.isnull().sum().sort_values(ascending=False))

    st.markdown("### 🛍️ Top Countries by Transaction Volume")
    st.bar_chart(df_clean['Country'].value_counts().head(10))

    st.markdown("### 📅 Monthly Invoices")
    monthly_sales = df_clean.groupby('Month')['InvoiceNo'].nunique()
    fig1, ax1 = plt.subplots()
    monthly_sales.plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

    missing_pct = df['CustomerID'].isnull().mean() * 100
    dup_pct = df.duplicated().mean() * 100
    neg_qty_pct = (df['Quantity'] < 0).mean() * 100
    score = 100 - missing_pct - dup_pct * 0.5 - neg_qty_pct * 0.5

    st.markdown("### ✅ Data Quality Score")
    st.metric(label="Data Quality Score", value=f"{round(score, 1)} / 100")
    st.download_button("📥 Download Cleaned Data", df_clean.to_csv(index=False), file_name="crm_cleaned.csv")

elif tabs == "Segmentation":
    st.subheader("📊 RFM Segmentation")

    # Determine optimal k
    inertias = []
    silhouettes = []
    K = range(2, 6)
    for k in K:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(rfm_scaled)
        inertias.append(model.inertia_)
        silhouettes.append(silhouette_score(rfm_scaled, labels))

    st.markdown("#### 🔢 Optimal Cluster Selection")
    fig2, ax2 = plt.subplots()
    ax2.plot(K, inertias, label="Inertia", marker='o')
    ax2.set_xlabel("k")
    ax2.set_ylabel("Inertia")
    ax2.set_title("Elbow Method")
    st.pyplot(fig2)

    st.markdown("### 🎯 Segment Profile")
    segment_summary = rfm.groupby('SegmentLabel').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean',
        'SegmentLabel': 'count'
    }).rename(columns={'SegmentLabel': 'Customer Count'})
    st.dataframe(segment_summary.style.background_gradient(cmap='Blues'))
    st.download_button("📥 Download Segmented Data", rfm.to_csv(index=False), file_name="rfm_segmented.csv")

elif tabs == "Strategy":
    st.subheader("🧭 Segment Strategy Recommendations")

    strategies = {
        "VIP": "Offer exclusives, early access, and premium service.",
        "Loyal": "Nurture with loyalty programs and personal touches.",
        "At Risk": "Send win-back campaigns and ask for feedback.",
        "Inactive": "Suppress or retarget with special offers."
    }

    selected_segment = st.selectbox("Select a Segment", list(strategies.keys()))
    st.markdown(f"**Segment:** {selected_segment}")
    st.markdown(f"**Strategy:** {strategies[selected_segment]}")

    st.bar_chart(rfm['SegmentLabel'].value_counts())
