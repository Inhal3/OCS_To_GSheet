from get_goods import get_items
from gsheet_upload_client import sheet_upload
import datetime

if __name__ == '__main__':
    print(datetime.datetime.now())
    get_items()
    sheet_upload()
