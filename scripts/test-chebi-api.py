from pysimplesoap.client import SoapClient

client = SoapClient(wsdl="https://www.ebi.ac.uk/webservices/chebi/2.0/webservice?wsdl",trace=False)
response = client.getLiteEntity(search='*',maximumResults=10)
print(response)
