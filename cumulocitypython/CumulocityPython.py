import logging

#import libs for data fetching
from http.client import HTTPSConnection
from base64 import b64encode
import json
import sys

#import data processing libs
import pandas as pd
import collections

#time management libraries
import time
from dateutil import parser, tz
from datetime import datetime, timedelta

class CumulocityPython:
        def __init__(self, base_url, username, password):
            credentials = b64encode(bytes(username + ':' + password, "utf-8")).decode("ascii")
            self.headers = { 'Authorization' : 'Basic %s' %  credentials }
            self.base_url = base_url
            logging.basicConfig(level=logging.INFO)
        
        #returns the current offset (takes into account daylight savings)
        def __get_current_utc_offset(self):
            ts = time.time()
            return (datetime.fromtimestamp(ts) - datetime.utcfromtimestamp(ts)).total_seconds()
            
        #formats any viable date to ISO 8601, if tz is not included then uses local tz
        def __format_date(self, date_string, is_parsed=False):
            #error handling
            if(date_string is None):
                return None
            
            #parses the date if needed
            parsed_datetime = date_string if is_parsed else parser.parse(date_string)
            
            #if timezone is present, uses that info, otherwise uses local timezone
            if(parsed_datetime.tzinfo is not None):
                return parsed_datetime.isoformat().replace("+", "%2B")
            else:
                local_tz = tz.tzoffset(None, self.__get_current_utc_offset())
                return parsed_datetime.replace(tzinfo=local_tz).isoformat().replace("+", "%2B")
        
        def __datetime_range(self, start, end, delta=None):
            # if no delta object, return the normal date ranges
            if(delta == None):
                return [{"dateFrom":self.__format_date(start), "dateTo":self.__format_date(end)}]
            
            # if delta paramenter is given and start or end is missing, raise error
            if(delta and (not start or not end)):
                raise Exception("If using timedelta, both date_from and date_to must be specified")
            
            start = parser.parse(start)
            end = parser.parse(end)
            # slice the start and end interval to an array based on delta
            ranges = []
            current = start
            while current < end:
                from_date = self.__format_date(current, is_parsed=True)
                to_date = self.__format_date(min(current+delta, end), is_parsed=True)
                ranges.append({"dateFrom":from_date, "dateTo": to_date})
                current += delta
            return ranges
        
        #takes the array of dictionaries and flattens their depth
        def __flatten(self, d, parent_key='', sep='_'):
            items = []
            for k, v in d.items():
                new_key = parent_key + sep + k if parent_key else k
                if isinstance(v, collections.MutableMapping):
                    items+=self.__flatten(v, new_key, sep=sep).items()
                else:
                    items.append((new_key, v))
            return dict(items)
        
        #goes through all the pages and concatenates their content
        def __fetch_all_data_pages(self, initial_url, data_type, info_string):
            data_array = []
            connection = HTTPSConnection(self.base_url)
            
            next_url = initial_url
            is_done = False
            sys.stdout.write("Downloading %s batch  %s:\n" % (data_type, info_string))
            while not is_done:
                try:
                    connection.request('GET', next_url, headers=self.headers)
                    res = connection.getresponse()
                except:
                    raise Exception("Could not connect to your Cumulocity tenant. Make sure your tenant URL is correct.")

                json_data= res.read()
                data = json.loads(json_data)
                
                #if request failed, throw the error to user
                if("error" in data.keys()):
                    raise Exception("Downloading %s failed: " % data_type + data["error"])
                
                #add data to the array
                data_array+=data[data_type]
                
                if int(data["statistics"]["totalPages"]) == 0:
                    return "NO_DATA"
                
                
                #print progress to the userz
                progress = (float(data["statistics"]["currentPage"]) / float(data["statistics"]["totalPages"])) * 100
                sys.stdout.write('\r')
                # the exact output you're looking for:
                sys.stdout.write("[%-20s] %.2f%%" % ('='*(int(progress/5)), progress))
                sys.stdout.flush()

                # if last page is concatenated, end while loop
                if(data["statistics"]["currentPage"] == data["statistics"]["totalPages"]):
                    is_done = True
                
                if("next" in data.keys()):
                    next_url = data["next"]

            connection.close()
            sys.stdout.write("\n")
            return data_array
        
        def get_measurements(self, date_from=None, date_to=None, device_id=None, measurement_id=None, measurement_type=None, value_fragment_type=None, value_fragment_series=None, timedelta=None, page_size=2000):
            device_id_param = "&source=%s" % str(device_id) if device_id else ""
            measurement_id_param = "&measurementId=%s" % str(measurement_id) if measurement_id else ""
            type_param = "&type=%s" % measurement_type if measurement_type else ""
            value_fragment_type_param="&valueFragmentType=%s" % value_fragment_type if value_fragment_type else ""
            value_fragment_series_param="&valueFragmentSeries=%s" % value_fragment_series if value_fragment_series else ""
            
            dates = self.__datetime_range(date_from, date_to, timedelta)

            data=[]
            for i in range(len(dates)):
                date_period = dates[i]
                date_period_from = date_period["dateFrom"]
                date_period_to = date_period["dateTo"]
                date_from_param = "&dateFrom=%s" % date_period_from if date_period_from else ""
                date_to_param = "&dateTo=%s" % date_period_to if date_period_to else ""
                
                #create query url and start making requests for data
                query_url = '/measurement/measurements?pageSize=' + str(page_size) + measurement_id_param + device_id_param + date_from_param + date_to_param + type_param + value_fragment_type_param + value_fragment_series_param + "&withTotalPages=true"
                data_fragment = self.__fetch_all_data_pages(query_url, "measurements", "%s of %s" % (i+1, len(dates)))
                if data_fragment == "NO_DATA":
                    logging.warning("No data exists in your tenant with the given parameters")
                    break
                data+=data_fragment
            
            #flatten multi level json structure to one dimension dictionary
            return pd.DataFrame([self.__flatten(m) for m in data])
        
        def get_events(self, date_from=None, date_to=None, device_id=None, event_type=None, fragment_type=None, page_size=2000, timedelta=None):
            device_id_param = "&source=%s" % str(device_id) if device_id else ""
            type_param = "&type=%s" % event_type if event_type else ""
            fragment_type_param="&fragmentType=%s" % fragment_type if fragment_type else ""
            
            dates = self.__datetime_range(date_from, date_to, timedelta)

            data=[]
            for i in range(len(dates)):
                date_period = dates[i]
                date_period_from = date_period["dateFrom"]
                date_period_to = date_period["dateTo"]
                date_from_param = "&dateFrom=%s" % date_period_from if date_period_from else ""
                date_to_param = "&dateTo=%s" % date_period_to if date_period_to else ""
                
                #create query url and start making requests for data
                query_url = "/event/events?pageSize=%s" % str(page_size) + date_from_param + date_to_param + device_id_param + type_param + fragment_type_param + "&withTotalPages=true"
                data_fragment = self.__fetch_all_data_pages(query_url, "events", "%s of %s" % (i+1, len(dates)))
                if data_fragment == "NO_DATA":
                    logging.warning("No data exists in your tenant with the given parameters")
                    break
                data+=data_fragment
            
            #flatten multi level json structure to one dimension dictionary
            return pd.DataFrame([self.__flatten(e) for e in data])
        
        def get_devices(self, device_type=None, fragment_type=None, ids=None, text=None, page_size=2000):
            device_type_param = "&deviceType=%s" % device_type if device_type else ""
            fragment_type_param = "&fragmentType=%s" % fragment_type if fragment_type else ""
            ids_param = "&ids=%s" % ",".join([str(i) for i in ids]) if ids else ""
            text_param = "&text=%s" % text if text else ""
            
            #create query url and start making requests for data
            query_url = "/inventory/managedObjects?pageSize=%s" % str(page_size) + device_type_param + fragment_type_param + ids_param + text_param + "&withTotalPages=true"
            data = self.__fetch_all_data_pages(query_url, "managedObjects", "devices")
            if data == "NO_DATA":
                logging.warning("No data exists in your tenant with the given parameters")
            #flatten multi level json structure to one dimension dictionary
            return pd.DataFrame([self.__flatten(m) for m in data])