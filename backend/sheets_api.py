import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint


class get_gspread_data():
    def __init__(self):
        self.results = None
        self.credentials = "client_secret.json"
        self.workbook = "19oxjhPkCo5tW5D_emRr5cO4GCCsAgvESc5VCGXeJ8L8"
        self.sheet = "Sheet1"
    def authenticate(self):
        """ Loads the API key and opens the workbook """
        scope = ['https://spreadsheets.google.com/feeds']
        print("Starting to authenticate the access credentials")
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials, scope)
        gc = gspread.authorize(credentials)

        print("credentials authorized, beginning to open the workbook")
        try:
            sh = gc.open_by_key(self.workbook)
            wks = sh.worksheet(self.sheet)
            print('Succesfully opened the worksheet', self.sheet,'inside the workbook',
                  'https://docs.google.com/spreadsheets/d/'+ self.workbook +'/edit#gid=0')
        except:
            return 'ERROR. Unable to load worksheet'

        ### get_all_values() returns a list of lists in which each list is a single row from the sheet ###
        print("trying to convert the list object to a dictionary")
        wks = wks.get_all_values()

        all_clients_dict = {}
        all_clients_dict["clients"] = []

        # the first row is the headers
        keys = wks[0]

        # following rows contain the client data
        values = wks[1:]

        # convert the list of lists into a dictionary
        # the header values such as name, address, run become keys and the client values become values
        try:
            for list_item in values:
                all_clients_dict["clients"].append(dict(zip(keys, list_item)))
        except:
            return "Conversion failed"

        print("conversion successful")

        self.results = all_clients_dict


