import csv
import time

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

search_query = "삼쩜삼"
search_url = f"https://search.naver.com/search.naver?where=news&query={search_query}"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--lang=ko_KR")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(search_url)

wait = WebDriverWait(driver, 20)
wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

recent_news_xpath = '//*[@id="snb"]/div/div/div/a[2]'
wait.until(EC.presence_of_element_located((By.XPATH, recent_news_xpath)))

# 최신순클릭
recent_news_element = driver.find_element(By.XPATH, recent_news_xpath)
recent_news_element.click()
wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

# 뉴스 최신 20까지 로딩이 안되어 스크롤2회 동작을 통해서 최신 뉴스 20까지 불러옴
for _ in range(2):
    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(1)

# 최신 뉴스 20까지 로딩되었는지 대기
news_result_xpath = '//*[@id="sp_nws20"]'
wait.until(EC.presence_of_element_located((By.XPATH, news_result_xpath)))

# 뉴스 리스트 저장소
news_list = []

# 최신뉴스 20개를 뉴스 리스트 저장소에 저장
for i in range(1, 21):
    try:
        news_title_xpath = f'//*[@id="sp_nws{str(i)}"]/div/div/div[2]/a[2]'
        news_title_element = driver.find_element(By.XPATH, news_title_xpath)
    except:
        news_title_2_xpath = f'//*[@id="sp_nws{str(i)}"]/div/div/div[2]/a'
        news_title_element = driver.find_element(By.XPATH, news_title_2_xpath)
    news_title = news_title_element.text
    print(news_title)
    try:
        news_url_xpath = f'//*[@id="sp_nws{str(i)}"]/div/div/div[2]/a'
        news_url_element = driver.find_element(By.XPATH, news_url_xpath)
    except:
        news_url_2_xpath = f'//*[@id="sp_nws{str(i)}"]/div/div/div[2]/a[2]'
        news_url_element = driver.find_element(By.XPATH, news_url_2_xpath)
    news_url = news_url_element.get_attribute("href")
    print(news_url)
    news_list.append({"No.":str(i) ,"제목": news_title, "URL": news_url})
    time.sleep(1)
driver.quit()

# 저장된 최신뉴스 정보를 CSV 파일로 저장
csv_file_path = "네이버뉴스_최신20개.csv"
with open(csv_file_path, "w", encoding="utf-8", newline="") as csv_file:
    fieldnames = ["No.","제목", "URL"]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(news_list)

print(f"뉴스 정보가 {csv_file_path} 파일로 저장되었습니다.")