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
      },
      {}, {}, {}
    ]
}
```
The server will send this .pdf to the default printer with help of CUPS (https://www.cups.org/). After printing it will perform a PATCH request to the 
API endpoint for handling remote queues.

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
```

## Help with .env
You should always include a default printer (PRINTER_LOCATION_DEFAULT). When not given a default printer, the jobs 
will not be processed. Beside the default printer, you could configure print locations. These locations can be given 
in de REST response with the `print_location` field. The location should be defined in the env as the following way:

`PRINTER_LOCATION_another_brother=Brother_Another`

The server will first look for a printer location with the named value. If none was given (or found) it will be printed to the 
default printer.

## Run the server:
`python3 main.py listen`

## Print single file:
`python3 main.py print path/file.pdf [optional location]`

## Possible flags, see help:
```
python main.py listen --help
python main.py print --help
```

