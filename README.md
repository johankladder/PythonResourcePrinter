# PythonResourcePrinter
A package to print external labels on a local labelprinter. This application is intended to run on a Raspberry Pi.
The application will poll a API endpoint for print jobs and create printable .pdf files from the 
given base64 data. An example response for this API is:

```json
{
    "data": [
      {
          "id": 1,
          "label_base64": "a-base-64-pdf-string"
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
AUTH_TOKEN=KlaDDeR
LP_OPTIONS=-o orientation-requested=4
PING_URL=https://beats.envoyer.io/heartbeat/a-heart-beat-id
```

## Run:
`python3 main.py listen`

## Possible flags:
`python3 main.py listen --help`
