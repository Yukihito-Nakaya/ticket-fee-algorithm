from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
import pytz

class Command(BaseCommand):
    help = '料金計算用'

    def handle(self, *args, **options):
        tokyo_timezone = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tokyo_timezone)
        weekday = now.weekday()
        print(f"実行日付:{now.strftime('%Y-%m-%d %H:%M:%S')}", f"曜日:{weekday}")
        print(options['child'],options['adult'],  options['senior'])
    
    def add_arguments(self, parser):
        parser.add_argument('adult', type=int)
        parser.add_argument('child', type=int)
        parser.add_argument('senior', type=int)

