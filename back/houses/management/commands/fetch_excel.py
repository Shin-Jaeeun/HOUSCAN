import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.core.management.base import BaseCommand
from houses.models import CompetitionRate

# 지금 맥북 기준 코드임!!!!!

class Command(BaseCommand):
    help = '청약 경쟁률 엑셀/CSV 자동 다운로드 + DB 저장'

    def handle(self, *args, **kwargs):
        DOWNLOAD_DIR = "/Users/tlsworma/Desktop/pjt/09-pjt/back/downloads"
        MAC_DEFAULT_DOWNLOAD = os.path.expanduser("~/Downloads")
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        self.stdout.write(f"📂 다운로드 경로 설정됨: {DOWNLOAD_DIR}")

        # ✅ 크롬 옵션 설정
        options = Options()
        prefs = {
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        # options.add_argument('--headless=new')  # GUI 없이 실행 시 주석 제거
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        try:
            self.stdout.write("🟡 크롬 드라이버 실행 중...")
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(15)

            url = "https://www.data.go.kr/data/15110988/fileData.do"
            driver.get(url)
            self.stdout.write(f"🌐 페이지 진입: {url}")
            wait = WebDriverWait(driver, 10)

            self.stdout.write("🟢 다운로드 버튼 탐색 중...")
            download_btn = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//a[contains(@class, 'button') and contains(@onclick, 'fileDetailObj.fn_fileDataDown')]"
            )))
            download_btn.click()
            self.stdout.write("✅ 다운로드 클릭 완료")

            # ✅ 최대 20초 동안 파일 다운로드 대기 (.crdownload 제외)
            def find_latest_file(*paths):
                for path in paths:
                    files = sorted(
                        [os.path.join(path, f) for f in os.listdir(path)
                         if not f.endswith(".crdownload") and f.endswith((".xlsx", ".xls", ".csv"))],
                        key=os.path.getctime,
                        reverse=True
                    )
                    if files:
                        return files[0]
                return None

            latest_file = None
            for i in range(20):
                latest_file = find_latest_file(DOWNLOAD_DIR, MAC_DEFAULT_DOWNLOAD)
                if latest_file:
                    break
                time.sleep(1)

            if not latest_file:
                self.stderr.write("❌ 다운로드된 파일을 찾을 수 없습니다.")
                self.stderr.write(f"📂 downloads/: {os.listdir(DOWNLOAD_DIR)}")
                self.stderr.write(f"📂 ~/Downloads/: {os.listdir(MAC_DEFAULT_DOWNLOAD)}")
                return

            self.stdout.write(f"📁 최신 파일: {latest_file}")
            ext = os.path.splitext(latest_file)[1].lower()

            # ✅ 파일 읽기
            if ext == '.csv':
                try:
                    df = pd.read_csv(latest_file, encoding='utf-8')
                except UnicodeDecodeError:
                    df = pd.read_csv(latest_file, encoding='cp949')
            elif ext in ['.xls', '.xlsx']:
                df = pd.read_excel(latest_file)
            else:
                self.stderr.write("❌ 지원하지 않는 파일 형식입니다.")
                return

            self.stdout.write(f"📊 데이터 미리보기:\n{df.head()}")

            # ✅ 안전한 변환 함수
            def safe_int(val):
                try:
                    return int(str(val).replace(',', '').replace('(△', '-').replace('△', '-').replace(')', ''))
                except:
                    return None

            def safe_float(val):
                try:
                    return float(str(val).replace(',', '').replace('(△', '-').replace('△', '-').replace(')', ''))
                except:
                    return None

            # ✅ DB 저장
            for _, row in df.iterrows():
                CompetitionRate.objects.create(
                    year_month=row['연월'],
                    region=row['시도'],
                    special_supply_units=safe_int(row['특별공급 공급세대수']),
                    special_applications=safe_int(row['특별공급 접수건수']),
                    special_competition_rate=safe_float(row['특별공급 경쟁률']),
                    general_supply_units=safe_int(row['일반공급 공급세대수']),
                    general_applications=safe_int(row['일반공급 접수건수']),
                    general_competition_rate=safe_float(row['일반공급 경쟁률']),
                )

            self.stdout.write("✅ DB 저장 완료!")

        except Exception as e:
            self.stderr.write(f"❌ 오류 발생: {e}")

        finally:
            if 'driver' in locals():
                driver.quit()
