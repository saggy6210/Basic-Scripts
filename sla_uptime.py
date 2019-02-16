import requests
import datetime
import json
import yaml
import math


health_ESURL  = "Your ES URL/index_name/health/_search" 
Header       = {"Content-Type": "application/json"}
timelength   = [1,3,7,30]
hitfrequency = 12 # 6 for every 10 min 12 for every 5 min
sla_data     = {}
product_line_sla = {}

app_list_yml = "main.yaml"
data = yaml.load(open(app_list_yml))

for inc in data.get("includes", []):
	try:
		data.update(yaml.load(open(inc)))
	except Exception as e:
		print (e)

for account_name_prefix,appdata in data.items():
	if account_name_prefix == "common" or account_name_prefix == "includes":
		pass
	else :
		print ("Service Name: ", account_name_prefix) #Product line name
		applist = appdata.get('applications')
		for servicename in applist.keys(): #Services 
			sla = {}
			for ctime in timelength:
				now  = datetime.datetime.now()   #for utc time utcnow()
				past = now + datetime.timedelta(days=-ctime)
				payload = {
				  "query": {
				    "bool": {
				      "must": [
				        {
				          "match": {
				            servicename + ".healthy_instance": "0"
				          }
				        }
				      ],
				      "filter": [
				        {
				          "range": {
				            "timestamp": {
				              "gte": past.isoformat(),
				              "lte": now.isoformat()
				            }
				          }
				        }
				      ]
				    }
				  }
				}
				totaltime     = ctime * hitfrequency * 24
				raw_data      = requests.get(url=health_ESURL,headers=Header, data=json.dumps(payload))
				downtime_data = json.loads(raw_data.content.decode("utf-8"))
				downtime      = downtime_data.get("hits").get("total")
				slapercentage = (downtime / totaltime) * 100
				sla['l-'+str(ctime)] = round(100 - slapercentage,2)
				
			sla_data[servicename] = {
			                      "l-1" : sla['l-1'],
			                      "l-3" : sla['l-3'],
			                      "l-7" : sla['l-7'],
			                      "l-30": sla['l-30'],
			                      "product_line": account_name_prefix
			                    }
			print( "Date range from {} to {} account_name_prefix {} svc {} SLA {} {}".format(past.isoformat(),now.isoformat(),account_name_prefix,servicename,sla,ctime))
		avg_sla_1 = avg_sla_3 = avg_sla_7 = avg_sla_30 = count = 0
		
		for name,servicesla in sla_data.items():
			if servicesla['product_line'] == account_name_prefix :
				for key, sla in  servicesla.items():
					if key == "product_line":
						pass
					elif key.endswith("l-1"):
						avg_sla_1 = avg_sla_1 + sla
						count += 1
					elif key.endswith("l-3"):
						avg_sla_3 = avg_sla_3 + sla
					elif key.endswith("l-7"):
						avg_sla_7 = avg_sla_7 + sla
					elif key.endswith("l-30"):
						avg_sla_30 = avg_sla_30 + sla
		print (count)
		product_line_sla[account_name_prefix + '_sla_1']  = round((avg_sla_1 / count), 2)
		product_line_sla[account_name_prefix + '_sla_3']  = round((avg_sla_3 / count), 2)
		product_line_sla[account_name_prefix + '_sla_7']  = round((avg_sla_7 / count), 2)
		product_line_sla[account_name_prefix + '_sla_30'] = round((avg_sla_30 / count), 2)
		print (product_line_sla)

mind_sla_1 = mind_sla_3 = mind_sla_7 = mind_sla_30 = count = 0
for name,sla in product_line_sla.items():
	sla_data[name] = round(sla,2)
	if name.endswith("sla_1"):
		mind_sla_1 = mind_sla_1 + sla
		count += 1
	elif name.endswith("sla_3"):
		mind_sla_3 = mind_sla_3 + sla
	elif name.endswith("sla_7"):
		mind_sla_7 = mind_sla_7 + sla
	elif name.endswith("sla_30"):
		mind_sla_30 = mind_sla_30 + sla

sla_data["Project_tile"] = {
                          "l-1" : math.floor((mind_sla_1 / count)*100)/100.0,
                          "l-3" : math.floor((mind_sla_3 / count)*100)/100.0,
                          "l-7" : math.floor((mind_sla_7 / count)*100)/100.0,	
                          "l-30": math.floor((mind_sla_30 / count)*100)/100.0,			
                          "product_line": "master",			
                         }			

ES = "Your ES URL/sla index name/doc_type"
sla_data['timestamp'] = now.isoformat()
stat  = "/" + now.strftime("%Y%m%d%H%M%S")
ESURL = ES + stat
                        
try:
    state = requests.post(url     = ESURL,
                          data    = json.dumps(sla_data),
                          headers = {"Content-Type": "application/json" },
                          timeout = 10
                          )

    print ('[ES_INFO] POST STATUS:', state.status_code, state.content)
except:
    print('[ES_ERROR] Post Error')

print (ESURL)
