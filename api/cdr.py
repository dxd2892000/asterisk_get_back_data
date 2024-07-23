import pymysql
import requests

from datetime import datetime

from collections import OrderedDict

from urllib.parse import urlencode, quote

class Cdr:
    # Contructor
    def __init__(self, host, user, password, dbname, name, url):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.name = name
        self.url = url

    def connect_to_database(self):
        #print(self.host)
        connection = pymysql.connect(
            host=self.host, 
            db=self.dbname,
            user=self.user,
            password=self.password
    )
        return connection

    def get_client(self, extension):
        first_char = extension[0]
        conn = self.connect_to_database()

        try:
            with conn.cursor() as cursor:
                first_char = conn.escape(first_char)
                query = f"SELECT client FROM client WHERE extension = {first_char}"
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    client = result[0]
                else:
                    client = 'non-exiting'
        finally:
            conn.close()

        return client
    
    def rq_cdr(self, unique_id, start_time, duration, disposition, billsec, mayle, sdt, path, call_type, client):
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
        
        
        # Print the response for inspection
            print(f"API Response: {response.text}")
        
    
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")

    def process_call(self, start, end):
        count = 0
        conn = self.connect_to_database()
        
        try:
            with conn.cursor() as cursor:
                sql = f"SELECT * FROM cdr WHERE calldate BETWEEN '{start}' AND '{end}'"
                cursor.execute(sql)
                # name of field from data gotten from database
                columns = [col[0] for col in cursor.description]
                results = []
                # print(f"Number of rows: {len(result)}")
                for row in cursor.fetchall(): # data with type tupple
                    row_dict = OrderedDict(zip(columns, row)) # convert from tuple to dictionary 
                    results.append(row_dict)

                for result in results:
                    unique_id = result['uniqueid']
                    start_time = result['calldate']
                    duration = result['duration']
                    disposition = result['disposition']
                    billsec = result['billsec']
                    mayle = result['cnum']
                    sdt = result['dst']
                    path = result['recordingfile']
                    last_app = result['lastapp']
                    dcontext = result['dcontext']

                    if last_app == 'Dial':
                        # call out
                        if dcontext == 'from-internal':
                            calltype = 'out'
                            client = self.get_client(mayle)
                            if client == self.name:
                                if disposition == 'NO ANSWER':
                                    disposition = 'NOANSWER'
                                #date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                                nam = start_time.strftime("%Y")
                                thang = start_time.strftime("%m")
                                ngay = start_time.strftime("%d")

                                path_full = f"https://{self.url}:8443/monitor/{nam}/{thang}/{ngay}/{path}"
                                path_encode = quote(path_full)
                                print(f"{unique_id}, {start_time}, {duration}, {disposition}, {billsec}, {mayle}, {sdt}, {path_encode}, {calltype}, {client}")
                                self.rq_cdr(unique_id, start_time, duration, disposition, billsec, mayle, sdt, path_encode, calltype, client)
                                count = count + 1
                        #call in group
                        if dcontext == 'ext-group':
                            calltype = 'in'
                            client = self.get_client(mayle)
                            if client == self.name:
                                if disposition == 'NO ANSWER':
                                    disposition = 'NOANSWER'
                                date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                                nam = date.strftime("%Y")
                                thang = date.strftime("%m")
                                ngay = date.strftime("%d")

                                path_full = f"https://{self.url}:8443/monitor/{nam}/{thang}/{ngay}/{path}"
                                path_encode = quote(path_full)
                                print(f"{unique_id}, {start_time}, {duration}, {disposition}, {billsec}, {mayle}, {sdt}, {path_encode}, {calltype}, {client}")
                                self.rq_cdr(unique_id, start_time, duration, disposition, billsec, mayle, sdt, path_encode, calltype, client)
                                count = count + 1
                                
                        #call in extension when group don't pick up        
                        if dcontext == 'ext-local':
                            calltype = 'in'
                            client = self.get_client(mayle)
                            if client == self.name:
                                if disposition == 'NO ANSWER':
                                    disposition = 'NOANSWER'
                                date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                                nam = date.strftime("%Y")
                                thang = date.strftime("%m")
                                ngay = date.strftime("%d")

                                path_full = f"https://{self.url}:8443/monitor/{nam}/{thang}/{ngay}/{path}"
                                path_encode = quote(path_full)
                                print(f"{unique_id}, {start_time}, {duration}, {disposition}, {billsec}, {mayle}, {sdt}, {path_encode}, {calltype}, {client}")
                                self.rq_cdr(unique_id, start_time, duration, disposition, billsec, mayle, sdt, path_encode, calltype, client)
                                count = count + 1
                                
                        if dcontext == 'followme-check':
                            calltype = 'in'
                            client = self.get_client(mayle)
                            if client == self.name:
                                if disposition == 'NO ANSWER':
                                    disposition = 'NOANSWER'
                                date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                                nam = date.strftime("%Y")
                                thang = date.strftime("%m")
                                ngay = date.strftime("%d")

                                path_full = f"https://{self.url}:8443/monitor/{nam}/{thang}/{ngay}/{path}"
                                path_encode = quote(path_full)
                                print(f"{unique_id}, {start_time}, {duration}, {disposition}, {billsec}, {mayle}, {sdt}, {path_encode}, {calltype}, {client}")
                                self.rq_cdr(unique_id, start_time, duration, disposition, billsec, mayle, sdt, path_encode, calltype, client)
                                count = count + 1
                                
        finally:
            conn.close()
            
        return count