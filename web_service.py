from bottle import route, request, response, run, error
import petl 
import json

file = 'clinic_service_locations.csv'

# this link will give the list of services
@route('/getservices')
def anyServices():
    # requested query
    Postcode = request.query.Postcode
    #Converting the Service value to String
    Postcode = str(Postcode)
    # reading the csv file
    csv = petl.fromcsv(file)

    # json content type declaration
    response.headers['Content-type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    for i in csv:
        if Postcode == i[4]:
            # select the data according to the given requested query
            dataSelect = petl.select(csv, "{Postcode} == '" + Postcode + "'")   
            # cutting out the required column names
            jsonData = petl.cut(dataSelect,'Service','Suburb')
            # convert the dictionary data into json data
            jsonData = json.JSONEncoder().encode(list(petl.dicts(jsonData)))
            # return the json data
            return jsonData

    else:
        jsonData = json.JSONEncoder().encode('Unable to find this Service.')
        return jsonData
    


# this link will provide the clinics names who provide the particular services
@route('/getclinics')
def main_loop():
    # requested query
    Service = request.query.Service
    #Converting the Service value to String
    Service = str(Service)
    
    csv = petl.fromcsv(file)
    response.headers['Content-type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'

    for i in csv:
        if Service == i[1]:
            # select the data according to the given requested query
            dataSelect = petl.select(csv, "{Service} == '" + Service + "'")   
            # cutting out the required column names
            jsonData = petl.cut(dataSelect, 'ClinicID', 'Suburb', 'Lat', 'Lon')
            # convert the dictionary data into json data
            jsonData = json.JSONEncoder().encode(list(petl.dicts(jsonData)))
            # return the json data
            return jsonData

        # this is requested link of getting all the distinct list of clinics offering any service.
        if Service == "0":
            anyServices = petl.unique(csv, key='Name')
            jsonData = petl.cut(anyServices, 'ClinicID', 'Suburb', 'Lat', 'Lon')
            jsonData = json.JSONEncoder().encode(list(petl.dicts(jsonData)))
            return jsonData
    else:
        jsonData = json.JSONEncoder().encode('Please Enter a Service.')
        return jsonData


# error handling or exception handling
@error(404)
def linkerror(error):
    return "<h1>Please fill proper link!!"


run(host='localhost', port='8080', debug=True)

main_loop()