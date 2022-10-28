from data_manager import DataManager

ORIGIN_AIRPORT = "MAD"
sheet_data = DataManager()
for destination in sheet_data.get_city():
    if destination["iataCode"] == "":
        destination["iataCode"] = sheet_data.get_iata_code(destination["city"])
        sheet_data.update_data(destination["iataCode"], destination["id"])
    sheet_data.cheap_flight(ORIGIN_AIRPORT, destination["iataCode"], destination["city"], destination["lowestPrice"])
    sheet_data.send_sms()
