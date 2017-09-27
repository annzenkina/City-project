# City-project
Repo with my python scripts that makes charts about cities that I visited. I use Google Spread Sheets as a backend.

![image 2017-09-20 10 47 15](https://user-images.githubusercontent.com/29050596/30632522-11ce9760-9df1-11e7-89a5-3091e90248a7.jpg)

When you click on an extension button in Chrome, browser gets geolocation and sends them by HTTP to server.py. The server makes a request to Google Maps Geocoder to get address from these coordinates. When geocoding is complete the server saves data about your location to Google Spreadsheets: Longitude, Latitude, Date, City, and Country.

# Components

## Chrome extension
I used [developers guide](https://developer.chrome.com/extensions/getstarted) to get started with Chrome Extension. This script is only 25 lines of code, it gets geolocation and sends it to local server.

## Local Server
Why do you need a local server and why can't you just send coordinates directly to Google SpreadSheets from the browser?
First of all you need to authorize in Google Apps, and you can't do it directly from Chrome Extension.
The second is that you also need to geocode the coordinates and doing it from extension would be tricky.
So I decided to build a local server in Python and keep it running on my Macbook all the time.

The server does all the work. It gets coordinates from HTTP request and sends a request to Google Maps Geocoder. It extracts City and Country from the geocoding result.
To avoid duplicates in the sheet, the server gets the last row from the spreadsheet and compares it with the current data. If the last row isn't equal, the server inserts a new row with Longitude, Latitude, Date, City, Country. If the data has been saved correctly it responds with HTTP 200 OK and  "Saved!" as response body. 
