from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
import pytz
import math

#料金テーブルクラス 今後追加予定
class RateTable:
    def __init__(self):
        self.rates = {
            0:{"adult": 1000,"child":500,"senior":800},
            1:{"adult": 600, "child":400,"senior":500},
        }

    #通常料金の取得
    def get_base_rate(self):
        return self.rates.get(0)
    #特別料金の取得
    def get_discount_rate(self,discount):
        return self.rates.get(discount,None)

#料金計算アルゴリズム
class Command(BaseCommand):
    help = '料金計算用'

    def handle(self, *args, **options):
        tokyo_timezone = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tokyo_timezone)
        weekday = now.weekday()
        
        rate_table = RateTable()
        rate = rate_table.get_base_rate()

        #大人人数
        adults = options['adults']
        children = options['children']
        seniors = options['seniors']

        #合計人数
        total_people = adults + children + seniors


        #料金明細用
        charge_details_data = {}

        #料金明細差額一時保存変数
        disvalue = 0

        #金額変更前の合計料金
        total_base = (adults * rate.get('adult'))+ (children * rate.get('child'))+(seniors * rate.get('senior'))

        #販売合計金額
        sales_amount = total_base
        try:
            #特別タイプの場合
            if options['discount'] > 0:
                rate = rate_table.get_discount_rate(options['discount'])
                if rate == None:
                    raise CommandError("discount codeに誤りがあります。設定を見直してください")
                sales_amount = (adults * rate.get('adult'))+ (children * rate.get('child'))+ (seniors * rate.get('senior'))

                charge_details_data["タイプ割引価格"] = [
                    f"大人 {adults}×{rate.get('adult')}",
                    f"子供 {children}×{rate.get('child')}",
                    f"シニア {seniors}×{rate.get('senior')}",
                    f"小計 {sales_amount}円"
                    ]
            #普通タイプの場合
            else:
                charge_details_data["基本価格"] = [
                    f"大人 {adults}×{rate.get('adult')}",
                    f"子供 {children}×{rate.get('child')}",
                    f"シニア {seniors}×{rate.get('senior')}",
                    f"小計 {total_base}円"
                ]
                
            #団体割引確認
            if (adults+ (children * 0.5) + options['seniors']) >= 10:
                disvalue = sales_amount * 0.9
                charge_details_data["団体割引"] = ["-10%",f"-{math.floor(sales_amount - disvalue)}円"]

                sales_amount = disvalue

            #時間割引確認
            if now.hour >= 17:
                disvalue = (total_people) * 100
                sales_amount = sales_amount - disvalue

                charge_details_data["時間割引"] = [f"{total_people}×100円",f"-{math.floor(disvalue)}円"]


            #休日確認
            if weekday == 5 or weekday == 6 or options['holiday'] == 1:
                disvalue = (total_people) * 200
                sales_amount = sales_amount + disvalue 

                charge_details_data["休日料金"] = [f"{total_people}×200円",f"+{math.floor(disvalue)}円"]

            #曜日割引確認
            if weekday == 0 or weekday == 2:
                disvalue = (total_people) * 100
                sales_amount = sales_amount - disvalue

                charge_details_data["曜日割引"] = [f"{total_people}×100円",f"-{math.floor(disvalue)}円"]
        except Exception as e:
            raise CommandError(f"error occurred:{e}")

        #️出力結果
        print(f"販売合計金額:{math.floor(sales_amount)}円")
        print(f"金額変更前合計金額:{math.floor(total_base)}円")
        print("料金明細")
        print("******************************************************************")
        print(f"販売日付:{now.strftime('%Y-%m-%d %H:%M:%S')}")
        for i in charge_details_data:
            print(f"{i}:",end=" ")
            for k in charge_details_data[i]:
                print(f"{k} ",end=" ")
            print()
        print("******************************************************************")
    
    #コンソール引数
    def add_arguments(self, parser):
        try:
            parser.add_argument('adults',type=int)
            parser.add_argument('children',type=int)
            parser.add_argument('seniors',type=int)
            parser.add_argument('--discount',default = 0,type=int)
            parser.add_argument('--holiday',default = 0, type=int)
        except Exception as e:
            raise CommandError(f"error occurred:{e}")