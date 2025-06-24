#!/bin/bash

echo "📦 fixture 덤프 시작..."

python manage.py dumpdata accounts.User --indent 2 > fixtures/users.json
echo "✅ users.json 저장 완료"

python manage.py dumpdata products.FinancialProduct > fixtures/financial_products.json
echo "✅ financial_products.json 저장 완료"

python manage.py dumpdata houses.CompetitionRate > fixtures/competition_rates.json
echo "✅ competition_rates.json 저장 완료"

echo "📦 청약 공고 데이터 저장 중..."
python manage.py dumpdata houses.RecruitNotice --indent 2 > fixtures/recruit_notices.json
echo "✅ recruit_notices.json 저장 완료"


echo "🎉 모든 fixture 백업 완료!"
