"""
File: webcrawler.py
Name: Bella
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10900879
Female Number: 7946050
---------------------------
2000s
Male Number: 12977993
Female Number: 9209211
---------------------------
1990s
Male Number: 14146310
Female Number: 10644506
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)
        url = 'https://www.ssa.gov/oact/babynames/decades/names'+year+'.html'
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html)

        numbers = [0, 0]
        # A tr contain the data of one rank.
        for tr in soup.find('tbody').select('tr'):
            tds = tr.select('td')
            # Exclude the last tr.
            if len(tds) > 2:
                # Count male number
                numbers[0] += int(tds[2].text.replace(',', ''))
                # Count female number
                numbers[1] += int(tds[4].text.replace(',', ''))
        print(f'Male Number: {numbers[0]}')
        print(f'Female Number: {numbers[1]}')


if __name__ == '__main__':
    main()
