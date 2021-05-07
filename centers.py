from datetime import date
import requests
def get_centers(min_age,pincode):
	today = date.today()
	prepare_text=""
	dates = today.strftime("%d-%m-%Y")
	url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"
	PARAMS = {'pincode':pincode,'date':str(dates)}
	r = requests.get(url = url, params = PARAMS)
	req = r.json()
	print(req)
	try:
		if(min_age>=req['sessions'][0]['min_age_limit']):
			prepare_text+="We have found this center based on your preferences.\n"
			prepare_text+="The center id is {} \n".format(req['sessions'][0]['center_id'])
			prepare_text+="Center Name is {}\n".format(req['sessions'][0]['name'])
			prepare_text+="Available capacity: {}\n".format(req['sessions'][0]['available_capacity'])
			prepare_text+="Fees: {} Rs\n".format(req['sessions'][0]['fee'])
			prepare_text+="Address: {}\n".format(req['sessions'][0]['address'])
		else:
			prepare_text="Sorry no current centers found"
		return prepare_text
	except:
		print("No centers found")
