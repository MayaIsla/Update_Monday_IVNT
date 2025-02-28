

import requests
import pandas as pd
import json


monday_api__Key = ""
api__URI = "https://api.monday.com/"
monday_headers = {"Authorization" : monday_api__Key,  "API-Version" : "2023-04"}
search_Query_Board_Items = 'query FindSubitem {boards(ids: 000000) {items_page(query_params: {rules: [{column_id: "name", compare_value: ["incident #"], operator: contains_text}]}) {items {id name}}}}'
data_board_item = {'query': search_Query_Board_Items}
Query_boardItems = requests.post(url=api__URI, json=data_board_item, headers=monday_headers)
json_data_boarditems = json.loads(Query_boardItems.text)
parsed_JSON__boardItem = pd.json_normalize(json_data_boarditems['data']['boards'][0]['items_page']['items'])
parsed_JSON__boardItem['INC #'] = (parsed_JSON__boardItem['name'].str.split('Incident #').str[1])
parsed_JSON__boardItem['SubID'] = parsed_JSON__boardItem['id']


for INC_number_iterator, SubItem_ID in zip(parsed_JSON__boardItem['INC #'], parsed_JSON__boardItem['SubID']):

    search_ivanti_url = "https://endpoint.saasit.com/api/odata/businessobject/incidents?$filter=IncidentNumber eq" + " " + INC_number_iterator
    iv_auth_header = {'Authorization': ''}
    request_iv_get_recID = requests.get(url=search_ivanti_url, headers=iv_auth_header)
    request_iv_get_recID_text = request_iv_get_recID.text

    json_RecID = json.loads(request_iv_get_recID_text)

    for i in json_RecID['value']:
        status_IVNT = (i['Status'])
        update_status_monday = 'mutation {change_simple_column_value(item_id: ' + SubItem_ID + ', board_id: 000000, column_id: "status_column_name", value: "' + status_IVNT + '") {id}}'
        mutation_status_monday = {'query': update_status_monday }
        update_query_request = requests.post(url=api__URI, json=mutation_status_monday, headers=monday_headers)
        print(update_query_request.text)









