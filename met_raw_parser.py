import csv
import requests
import json


IMG_BASE_URL = "https://www.metmuseum.org/api/Collection/additionalImages?crdId={id}&page=1&perPage=1"

def handle_row(content_list):
    data = {
        "id": row[3],
        "dept": row[4],
        "title": row[6],
        "artist_name": row[14],
        "artist_bio": row[15],
        "link": row[40]
    }

    r = requests.get(IMG_BASE_URL.format(id=data["id"]))
    image_object = json.loads(r.text)
    if image_object["results"] and len(image_object["results"]) > 0:
        data["image"] = image_object["results"][0]["webImageUrl"]
        return data
    else:
        return None

with open('met_objects_raw_american.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # Skip first line
    first_row = next(reader)
    collection = []
    for row in reader:
        data = handle_row(row)
        if data:
            print "done"
            collection.append(data)
        else:
            print "skip"

    with open("met_objects_raw_american.json", "w") as fd:
        json.dump(collection, fd);
    print collection[0]
    print len(collection)