Media Service Live 4 Stream Update Automation - Python

This python script automates MSL4 stream updates using Akamai Media AI endpoint. https://developer.akamai.com/api/media_delivery/msl_stream_provisioning/v2.html#putaspecificstreamid
So far the script supports updates to XBC regions, Preferred EntryPoint regions and Archive settings.

Pre-requisite:

This script requires AkamaiOPEN library. Please follow the AkamaiOPEN instruction below and get edgegrid-python installed. https://github.com/akamai/AkamaiOPEN-edgegrid-python
$ pip install edgegrid-python
Akamai LUNA API Client. You would need a valid credentials with approrite Read/Write permissions in order to perform changes.

Credentials:

Please make sure that your API credentials are copied to a file named "credentials" under the same directory as the python scripts. You can use the "credentials" template uploaded here.

Input:

Update column "B" of the "input_streams.csv" file with the list of streamID's that need to be updated. 

Stream Name	Stream ID
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

Options:

usage: UpdateStreamIDs.py [-h] [--xbc] [--ent] [--arc]

optional arguments:
  -h, --help  show this help message and exit
  --xbc       use this option to update XBC regions
  --ent       use this option to update entrypoint regions
  --arc       use this option to update Archive Settings
