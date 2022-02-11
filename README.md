# PythonResourcePrinter     [![CircleCI](https://circleci.com/gh/johankladder/PythonResourcePrinter/tree/master.svg?style=svg)](https://circleci.com/gh/johankladder/PythonResourcePrinter/tree/master)
A package to print external labels on a local labelprinter. This application is intended to run on a Raspberry Pi.
The application will poll a API endpoint for print jobs and create printable .pdf files from the 
given base64 data. An example response for this API is:

```json
{
    "data": [
      {
          "id": 1,
          "label_base64": "a-base-64-pdf-string",
          "print_location": 1 // (Optional)
          "print_location_mix": 2 // (Optional)
          "n_mix": 3 // (Optional)
      },
      {}, {}, {}
    ]
}
```
The server will send this .pdf to the default printer with help of CUPS (https://www.cups.org/). After printing it will perform a PATCH request to the 
API endpoint for handling remote queues. When given the n_mix key, the server will split the provided pdf into mix labels and 
default labels. The mix labels will then be printed to the mix printer (if provided, otherwise to the given print_location) and the default 
labels to the base printer

## Install needed dependencies
`pip3 install -r requirements.txt`

## Initialise .env
See the .env-example for possible values. In general this would be:
```
PRINT_QUEUE_BASE_URL=https://api.printqueue.nl/get-queue
AUTH_TOKEN=secret
LP_OPTIONS=-o landscape -o fit-to-page -o media=Custom.102x152mm
PING_URL=https://beats.envoyer.io/heartbeat/a-heart-beat-id
PRINTER_LOCATION_DEFAULT=Brother
PRINTER_LOCATION_[*]=
WLED_IP=*.*.*.*
```

## Help with .env
You should always include a default printer (PRINTER_LOCATION_DEFAULT). When not given a default printer, the jobs 
will not be processed. Beside the default printer, you could configure print locations. These locations can be given 
in de REST response with the `print_location` field. The location should be defined in the env as the following way:

`PRINTER_LOCATION_another_brother=Brother_Another`

The server will first look for a printer location with the named value. If none was given (or found) it will be printed to the 
default printer.

## WLED
The server also supports WLED. Please provide your own custom presets within the app. Also set the WLED ip in the environment.
The server will then look up the current visual preset and send the matching preset to indicate a status update.
The status-presets are mapped in the following way:

```python
    preset_map = {
        Status.IDLE: 2,
        Status.ERROR: 3,
        Status.PRINTING: 4,
        Status.ON: 5,
        Status.OFF: 6,
        Status.PINGING: 7,
    }
```

The status on will also force WLED to turn the lights on.

## Run the server:
`python3 main.py listen`

## Print single file:
`python3 main.py print path/file.pdf [optional location]`

## Split single file:
`python3 main.py split path/file.pdf [optional n_mix]`

## Remove documents:
`python3 main.py clean`

## Test wled:
`python3 main.py wled [status]`


## Possible flags, see help:
```
python main.py listen --help
python main.py print --help
python main.py split --help
python main.py wled --help
```

