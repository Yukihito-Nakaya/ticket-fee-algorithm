#!/bin/bash
#団体割確認　
#10人以上　指定無し
docker exec -it ticketFee python manage.py calculation 5 2 4 > test_result.txt
#10人未満　指定無し
docker exec -it ticketFee python manage.py calculation 2 8 3 >> test_result.txt

#特別料金 月曜日　曜日割引　団体割引
docker exec -it ticketFee python manage.py calculation 10 0 0 --discount 1 --holiday 0 --weekday 0 --time "10:30" >> test_result.txt

#火曜日 + 時間割引 +　休日料金
docker exec -it ticketFee python manage.py calculation 2 10 0 --discount 0 --holiday 1 --weekday 1 --time "17:30" >> test_result.txt

#特別料金 水曜日　曜日割引　団体割引　時間割引
docker exec -it ticketFee python manage.py calculation 2 3 9 --discount 1 --holiday 1 --weekday 2 --time "19:00" >> test_result.txt
#木曜日 割引なし　増加無し
docker exec -it ticketFee python manage.py calculation 2 9 3 --discount 0 --holiday 0 --weekday 3 --time "15:00" >> test_result.txt

#料金タイプ存在しないものを選択　
docker exec -it ticketFee python manage.py calculation 2 8 3 --discount 4 >> test_result.txt

#holiday 0,1 意外
docker exec -it ticketFee python manage.py calculation 2 8 3 --discount 1 --holiday 4 >> test_result.txt

