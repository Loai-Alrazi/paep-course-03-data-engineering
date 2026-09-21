# Student Performance Data Pipeline

## وصف المشروع

مشروع تدريبي لبناء **Data Engineering Pipeline** باستخدام Python وPandas لتحويل بيانات الطلاب الخام من ملف CSV إلى بيانات نظيفة، منظمة، متحقق منها، وجاهزة للاستخدام في مسارات Machine Learning.

يقوم المشروع بقراءة البيانات الخام، فحص بنيتها، تحويل أنواع البيانات، إزالة التكرارات، معالجة القيم المفقودة وغير الصالحة، تطبيق قواعد التحقق من جودة البيانات، ثم حفظ Dataset نهائية من نوع **ML-ready Dataset**.

---

## Pipeline

يمر تدفق البيانات بالمراحل التالية:

```text
Raw CSV
    ↓
Load
    ↓
Schema Validation
    ↓
Data Type Conversion
    ↓
Cleaning
    ↓
Data Validation
    ↓
Data Quality Report
    ↓
Save
    ↓
ML-ready Dataset
```

---

## هيكل المشروع

```text
student_data_pipeline/
│
├── data/
│   ├── raw/
│   │   └── students_raw.csv
│   │
│   └── processed/
│       └── students_ml_ready.csv
│
├── logs/
│   └── pipeline.log
│
├── src/
│   └── pipeline.py
│
├── tests/
│
├── requirements.txt
├── requirements.lock.txt
└── README.md
```

---

## الملفات الرئيسية

* `src/pipeline.py`
  يحتوي على كود الـ Data Pipeline ومراحل التحميل والتنظيف والتحقق والحفظ.

* `data/raw/students_raw.csv`
  ملف البيانات الخام الأصلي. يجب الاحتفاظ به دون تعديل مباشر.

* `data/processed/students_ml_ready.csv`
  ملف البيانات النهائي بعد التنظيف والتحقق.

* `logs/pipeline.log`
  يحتوي على سجل تشغيل الـ Pipeline والأخطاء التي تحدث أثناء التنفيذ.

* `requirements.txt`
  يحتوي على المكتبات المطلوبة لتشغيل المشروع.

* `requirements.lock.txt`
  يحتوي على إصدارات المكتبات المثبتة بهدف تحسين قابلية إعادة تشغيل المشروع بنفس البيئة.

* `tests/`
  يحتوي على اختبارات المشروع.

---

## الأعمدة المطلوبة

يجب أن يحتوي ملف البيانات على الأعمدة التالية:

```text
student_id
name
age
gpa
attendance
city
```

إذا كان أحد الأعمدة المطلوبة غير موجود، تفشل مرحلة **Schema Validation** وتتوقف الـ Pipeline.

---

## Data Quality Rules

تطبق الـ Pipeline مجموعة من قواعد جودة البيانات، أهمها:

* `student_id` يجب ألا يكون فارغًا.
* `student_id` يجب أن يكون فريدًا.
* `name` يجب ألا يكون فارغًا.
* `age` يجب أن يكون بين `16` و`80`.
* `gpa` يجب أن يكون بين `0` و`4`.
* `attendance` يجب أن يكون بين `0` و`100`.
* يتم التعامل مع الصفوف المكررة.
* يتم تنظيف المسافات الزائدة في الحقول النصية.
* يتم توحيد تنسيق أسماء المدن.
* يتم التعامل مع القيم المفقودة في الأعمدة الرقمية وفق استراتيجية التنظيف المحددة في الـ Pipeline.

عند فشل قواعد التحقق النهائية، يتم إيقاف التنفيذ وعدم اعتبار البيانات **ML-ready**.

---

## Input

ملف البيانات الخام:

```text
data/raw/students_raw.csv
```

يتم الاحتفاظ بالملف الخام في حالته الأصلية لدعم:

* Reprocessing
* Debugging
* Auditing
* Comparison
* Recovery
* Reproducibility

---

## Output

بعد نجاح جميع مراحل التنظيف والتحقق، يتم إنشاء:

```text
data/processed/students_ml_ready.csv
```

وهو Dataset نظيف ومتحقق منه ومجهز للاستخدام في مسار Machine Learning.

---

## Data Quality Report

تقوم الـ Pipeline بإنشاء وعرض تقرير جودة للبيانات يحتوي على معلومات مثل:

* اسم العمود.
* نوع البيانات.
* عدد القيم المفقودة.
* نسبة القيم المفقودة.
* عدد القيم الفريدة.

يساعد التقرير في فهم حالة البيانات النهائية ومراجعة جودة الـ Dataset.

---

## Logging

تسجل الـ Pipeline معلومات التنفيذ والأخطاء داخل:

```text
logs/pipeline.log
```

يتضمن السجل أحداثًا مثل:

```text
Pipeline started.
Loading data...
Data loaded successfully.
Processed data saved.
Pipeline completed successfully.
```

وعند حدوث خطأ، يتم تسجيل معلومات الخطأ للمساعدة في عملية Debugging.

---

## إعداد البيئة

من داخل مجلد المشروع، أنشئ Virtual Environment إذا لم تكن موجودة:

```powershell
python -m venv .venv
```

ثم ثبّت المكتبات المطلوبة:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

ولإعادة تثبيت الإصدارات المسجلة نفسها يمكن استخدام:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
```

---

## تشغيل الـ Pipeline

شغّل:

```powershell
.\.venv\Scripts\python.exe .\src\pipeline.py
```

عند نجاح التنفيذ:

* تتم قراءة البيانات الخام.
* يتم التحقق من بنية البيانات.
* يتم تحويل أنواع البيانات.
* تتم معالجة التكرارات والقيم غير الصالحة والمفقودة.
* يتم تطبيق قواعد التحقق.
* يتم عرض Data Quality Report.
* يتم حفظ الـ ML-ready Dataset.
* يتم تسجيل تفاصيل التنفيذ داخل `pipeline.log`.

---

## معالجة الأخطاء

تستخدم الـ Pipeline آلية Exception Handling لمنع استمرار المعالجة عند وجود مشكلة تؤثر على موثوقية البيانات.

من أمثلة الحالات التي تؤدي إلى فشل التنفيذ:

* ملف الإدخال غير موجود.
* Dataset فارغة.
* عمود مطلوب غير موجود.
* `student_id` غير صالح أو مفقود.
* وجود `student_id` مكرر بعد التنظيف.
* فشل إحدى قواعد Data Validation.
* عدم وجود قيم رقمية صالحة تسمح بتنفيذ استراتيجية المعالجة المطلوبة.

عند فشل التحقق النهائي، لا يتم اعتبار البيانات جاهزة للاستخدام في Machine Learning.

---

## تشغيل الاختبارات

لتشغيل اختبارات المشروع:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

---

## التقنيات المستخدمة

* Python
* Pandas
* pathlib
* Logging
* CSV
* unittest
* Git

---

## الهدف التعليمي

يهدف المشروع إلى تطبيق دورة معالجة بيانات مبسطة:

```text
Data Source
    ↓
Data Ingestion
    ↓
Raw Storage
    ↓
Data Processing
    ↓
Data Cleaning
    ↓
Data Validation
    ↓
ML-ready Dataset
```

والهدف الأساسي هو فهم أن بناء نظام Machine Learning موثوق يبدأ أولًا من بناء مسار بيانات موثوق وقابل للتتبع وإعادة التشغيل.
