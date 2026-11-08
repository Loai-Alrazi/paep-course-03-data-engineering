import pandas as pd
import requests


# ==========================================================
# إعداد عنوان الـ API
# ==========================================================

API_URL = (
    "https://jsonplaceholder.typicode.com/users"
)


# ==========================================================
# 1. إرسال GET Request
# ==========================================================

try:

    response = requests.get(
        API_URL,
        timeout=10
    )

    # إذا أعاد السيرفر HTTP Error
    # فسيتم رفع Exception
    response.raise_for_status()

except requests.RequestException as exc:

    print(
        "حدث خطأ أثناء الاتصال بالـ API:"
    )

    print(exc)

    raise


# ==========================================================
# 2. تحويل JSON Response إلى Python Object
# ==========================================================

data = response.json()


# ==========================================================
# 3. معرفة نوع البيانات المستلمة
# ==========================================================

print(
    "Data type:",
    type(data)
)


# ==========================================================
# 4. عرض أول عنصر
# ==========================================================
# الـ API يعيد قائمة من المستخدمين،
# وكل مستخدم عبارة عن Dictionary.

print(
    "\nFirst record:"
)

print(
    data[0]
)


# ==========================================================
# 5. الوصول إلى قيم داخل JSON
# ==========================================================

print(
    "\nFirst user name:"
)

print(
    data[0]["name"]
)


# ==========================================================
# 6. المرور على البيانات
# ==========================================================

print(
    "\nUsers:"
)

for user in data:

    print(
        user["id"],
        "-",
        user["name"]
    )


# ==========================================================
# 7. تحويل JSON إلى Pandas DataFrame
# ==========================================================

df = pd.DataFrame(data)


print(
    "\n========== DATAFRAME =========="
)

print(
    df.head()
)


# ==========================================================
# 8. فحص البيانات
# ==========================================================

print(
    "\nShape:"
)

print(
    df.shape
)


print(
    "\nColumns:"
)

print(
    df.columns
)


print(
    "\nData Types:"
)

print(
    df.dtypes
)


# ==========================================================
# 9. اختيار أعمدة نحتاجها فقط
# ==========================================================

users_df = df[
    [
        "id",
        "name",
        "username",
        "email",
        "phone",
        "website"
    ]
]


print(
    "\nSelected Data:"
)

print(
    users_df
)


# ==========================================================
# 10. Query Parameters
# ==========================================================

PARAMS_URL = (
    "https://jsonplaceholder.typicode.com/posts"
)


# نمرر Parameters كـ Dictionary
params = {
    "userId": 1
}


response = requests.get(
    PARAMS_URL,
    params=params,
    timeout=10
)

response.raise_for_status()


posts = response.json()


print(
    "\n========== PARAMETERS =========="
)

print(
    "Final URL:"
)

print(
    response.url
)


print(
    "\nNumber of posts:"
)

print(
    len(posts)
)


print(
    "\nFirst post:"
)

print(
    posts[0]
)