from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers


from OffCampusRestApi.models import Listing

def compute_averages():
    d = {}
    averages = {}
    for x in Listing.listings.all():
        if x.baths is None or x.beds is None or x.price is None:
            continue
        key = (x.beds, x.baths)
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
        #print(str(key)+": "+str(avg)+" - "+str(p))
    return averages