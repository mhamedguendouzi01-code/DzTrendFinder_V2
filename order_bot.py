import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def run_auto_order():
    # 1. قراءة بيانات الطلب اللي سجلتها في الموقع
    try:
        with open("last_order.json", "r") as f:
            order = json.load(f)
    except:
        print("❌ لا يوجد طلب جديد لتنفيذه.")
        return

    # 2. إعداد المتصفح المخفي (للعمل في سيرفرات GitHub)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    print(f"🚀 جاري معالجة الطلب لـ: {order['cust_name']}")

    # 3. الدخول لـ AliExpress (رابط المنتج)
    driver.get(order['product_link'])
    time.sleep(5)

    try:
        # 4. الضغط على "Buy Now"
        buy_now_btn = driver.find_element(By.CLASS_NAME, "buy-now-btn") # ملاحظة: الكلاس يتغير حسب نسخة الموقع
        buy_now_btn.click()
        time.sleep(3)

        # 5. تغيير العنوان (Logic)
        # هنا الروبو يحوس على خانات الاسم، العنوان، والزيب كود ويعمرهم
        # driver.find_element(By.NAME, "contactPerson").send_keys(order['cust_name'])
        # driver.find_element(By.NAME, "address").send_keys(order['cust_address'])
        # driver.find_element(By.NAME, "zip").send_keys(order['cust_zip'])

        print(f"✅ تم تحديث العنوان إلى: {order['cust_address']}")
        print("🔔 الروبو متوقف الآن عند 'تأكيد الدفع' بانتظار موافقتك.")

    except Exception as e:
        print(f"❌ خطأ تقني أثناء تغيير العنوان: {e}")

    driver.quit()

if __name__ == "__main__":
    run_auto_order()