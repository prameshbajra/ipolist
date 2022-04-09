import re
import os
import json
import requests
from datetime import date
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sympy import symbols


def get_data_from_source():
    URL = "https://www.sharesansar.com/existing-issues?draw=1&columns[0][data]=DT_Row_Index&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=false&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=company.symbol&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=company.companyname&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=false&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=ratio_value&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=total_units&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=false&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=issue_price&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=opening_date&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=false&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=closing_date&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=false&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=final_date&columns[8][name]=&columns[8][searchable]=true&columns[8][orderable]=false&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=listing_date&columns[9][name]=&columns[9][searchable]=true&columns[9][orderable]=false&columns[9][search][value]=&columns[9][search][regex]=false&columns[10][data]=issue_manager&columns[10][name]=&columns[10][searchable]=false&columns[10][orderable]=false&columns[10][search][value]=&columns[10][search][regex]=false&columns[11][data]=status&columns[11][name]=&columns[11][searchable]=false&columns[11][orderable]=false&columns[11][search][value]=&columns[11][search][regex]=false&columns[12][data]=view&columns[12][name]=&columns[12][searchable]=false&columns[12][orderable]=false&columns[12][search][value]=&columns[12][search][regex]=false&columns[13][data]=right_eligibility_link&columns[13][name]=&columns[13][searchable]=false&columns[13][orderable]=false&columns[13][search][value]=&columns[13][search][regex]=false&start=0&length=20&search[value]=&search[regex]=false&type=1&_=1649482141370"
    headers = {"X-Requested-With": "XMLHttpRequest"}
    page = requests.get(URL, headers=headers)
    data = json.loads(page.text)
    return data


def find_company_details(s):
    result = re.search('>(.*)<', s)
    return result.group(1)


def send_email(details):
    message = Mail(
        from_email='pe.messh@gmail.com',
        to_emails='qesrvhgk@cutradition.com',
        subject=f'IPO Listing: {details.symbol} - {details.company_name}',
        html_content='''
            <strong>
                {details.symbol} - {details.company_name} will be listed on NEPSE today. <br> 
                Make sure to place order at 11 AM today.
                <br><br><br>
                Find more on : <a href='https://www.sharesansar.com/existing-issues'>Existing Issues</a>
            </strong>
        ''')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


def main():
    data = get_data_from_source()
    for row in data['data']:
        company_details = row['company']
        company_symbol = find_company_details(company_details['symbol'])
        company_name = find_company_details(company_details['companyname'])
        status = row['status']
        listing_date = row['listing_date']
        print(status, date.today(), listing_date)
        if (status == 1 and listing_date == str(date.today())):
            print(company_symbol, company_name, listing_date)
            send_email({
                'company_name': company_name,
                'symbol': company_symbol
            })


main()