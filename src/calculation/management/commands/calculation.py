from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
import pytz

#料金テーブルクラス
class RateTable:
    def __init__(self):
        self.rates = {
            0:{"adult": 1000,"child":500,"senior":800},
            1:{"adult": 600, "child":400,"senior":500},
        }

    def get_base_rate(self):
        return self.rates.get(0)
    
    def get_discount_rate(self,discount):
        return self.rates.get(discount)

#料金計算アルゴリズム
class Command(BaseCommand):
    help = '料金計算用'

    def handle(self, *args, **options):
        tokyo_timezone = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tokyo_timezone)
        weekday = now.weekday()
        
        rate_table = RateTable()
        rate = rate_table.get_base_rate()

        #料金明細用
        charge_details_data = {}
        #料金明細差額一時保存変数
        disvalue = 0

        #金額変更前の合計料金
        total_base = (options['adults'] * rate.get('adult'))
        + (options['childs'] * rate.get('child'))
        + (options['seniors'] * rate.get('senior'))

        #販売合計金額
        sales_amount = total_base
        
        #特別タイプの場合
        if options['discount'] > 0:
            rate = rate_table.get_discount_rate(options['discount'])
            sales_amount = (options['adults'] * rate.get('adult'))
            + (options['childs'] * rate.get('child'))
            + (options['seniors'] * rate.get('senior'))
            charge_details_data["タイプ割引価格"] = [
                f"大人:{options['adults']}×{rate.get('adult')}",
                f"子供:{options['childs']}×{rate.get('child')}",
                f"シニア:{options['seniors']}×{rate.get('senior')}",
                f"{sales_amount}"
                ]
            
        #団体割引確認
        if (options['adults']+ (options['childs'] * 0.5) + options['seniors']) >= 10:
            disvalue = sales_amount * 0.9
            sales_amount = disvalue

            charge_details_data["団体割引"] = ["-10%",f"-{disvalue}"]

        #時間割引確認
        if now.hour >= 17:
            disvalue = (options['adults']+ options['childs'] + options['seniors']) * 100
            sales_amount = sales_amount - disvalue

            charge_details_data["時間割引"] = [f"-{options['adults']+ options['childs'] + options['seniors']}×100円",f"-{disvalue}"]


        #休日確認
        if weekday == 5 or weekday == 6 or options['holiday'] == 1:
            disvalue = (options['adults']+ options['childs'] + options['seniors']) * 200
            sales_amount = sales_amount + disvalue 

            charge_details_data["休日料金"] = [f"+{options['adults']+ options['childs'] + options['seniors']}×200円",f"+{disvalue}"]

        #曜日割引確認
        if weekday == 0 or weekday == 2:
            disvalue = (options['adults']+ options['childs'] + options['seniors']) * 100
            sales_amount = sales_amount - disvalue

            charge_details_data["曜日割引"] = [f"-{options['adults']+ options['childs'] + options['seniors']}×100円",f"-{disvalue}"]

        print(weekday)
        print(f"販売合計金額:{sales_amount}円")
        print(f"金額変更前合計金額:{total_base}円")
        print("料金明細")
        print("**********************")
        print(f"販売日付:{now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(charge_details_data)
    
    def add_arguments(self, parser):
        parser.add_argument('adults', type=int)
        parser.add_argument('childs', type=int)
        parser.add_argument('seniors', type=int)
        parser.add_argument('--discount',default = 0,type=int)
        parser.add_argument('--holiday',default = 0, type=int)