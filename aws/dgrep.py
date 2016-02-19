import boto3

r53 = boto3.client('route53')

zones = ['itp.netflix.com', 'itp.netflix.net', 'itd.netflix.com', 'itd.netflix.net']
zoneids = ['Z3TNCN3W3O24M9', 'Z13MPXCU0UPD0Q']

zoneid = 'Z3TNCN3W3O24M9'


response = r53.list_resource_record_sets(
    HostedZoneId = zoneid
)

for resource-record in resoponse['ResourceRecordSets']:
    print resource-record

