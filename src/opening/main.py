import os
import re
import json
import traceback
import boto3
import requests
from datetime import date

SES_CLIENT = boto3.client('ses')
EMAILS_TO_SEND = os.environ.get('emails_to_send', '')


def get_data_from_source():
    URL = "https://www.sharesansar.com/existing-issues?draw=1&columns[0][data]=DT_Row_Index&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=false&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=company.symbol&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=company.companyname&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=false&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=ratio_value&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=total_units&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=false&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=issue_price&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=opening_date&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=false&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=closing_date&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=false&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=final_date&columns[8][name]=&columns[8][searchable]=true&columns[8][orderable]=false&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=listing_date&columns[9][name]=&columns[9][searchable]=true&columns[9][orderable]=false&columns[9][search][value]=&columns[9][search][regex]=false&columns[10][data]=issue_manager&columns[10][name]=&columns[10][searchable]=false&columns[10][orderable]=false&columns[10][search][value]=&columns[10][search][regex]=false&columns[11][data]=status&columns[11][name]=&columns[11][searchable]=false&columns[11][orderable]=false&columns[11][search][value]=&columns[11][search][regex]=false&columns[12][data]=view&columns[12][name]=&columns[12][searchable]=false&columns[12][orderable]=false&columns[12][search][value]=&columns[12][search][regex]=false&columns[13][data]=right_eligibility_link&columns[13][name]=&columns[13][searchable]=false&columns[13][orderable]=false&columns[13][search][value]=&columns[13][search][regex]=false&start=0&length=20&search[value]=&search[regex]=false&type=1&_=1649482141370"
    headers = {"X-Requested-With": "XMLHttpRequest"}
    page = requests.get(URL, headers=headers)
    data = json.loads(page.text)
    return data


def find_company_details(s):
    result = re.search('>(.*)<', s)
    return result.group(1)


def send_email(symbol, company_name):
    try:
        emails = EMAILS_TO_SEND.split(",")
        print("SENDING EMAILS TO => ", emails)
        if len(emails) == 0:
            return False
        response = SES_CLIENT.send_email(
            Destination={'ToAddresses': emails},
            Message={
                'Body': {
                    'Html': {
                        'Charset':
                        'UTF-8',
                        'Data':
                        f'''
                        <html>
                            <strong>
                                Symbol: {symbol} <br>
                                Company Name: {company_name} <br>
                                will available for IPO today. <br> <br> 
                                You can apply for it from your Mero Share account.
                                <br><br><br>
                                Find more on : <a href='https://www.sharesansar.com/existing-issues'>IPO Details</a>
                            </strong>
                        </html>
                        ''',
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': f'IPO Opens Today: {symbol} - {company_name}',
                },
            },
            Source='bajracharyapramesh99@gmail.com',
        )
        print(response)
    except Exception as e:
        traceback.format_exc()


def lambda_handler(event, context):
    data = get_data_from_source()
    for row in data['data']:
        company_details = row['company']
        company_symbol = find_company_details(company_details['symbol'])
        company_name = find_company_details(company_details['companyname'])
        status = row['status']
        opening_date = row['opening_date']
        print(company_name, company_symbol, opening_date, status)
        if (status == 0 and opening_date == str(date.today())):
            print("IPO OPEN : ", company_name, company_symbol, opening_date,
                  status)
            send_email(symbol=company_symbol, company_name=company_name)