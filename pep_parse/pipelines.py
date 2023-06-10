import csv
from collections import defaultdict
from datetime import datetime

from pep_parse.settings import BASE_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_count = defaultdict(int)

    def process_item(self, item, spider):
        self.status_count[item['status']] += 1
        return item

    def close_spider(self, spider):
        time = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        path = BASE_DIR / 'results' / f'status_summary_{time}.csv'

        with open(path, mode='w', encoding='utf-8') as csvfile:
            writer = csv.writer(
                csvfile, dialect='unix', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerows([
                ['Статус', 'Количество'],
                *(self.status_count.items()),
                ['Total', sum(self.status_count.values())]
            ])
