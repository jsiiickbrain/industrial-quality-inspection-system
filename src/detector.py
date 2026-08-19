import cv2
from ultralytics import YOLO
from database import log_inspection

# تحميل نموذج YOLOv8 جاهز وخفيف (سيعمل على المعالج عادي)
model = YOLO("yolov8n.pt")

def process_image(image_path, item_id="ITEM_001"):
    """قراءة الصورة، كشف العيوب/الأجسام، وتسجيل النتيجة في قاعدة البيانات"""
    
    # قراءة الصورة
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image at {image_path}")
        return
    
    # تشغيل نموذج الذكاء الاصطناعي
    results = model(image)
    
    status = "PASSED"
    defect_type = "None"
    max_conf = 0.0
    
    # تحليلات النتائج
    for result in results:
        for box in result.boxes:
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            
            if conf > max_conf:
                max_conf = conf
            
            # محاكاة: افتراض أن كشف أجسام معينة يعتبر عيب صناعي
            status = "FAILED"
            defect_type = label

    # حفظ النتيجة في قاعدة البيانات
    log_inspection(item_id=item_id, status=status, confidence=round(max_conf, 2), defect_type=defect_type)
    print(f"Inspection Complete for {item_id}: Status={status}, Defect={defect_type}, Confidence={max_conf:.2f}")

if __name__ == "__main__":
    # تشغيل فحص تجريبي على الصورة test.jpg
    process_image("data/test.jpg", item_id="ITEM_TEST_01")