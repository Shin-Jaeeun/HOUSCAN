import requests
from django.core.management.base import BaseCommand
from products.models import FinancialProduct
from datetime import datetime

API_KEY = '84fb3ed7f7d193a5ed4326d269a0bfe4'

DEPOSIT_URL = f'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
SAVING_URL = f'https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'


class Command(BaseCommand):
    help = '금융감독원 API에서 정기예금 및 적금 상품 데이터를 가져와 저장합니다.'

    def handle(self, *args, **options):
        self.stdout.write("📡 금융상품 데이터 가져오는 중...")
        for url in [DEPOSIT_URL, SAVING_URL]:
            self.fetch_and_save(url)

    def fetch_and_save(self, url):
        res = requests.get(url)
        if res.status_code != 200:
            self.stdout.write(self.style.ERROR("❌ API 요청 실패"))
            return

        data = res.json()
        base_list = data['result']['baseList']
        option_list = data['result']['optionList']

        for base in base_list:
            matching_options = [opt for opt in option_list if opt['fin_prdt_cd'] == base['fin_prdt_cd']]

            for opt in matching_options:
                FinancialProduct.objects.create(
                        name=base.get('fin_prdt_nm', ''),
                        institution=base.get('kor_co_nm', ''),
                        join_method=base.get('join_way', ''),
                        maturity_interest_rate=opt.get('mtrt_int', 0),
                        preferential_condition=base.get('spcl_cnd', ''),
                        join_limit=base.get('join_deny', ''),
                        join_target=base.get('join_member', ''),
                        max_limit=base.get('max_limit', ''),
                        notice=base.get('etc_note', ''),
                        option_interest_type=opt.get('intr_rate_type', ''),
                        option_payment_type=opt.get('rsrv_type', ''),
                        option_saving_period=opt.get('save_trm', ''),
                        option_base_rate=opt.get('intr_rate', 0),
                        option_max_rate=opt.get('intr_rate2', 0),

                        max_monthly_payment=1000000,  # 추후 계산 가능
                        goal_asset=0,  # 사용자 기반 아님
                        target_date=datetime.now().date(),  # 임시
                        preferred_type='예금' if 'deposit' in url else '적금'
                )

        self.stdout.write(self.style.SUCCESS(f"✅ {len(base_list)}개 상품 저장 완료"))
