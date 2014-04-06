import logging
import lob
from secrets import lob_secret
lob.api_key = lob_secret


def sendpicture(name,address,city,state,zipcode,country, tweet):
    #Last two are category of tweet and the actual tweet
##    name = str(raw_input("What is your name? "))
##    address = str(raw_input("What is your address? "))
##    city = str(raw_input("What is your city? "))
##    state = str(raw_input("What is your state? "))
##    zipcode = str(raw_input("What is your zip? "))
##    country = "US"
    verified_address = lob.AddressVerify.verify(name=name, address_line1=address,
                                 address_city=city, address_state=state, address_country=country,
                                 address_zip=zipcode)

    created_address = lob.Address.create(name=name, address_line1=verified_address.address.address_line1,	
    address_city=verified_address.address.address_city, address_state=verified_address.address.address_state, address_country=verified_address.address.address_country,
                                 address_zip=verified_address.address.address_zip)

    #go through all files in folder and create postcard of each file
    Newmessage = "Tweet: {0}".format(tweet)

    lob.Postcard.create(name=name,to=created_address.id,message=Newmessage,front=open(r"postcard.pdf",'rb'),from_address=created_address.id).to_dict 
    #print("Uploaded file")

    #if  os.path.exists(r'C:\Python27\pictures'): shutil.rmtree('C:\Python27\pictures')
    #print("Your post cards have been created and will be processed in 2-3 days! :)")
    #raw_input()

