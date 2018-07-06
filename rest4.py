/* 
*  Trip Planner Program
*
*  The following program takes a list of starting and ending locations,
*  performs a RESTful query from google API to obtain the distance between
* each of the pair of locations, and determines the shortest distance and driving duration.
*
*/



import json
import requests

def consumeGETRequestSync(trip_list1_json):
# this function does the main work for REST get.
# Input is a json string with origin and destination values.
# The output is a json string with the rest of the details.

# convert input json into a list of dictionary key-value pairs.
    trip_list1  = json.loads(trip_list1_json)
# initialize
    result_list = []
    result = {}
# The list may have more than one data points. for each, pick the
#origin, destination, make the url string and mage the REST query
    for trip in trip_list1:
        origin = trip["origin"]
        destination = trip["destination"]
        params = {}
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + origin + "&destinations=" + destination + "&key=AIzaSyAJjZ1Ya4x6hwsEM4OtaqcFk0Iic_YcCcc"
        headers = {"Accept": "application/json"}
        # call get service with headers and params
        response = requests.get(url, headers=headers, data=params)
        # get the response from the REST query
        my_dict = json.loads(response.text)
        #find the return values in the response, store them into a local dictionary/list
        origin1 = my_dict["origin_addresses"][0]
        destination1 = my_dict["destination_addresses"][0]
        distance1_text = my_dict["rows"][0]['elements'][0]['distance']['text']
        distance1_value = my_dict["rows"][0]['elements'][0]['distance']['value']
        duration1_text = my_dict["rows"][0]['elements'][0]['duration']['text']
        duration1_value = my_dict["rows"][0]['elements'][0]['duration']['value']
        status1 = my_dict["status"]
        result["origin"]=origin1
        result["destination"]=destination1
        result["distance_text"]=distance1_text
        result["distance_value"]=distance1_value
        result["duration_text"]=duration1_text
        result["duration_value"]=duration1_value
        result["status"]=status1
        result_list.append(dict(result))
    # convert it to json string and return
    result_list_json = json.dumps(result_list)
    return (result_list_json)


# main program
# set up space for the input data
trip_list = []
trip = {}

# enter the origin and destination for trip #1
# we are storing these in a dictionary, and save the dictionary int a list.
trip["origin"] = "Hartford, CT"
trip["destination"] = "Boston, MA"
trip_list.append(dict(trip))

# enter the origin and destination for trip #2
trip["origin"] = "Los Angeles, CA"
trip["destination"] = "Beverly Hills, CA"
trip_list.append(dict(trip))

trip["origin"] = "Cambridge MA"
trip["destination"] = "Boston, MA"
trip_list.append(dict(trip))

trip["origin"] = "New York NY"
trip["destination"] = "Chicago IL"
trip_list.append(dict(trip))

# we can enter any number of origin/destination pairs
# let us print the data to verify
print(*trip_list, sep='\n')

# Let us make a json file from the list of dictionaries.
trip_list_json = json.dumps(trip_list)

# call the function to do the work.
# input: a json string, output: a json string
result_list_json = consumeGETRequestSync(trip_list_json)

# print the results
print (result_list_json)

#convert json to list of dictionaries
result_list = json.loads(result_list_json)

# find the shortest time interval
maxval = 999999
for result in result_list:
    if (result["status"] == "OK"):   # only take cases for which Google returned valid data
        if (result["duration_value"] < maxval):
            maxval = result["duration_value"]
            origin_short = result["origin"]
            destination_short = result["destination"]
            distance_text_short = result["distance_text"]
            distance_value_short = result["distance_value"]
            duration_text_short = result["duration_text"]
            duration_value_short = result["duration_value"]
            status_short = result["status"]

# print the results
print("\n")
for result in result_list:
    origin = result["origin"]
    destination = result["destination"]
    distance_text = result["distance_text"]
    distance_value = result["distance_value"]
    duration_text = result["duration_text"]
    duration_value = result["duration_value"]
    status = result["status"]
    print ("===========Results==============\n")
    print ("Origin ........................." + origin)
    print ("Destination.................." + destination)
    print ("Status Code ................." + status)
    print ("Driving distance .........." + distance_text)
    print ("Duration ....................." + duration_text)
    print("\n")
print("===========Shortest Duration Results==============\n")
print("Origin ........................." + origin_short)
print("Destination.................." + destination_short)
print("Driving distance .........." + distance_text_short)
print("Duration......... ............" + duration_text_short)


