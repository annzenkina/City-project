from __future__ import print_function
import httplib2
import os
import datetime
import my_utils

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import matplotlib.pyplot as plt
import pandas as pd
import googlemaps
import geo

def pie_chart(labels, sizes):
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

def insert_city(spreadsheet_id, lng, lat):
    range_name = 'Cities!A:E'
    credentials = my_utils.get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    gmaps = googlemaps.Client(key='AIzaSyDGJ2fytmLrTp3L4wTTp2zn_4L8iQVZvyQ')
    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((float(lat), float(lng)))
    city, country = geo.extract_city(reverse_geocode_result)
    #components = city[0]["address_components"]
    # find component with types == "locality"
    #'types': ['locality', 'political']
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    #import pdb; pdb.set_trace()
    if city not in values[-1]:
        values = [
            [
                float(lat), float(lng), str(datetime.date.today()), city, country
            ],
        ]
        body = {
          'values': values
        }
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name, valueInputOption='USER_ENTERED',body=body).execute()
        return True
    return False

# def main():
#     credentials = my_utils.get_credentials()
#     http = credentials.authorize(httplib2.Http())
#     discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
#                     'version=v4')
#     service = discovery.build('sheets', 'v4', http=http,
#                               discoveryServiceUrl=discoveryUrl)
#
#     spreadsheetId = '1eqS-m4EPRM4U8Py269jwqUWZGQrKHFkfirATVwD9wAQ'
#     rangeName = 'Cities!A:C'
#     result = service.spreadsheets().values().get(
#         spreadsheetId=spreadsheetId, range=rangeName).execute()
#     values = result.get('values', [])
#
#
#
#     # First row = column, the rest is data
#     city_table = pd.DataFrame(data=values[1::], columns=values[0])
#     # We drop 'Date' to be able to group
#     city_table = city_table.drop('Date', axis=1)
#     # Converting 'Count days' to integer
#     city_table['Count days'] = city_table['Count days'].apply(pd.to_numeric)
#     # Reduce duplicates in 'City'
#     city_table = city_table.groupby('City').sum()
#
#     pie_chart(city_table.axes[0], city_table.get('Count days').values)
#
# if __name__ == '__main__':
#     main()
