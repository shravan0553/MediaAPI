## Media Service Live 4 Stream Update Automation - Python

This python script automates MSL4 stream updates using Akamai Media AI endpoint. https://developer.akamai.com/api/media_delivery/msl_stream_provisioning/v2.html#putaspecificstreamid
So far the script supports updates to XBC regions, Preferred EntryPoint regions, Archiver settings and stream deletion.

### Pre-requisite:

1. This script requires AkamaiOPEN library. Please follow the AkamaiOPEN instruction below and get edgegrid-python installed.    https://github.com/akamai/AkamaiOPEN-edgegrid-python
   ```
   $ pip install edgegrid-python
   ```
2. You would need a valid API credentials with approrite Read/Write permissions in order to execute the script.

### Credentials:

Please make sure that your API credentials are copied to a file named "**credentials**" under the same directory as the python scripts. You can use the "**credentials**" template uploaded here.

```
client_secret = 
host = 
access_token = 
client_token = 
```

### Input:

Update column "B" of the "**input_streams.csv**" file with the list of streamID's that need to be updated. 
```
Stream Name   Stream ID
Example Stream 	123445
Example Stream 	123446
Example Stream 	123447
Example Stream 	123448
Example Stream 	123449
Example Stream 	123450
Example Stream 	123451
Example Stream 	123452
Example Stream 	123453
Example Stream 	123454
Example Stream 	123455
Example Stream 	123456
```

### Options:
```bash
usage: UpdateStreamIDs.py [-h] [--xbc] [--ent] [--arc] [--rem]

optional arguments:
  -h, --help  show this help message and exit
  --xbc       use this option to update XBC regions
  --ent       use this option to update entrypoint regions
  --arc       use this option to update Archive Settings
  --rem       use this option to delete the streams
```
