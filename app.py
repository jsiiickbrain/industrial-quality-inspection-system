import streamlit as st
import sqlite3
import pandas as pd
import os
import numpy as np
from PIL import Image
from ultralytics import YOLO

# إعداد صفحة الواجهة
st.set_page_config(page_title="Industrial Quality Dashboard", layout="wide")

st.title("🏭 Industrial AI Quality Inspection Dashboard")
st.markdown("Real-time monitoring and Analytics for automated manufacturing line.")

# تحكم جانبي لرفع الصور
st.sidebar.header("🔍 Image Testing")
uploaded_file = st.sidebar.file_uploader("Upload an item image for inspection...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # قراءة الصورة
    image = Image.open(uploaded_file)
    
    # عرض الصورة المرفوعة في القائمة الجانبية
    st.sidebar.image(image, caption="Uploaded Image", use_container_width=True)
    
    img_array = np.array(image)
    
    # تحميل نموذج الذكاء الاصطناعي للفحص
    model = YOLO("yolov8n.pt")
    results = model(img_array)
    
    # فحص العيوب
    detections = results[0].boxes
    defect_detected = len(detections) > 0
    status = "FAILED" if defect_detected else "PASSED"
    defect_type = "Defect Found" if defect_detected else "None"
    confidence = float(detections.conf[0]) if defect_detected else 0.0

    st.sidebar.success(f"Inspection Result: {status}")
    
    # حفظ النتيجة في قاعدة البيانات
    db_path = "inspection_data.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inspection_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            item_id TEXT,
            status TEXT,
            confidence REAL,
            defect_type TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO inspection_logs (item_id, status, confidence, defect_type)
        VALUES (?, ?, ?, ?)
    ''', (f"UPLOAD_{uploaded_file.name}", status, confidence, defect_type))
    conn.commit()
    conn.close()

# عرض البيانات من قاعدة البيانات
db_path = "inspection_data.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM inspection_logs ORDER BY id DESC", conn)
    conn.close()

    if not df.empty:
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

        st.subheader("📋 Recent Inspection Logs")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Quality Distribution")
        status_counts = df['status'].value_counts()
        st.bar_chart(status_counts)