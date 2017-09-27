def extract_city(google_geocode):
    components = google_geocode[0]['address_components']
    for comp in components:
        #if comp['types'] == ['locality', 'political']:
        if 'locality' in comp['types']:
            city = comp['long_name']
        #if comp['types'] == ['country', 'political']:
        if 'country' in comp['types']:
            country = comp['long_name']
    return city, country
