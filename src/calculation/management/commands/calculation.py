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
        return {self.rates.get(0),self.rates.get(discount,'discountコードが間違っています。')}

#料金計算アルゴリズム
class Command(BaseCommand):
    help = '料金計算用'

    def handle(self, *args, **options):
        tokyo_timezone = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tokyo_timezone)
        weekday = now.weekday()
        
        rate_table = RateTable()
        rate = rate_table.get_base_rate()

        #total_base
        total_base = (options['adults'] * rate.get('adult'))
        + (options['childs'] * rate.get('child'))
        + (options['seniors'] * rate.get('senior'))

        sales_amount = total_base
        
        #特別タイプの場合
        if options['discount'] > 0:
            rate = rate_table.get_discount_rate(options['discount'])
            sales_amount = (options['adults'] * rate.get('adult'))
            + (options['childs'] * rate.get('child'))
            + (options['seniors'] * rate.get('senior'))

        #団体割引確認
        if (options['adults']+ (options['childs'] * 0.5) + options['seniors']) >= 10:
            sales_amount = sales_amount * 0.9

        #時間割引確認
        if now.hour >= 17:
            sales_amount = - (options['adults']+ options['childs'] + options['seniors']) * 100

        #休日確認
        if weekday == 5 or weekday == 6 or options['holiday']:
            sales_amount = sales_amount * 0.8

        #曜日割引確認
        if weekday == 0 or weekday == 2:
            sales_amount = sales_amount - (options['adults']+ options['childs'] + options['seniors']) * 100

        
        print(f"販売合計金額:{sales_amount}円")
        print(f"金額変更前合計金額:{total_base}円")
        print(f"販売日付:{now.strftime('%Y-%m-%d %H:%M:%S')}", f"曜日:{weekday}")
    
    def add_arguments(self, parser):
        parser.add_argument('adults', type=int)
        parser.add_argument('childs', type=int)
        parser.add_argument('seniors', type=int)
        parser.add_argument('--discount',default = 0,type=int)
        parser.add_argument('--holiday',default = False, type=bool)