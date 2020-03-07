This package allows you to connect to your cumulocity platform and query historical data from their REST API. Currently it only supports devices, measurements and events endpoints. The returned json data is converted to a pandas dataframe.

# Getting started

```python
pip install cumulocitypython
```

## import lthe CumulocityConnection class

```python
from cumulocitypython import CumulocityConnection
```

## Enter your credentials and create the connection

```python
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
tenant_url = "YOUR_TENANT_URL"

connection = CumulocityConnection(tenant_url, username, password)
```

This creates basic auth headers with your credentials. Make sure you don't include the http/https prefix when entering your tenant url.

# Query your data

All the argument values should be available in your cumulocity tenant.

## Measurements

```python
measurement_data = connection.get_measurements(
            value_fragment_type="c8y_EngineMetric",
            date_from="07-11-19 03:00:00",
            date_to="07-13-19 04:00:00",
        )
```

#### Arguments

These are the arguments that the get_measurements function can take. All of them are optional. The arguments are used to filter the data returned to you by Cumulocity.

| Arg                   | Default value | Accepted values                         | Description                                                   |
| --------------------- | ------------- | --------------------------------------- | ------------------------------------------------------------- |
| date_from             | None          | any widely used date format as a string | starting date from which you want to request data from.       |
| date_to               | None          | any widely used date format as a string | end date from which you want to request data to.              |
| device_id             | None          | any device id as a int or string        | id of the device from which you want to request data from.    |
| measurement_id        | None          | any measurement id as a int or string   | id of the measurement you want to request.                    |
| measurement_type      | None          | any measurement type as a string        | type of the measurement you want to request.                  |
| value_fragment_type   | None          | any value fragment type as a string     | value fragment type of the measurement you want to request.   |
| value_fragment_series | None          | any value fragment series as a strinh   | value fragment series of the measurement you want to request. |
| timedelta             | None          | timedelta object                        | speeds up big queries. supports minutes, hours, days, weeks.  |
| page_size             | 2000          | integer from 1 to 2000                  | determines the amount of rows sent by each request.           |

#### Returns

A pandas dataframe object

## Events

```python
event_data = connection.get_events(
            device_id="194442191",
            date_from="07-30-19 12:00:00",
            date_to="07-30-19 13:00:00",
            timedelta=timedelta(hours=3)
        )
```

#### Arguments

These are the arguments that the get_events function takes

| Arg           | Default value | Accepted values                         | Description                                                  |
| ------------- | ------------- | --------------------------------------- | ------------------------------------------------------------ |
| date_from     | None          | any widely used date format as a string | starting date from which you want to request data from.      |
| date_to       | None          | any widely used date format as a string | end date from which you want to request data to.             |
| device_id     | None          | any device id as a int or string        | id of the device from which you want to request data from.   |
| event_type    | None          | any event type as a string              | type of the event you want to request.                       |
| fragment_type | None          | any fragment type as a string           | fragment type of the event you want to request               |
| timedelta     | None          | timedelta object                        | speeds up big queries. supports minutes, hours, days, weeks. |
| page_size     | 2000          | integer from 1 to 2000                  | determines the amount of rows sent by each request.          |

#### Returns

A pandas dataframe object

## Devices

```python
ids=[117925736,117925737,117925738,117925739]
device_data = connection.get_devices(ids=ids, page_size=1000)
```

#### Arguments

These are the arguments that the get_devices function takes

| Arg           | Default value | Accepted values                      | Description                                               |
| ------------- | ------------- | ------------------------------------ | --------------------------------------------------------- |
| device_type   | None          | any device type as a string          | type of the device you want to request data from.         |
| fragment_type | None          | any device fragment type as a string | fragment type of the device you want to request data to.  |
| ids           | None          | list of int or string id values      | list of ids of the devices you want to request data from. |
| text          | None          | text as a string                     | attached text of the devices you want to request.         |
| page_size     | 2000          | integer from 1 to 2000               | determines the amount of rows sent by each request.       |

#### Returns

A pandas dataframe object

## Export data to a CSV

You might want to save the requested data to a csv so there is no need to request it a second time.
Since all functions return a Pandas dataframe, you can easily use the built in pandas dataframe function: to_csv

Example:

```python
event_data = connection.get_events(
            device_id="194442191",
            date_from="07-30-19 12:00:00",
            date_to="07-30-19 13:00:00",
            timedelta=timedelta(hours=3)
        )

event_data.to_csv("YOUR_CSV_NAME.csv", index=False, encoding="utf8")
```
