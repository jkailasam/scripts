import boto3

iam = boto3.resource('iam')
iamc = boto3.client('iam')

string = 'LastUsedDate'

users = iam.users.all()
# Metadata = iamc.list_access_keys(UserName=user.user_name)

for user in users:
    for key in user.access_keys.all():
        username = user.user_name
        fusername = username.ljust(35)
        accessid = key.id
        status = key.status
        lastused = iamc.get_access_key_last_used(AccessKeyId=accessid)
        if status == "Active":
            if string in lastused['AccessKeyLastUsed']:
                date = lastused['AccessKeyLastUsed'][string].strftime('%Y-%m-%d %H:%M UTC')
                print "User: {0}  Key: {1}     Last_Used: {2}".format(fusername,accessid,date)
            else:
                print "User: {0}  Key: {1}     Key_Active_but_Never_Used".format(fusername,accessid)





