from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

from houses.models import RecruitNotice

BASE_URL = "https://www.reby24.com"
LIST_URL = f"{BASE_URL}/recruit"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

class Command(BaseCommand):
    help = "Reby24에서 청약 공고를 크롤링해 DB에 저장합니다."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("📦 Reby24 크롤링 시작"))

        soup = self.get_list_page()
        today = datetime.today().date()

        ul_list = soup.select("ul.list.m-padding-on")
        for ul in ul_list:
            # 🔗 링크 및 제목
            link_tag = ul.select_one("a[href*='bmode=view']")
            if not link_tag:
                continue
            detail_href = link_tag["href"]
            detail_url = detail_href if detail_href.startswith("http") else BASE_URL + detail_href

            li_tag = ul.select_one("li.tit")
            if not li_tag:
                continue

            category_tags = li_tag.select("em")
            category = category_tags[1].text.strip() if len(category_tags) >= 2 else ""

            title_tag = li_tag.select_one("span")
            title = title_tag.text.strip() if title_tag else "제목없음"

            # ✅ 썸네일 이미지 추출
            img_tag = ul.select_one("img.board_thumb")
            thumbnail = img_tag.get("src") if img_tag else None

            # ✅ 청약 접수일 추출
            apply_text = None
            small_tag = ul.select_one("small.text-block")
            if small_tag:
                raw = small_tag.decode_contents().replace("<br>", "\n")
                lines = raw.splitlines()
                for line in lines:
                    line = BeautifulSoup(line, "html.parser").get_text(strip=True)
                    if "청약접수" in line:
                        apply_text = line.split(":")[-1].strip()

            if not apply_text:
                print(f"❌ 청약접수일 못 찾음: {title}")
                continue

            start_date, end_date = self.extract_date(apply_text)
            if not start_date or not end_date:
                print(f"❌ 날짜 파싱 실패: {title}")
                continue

            # ✅ 상세페이지 정보
            location, scale, notice_url, winner_date = self.get_detail_data(detail_url)

            # ✅ 혼합 필터 적용
            is_active = end_date >= today
            is_waiting = winner_date and winner_date >= today

            if is_active:
                status = "접수중"
            elif is_waiting:
                status = "당첨대기"
            else:
                print(f"⛔ 제외됨: {title} (접수 마감 & 당첨자 발표 완료)")
                continue

            # ✅ region은 location이 있으면 앞 단어에서 추출 (예: 서울시 강남구 → 서울시)
            region = location.split()[0] if location else ""

            RecruitNotice.objects.update_or_create(
                detail_url=detail_url,
                defaults={
                    "title": title,
                    "category": category,
                    "region": region,
                    "apply_start": start_date,
                    "apply_end": end_date,
                    "image_url": thumbnail,
                    "location": location,
                    "scale": scale,
                    "notice_url": notice_url,
                    "winner_announcement_date": winner_date,
                    "status": status,
                }
            )

            print(f"✅ 저장됨: {title} | 상태: {status}")

        self.stdout.write(self.style.SUCCESS("🎉 Reby24 공고 저장 완료"))

    def get_list_page(self):
        res = requests.get(LIST_URL, headers=HEADERS)
        res.raise_for_status()
        return BeautifulSoup(res.text, "html.parser")

    def extract_date(self, text):
        match = re.search(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일.*?(\d{1,2})월\s*(\d{1,2})일", text)
        if match:
            start_date = datetime.strptime(f"{match.group(1)}-{match.group(2)}-{match.group(3)}", "%Y-%m-%d").date()
            end_date = datetime.strptime(f"{match.group(1)}-{match.group(4)}-{match.group(5)}", "%Y-%m-%d").date()
            return start_date, end_date

        match2 = re.search(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일", text)
        if match2:
            date = datetime.strptime(f"{match2.group(1)}-{match2.group(2)}-{match2.group(3)}", "%Y-%m-%d").date()
            return date, date
        return None, None

    def get_detail_data(self, detail_url):
        res = requests.get(detail_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        rows = soup.select("table.tbl_st tbody tr")
        location, scale, winner_date = None, None, None
        for row in rows:
            cols = row.select("th, td")
            if len(cols) < 2:
                continue

            key = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)

            if "공급위치" in key:
                location = value
            elif "공급규모" in key:
                scale = value
            elif "당첨자 발표일" in key:
                match = re.search(r"\d{4}-\d{2}-\d{2}", value)
                if match:
                    try:
                        winner_date = datetime.strptime(match.group(0), "%Y-%m-%d").date()
                    except Exception as e:
                        print(f"❌ 날짜 파싱 실패: {match.group(0)} → {e}")

        notice_link = None
        link_tag = soup.select_one('a.radius_btn')
        if link_tag and "href" in link_tag.attrs:
            notice_link = link_tag["href"]

        return location, scale, notice_link, winner_date
