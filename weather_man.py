import Keys.client_secret_weather as key
import requests

api_url = 'http://api.openweathermap.org/data/2.5/'
main_endpoint = 'weather'
city = 'Toronto'


def main():
	req_url = api_url + main_endpoint
	api_params= {'q': city, 'APPID': key.weather_secret}
	resp = requests.get(req_url, params=api_params)
	if (resp.status_code == 200):
		return resp.json()
	else:
		return {}


if __name__ == '__main__':
	main()


