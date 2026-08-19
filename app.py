import streamlit as st
import sqlite3
import pandas as pd
import os

# إعداد صفحة الواجهة
st.set_page_config(page_title="Industrial Quality Dashboard", layout="wide")

st.title("🏭 Industrial AI Quality Inspection Dashboard")
st.markdown("Real-time monitoring and Analytics for automated manufacturing line.")

# الاتصال بقاعدة البيانات وقراءة السجلات
db_path = "inspection_data.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM inspection_logs ORDER BY id DESC", conn)
    conn.close()

    if not df.empty:
        # عرض المؤشرات الرئيسية (KPIs)
        col1, col2, col3, col4 = st.columns(4)
        
        total_inspections = len(df)
        passed_count = len(df[df['status'] == 'PASSED'])
        failed_count = len(df[df['status'] == 'FAILED'])
        pass_rate = (passed_count / total_inspections) * 100

        col1.metric("Total Inspections", total_inspections)
        col2.metric("Passed Items", passed_count)
        col3.metric("Failed Items", failed_count)
        col4.metric("Pass Rate", f"{pass_rate:.1f}%")

        st.markdown("---")

        # جدول البيانات التفاعلي
        st.subheader("📋 Recent Inspection Logs")
        st.dataframe(df, use_container_width=True)

        # رسم بياني لحالة المنتجات
        st.subheader("📊 Quality Distribution")
        status_counts = df['status'].value_counts()
        st.bar_chart(status_counts)

    else:
        st.info("No inspection logs available yet.")
else:
    st.warning("Database file not found. Please run the detector first.")