import petl as pt

def DataIntegration(clinics_LOC,Services_LOC,Location_LOC):
    # Reading the clinics.csv file
    fileData = pt.fromcsv(clinics_LOC)

    # Reading the clinic_services.csv file
    servicesData = pt.fromcsv(Services_LOC)

    # reading the xml file cliniclocations.xml
    locationXML = pt.fromxml(Location_LOC, 'clinic', {"ClinicID": "ClinicID", "Lat": "Lat", "Lon": "Lon"})

    # join the csv file's using the inbuilt function join using ClinicID as main key
    fileJoin = pt.join(servicesData, fileData, key="ClinicID")

    # join the csv file using the inbuilt function join using ClinicID as main key
    MainJoin = pt.join(fileJoin, locationXML, key="ClinicID")

    # acquire the required columns
    result = pt.cut(MainJoin, 'ClinicServiceID', 'Service', 'ClinicID', 'Suburb', 'Postcode', 'Lat', 'Lon')

    # creating the final csv file which is clinicservicelocations.csv
    pt.tocsv(result, "clinic_service_locations.csv")
    print('Csv file generated.!!!')  

if __name__ == "__main__":
    # Files Location
    clinics_LOC = 'clinics.csv'
    Services_LOC = 'clinic_services.csv'
    Location_LOC = 'cliniclocations.xml'

    #Passing the Location Parameters to DataIntegration Funtion for Processing
    DataIntegration(clinics_LOC,Services_LOC,Location_LOC)
