# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    return list(map(lambda x:datetime.strptime(x,'%Y-%m-%d').strftime('%d %b %Y') ,old_dates))


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start,str):
        raise TypeError('date not in str')
    if not isinstance(n,int):
        raise TypeError('n is not in integer')

    return [datetime.strptime(start,'%Y-%m-%d')+timedelta(days=i) for i in range(n)]




def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    date_li= date_range(start_date,len(values))
    return list(zip(date_li,values))

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile,'r') as f:
        file = DictReader(f)
        dic={}
        for i in file:
            day_diff=datetime.strptime(i['date_returned'],'%m/%d/%Y')-datetime.strptime(i['date_due'],'%m/%d/%Y')
            days_diff = day_diff.days
            cost = round(days_diff * 0.25, 2) if days_diff > 0 else 0
            if i['patron_id'] in dic.keys():
                dic[i['patron_id']] += cost
            else:
                dic[i['patron_id']]=cost
    li_fee=[{'patron_id':i,'late_fees':format(j,'.2f')} for i,j in dic.items()]
    with open(outfile , 'w') as csvfile:
        writer = DictWriter(csvfile, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(li_fee)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.
if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
