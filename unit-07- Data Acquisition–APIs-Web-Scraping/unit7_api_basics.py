import requests


# ==========================================================
# 1. عنوان الموقع الذي سنرسل إليه GET Request
# ==========================================================

URL = "https://jsonplaceholder.typicode.com/users"


# ==========================================================
# 2. إرسال GET Request
# ==========================================================
# timeout يمنع البرنامج من الانتظار إلى ما لا نهاية
# إذا لم يستجب السيرفر خلال الوقت المحدد.

response = requests.get(
    URL,
    timeout=10
)


# ==========================================================
# 3. قراءة Status Code
# ==========================================================

print(
    "Status Code:",
    response.status_code
)


# ==========================================================
# 4. التحقق اليدوي من نجاح الطلب
# ==========================================================

if response.status_code == 200:
    print(
        "Request succeeded."
    )
else:
    print(
        "Request failed:",
        response.status_code
    )


# ==========================================================
# 5. استخدام raise_for_status
# ==========================================================
# إذا كان Status Code يمثل HTTP Error
# ستقوم requests برفع Exception تلقائيًا.

try:

    response.raise_for_status()

    print(
        "No HTTP error occurred."
    )

except requests.RequestException as exc:

    print(
        "HTTP request failed:",
        exc
    )


# ==========================================================
# 6. قراءة جزء من Response Body
# ==========================================================
# example.com يعيد HTML وليس JSON،
# لذلك نستخدم response.text هنا.

print(
    "\nResponse preview:"
)

print(
    response.json()
)