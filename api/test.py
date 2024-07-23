# import requests
# from urllib.parse import urlencode

# # Initialize variables
# client = "nextx"  # Replace with actual client name
# StartTime = "2024-07-18 15:02:13"  # Example start time
# UniqueID = "1721289733.161546"
# Duration = 60  # Example duration
# Billsec = 50  # Example bill seconds
# Disposition = "HANGUP"  # Example disposition
# Mayle = "1013"  # Example extension
# SDT = "0123456789"  # Example phone number
# path = ""  # Example recording file path
# call_type = "out"  # Example call type

# # URL encode the StartTime
# Calldate = urlencode({"calldate": StartTime})[9:]  # Removing 'calldate='

# # Construct the URL
# url = (
#     f"https://call.nextcrm.vn/api/crm/ezcall/sync-call?callid={UniqueID}&calldate={Calldate}"
#     f"&duration={Duration}&billsec={Billsec}&status={Disposition}&extension={Mayle}"
#     f"&phone={SDT}&recordingfile={path}&calltype={call_type}"
# )

# print(f"Client: {client}")
# print(url)

# # Basic authentication
# username = client
# password = "1a2s3dA!@#"

# # Execute the request
# response = requests.get(url, auth=(username, password), timeout=(3, 20))

# # Output the response
# print(response.text)

import requests
from urllib.parse import urlencode

def rq_cdr(unique_id, start_time, duration, disposition, billsec, mayle, sdt, path, call_type, client):
    status = -1
    calldate = urlencode({'calldate': start_time})[9:]  # Mã hóa start_time để sử dụng trong URL
    url = (
        f"https://call.nextcrm.vn/api/crm/ezcall/sync-call"
        f"?callid={unique_id}&calldate={calldate}&duration={duration}"
        f"&billsec={billsec}&status={disposition}&extension={mayle}"
        f"&phone={sdt}&recordingfile={path}&calltype={call_type}"
    )
    
    print(f"Client: {client}")
    print(url)
    
    username = client
    password = "1a2s3dA!@#"
    
    try:
        response = requests.get(url, auth=(username, password), timeout=(3, 20))
        response.raise_for_status()  # Kiểm tra nếu có lỗi HTTP
        
        response_data = response.json()
        
        # Print the response for inspection
        print(f"API Response: {response.text}")
        
        if "status code" in response_data:
            status = response_data["status code"]
    
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    
    # Ghi log thông tin chi tiết cuộc gọi

    
    return status

# Ví dụ cách gọi hàm
status = rq_cdr('1721358702.163849', '2024-07-19 10:11:42', 300, 'NO ANSWER', 250, '1001', '0379061925', 'https://nextxcall.nextcrm.vn:8443/monitor/2024/07/19/out-0379061925-1001-20240719-101142-1721358702.163849.wav', 'out', 'nextx')
print(f"Status: {status}")