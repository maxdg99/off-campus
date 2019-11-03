from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers


from apartmentSearchApp.models import Listing

def compute_averages():
    d = {}
    averages = {}
    for x in Listing.listings.all():
        if x.num_bathrooms is None or x.num_bedrooms is None or x.price is None:
            continue
        key = (x.num_bedrooms, x.num_bathrooms)
        if key in d:
            d[key].append(x)
        else:
            d[key] = [x]

    
    for key, listings in d.items():
        sum = 0
        p = []
        for l in listings:
            p.append(l.price)
            sum += l.price
        avg = sum / len(listings)
        averages[key] = avg
        print(str(key)+": "+str(avg)+" - "+str(p))
    return averages