from cumulocitypython import CumulocityConnection
from datetime import timedelta

#insert credientals for the connection
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
tenant_url = "YOUR_TENANT_URL" # Without the http/https prefix

#Create the class and authentication to connect to Cumulocity
connection = CumulocityConnection(tenant_url, username, password)


#EXAMPLE
#Fetch measurements from Cumulocity
measurement_data = connection.get_measurements(
            value_fragment_type="c8y_EngineMetric",
            date_from="07-11-19 03:00:00",
            date_to="07-13-19 04:00:00",
        )

#Export the data to a csv
measurement_data.to_csv("YOUR_CSV_NAME.csv", index=False, encoding="utf8")


#EXAMPLE
#Fetch events from Cumulocity
event_data = connection.get_events(
            device_id="1198662331",
            date_from="07-30-19 12:00:00",
            date_to="07-30-19 13:00:00",
            timedelta=timedelta(hours=3)
        )

#Export the data to a csv
event_data.to_csv("YOUR_CSV_NAME.csv", index=False, encoding="utf8")


#EXAMPLE
ids=[117925736,117925737,117925738,117925739,117925740,117925741,117925742,117925743,117925744,117925745,117925746, 117925747, 117925748, 117925749, 117925750, 117925751]
#Fetch devices from Cumulocity
device_data = connection.get_devices(ids=ids, page_size=1000)

#Export the data to a csv
device_data.to_csv("YOUR_CSV_NAME.csv", index=False, encoding="utf8")