# IPS.ROCKS

## https://ips.rocks

ips.rocks can currently be used for a few things:

1. Determine your current IP and the relevant lookup information
2. Lookup information about another IP address
3. Get a plain response of your IP
4. Fetch the current time in epoch

**ips.rocks/**

Request: `curl https://ips.rocks/`

Response: `{"asn":64200,"city":"Guadalajara","country":"Mexico","latitude":20.676,"longitude":-103.3358,"network":"192.154.196.0/24","org":"VIVIDHOSTING","province/state":"Jalisco","query":"192.154.196.28"}`

**ips.rocks/api/?ip=<ipaddress>**

Request: `curl https://ips.rocks/api/?ip=8.8.8.8`

Response: `{"asn":15169,"city":"None","country":"United States","latitude":37.751,"longitude":-97.822,"network":"8.8.0.0/17","org":"GOOGLE","province/state":"None","query":"8.8.8.8"}`

**ips.rocks/plain**

Request: `curl https://ips.rocks/plain`

Response: `192.154.196.28`

**ips.rocks/time**

Request: `curl https://ips.rocks/time`

Response: `1616448630`



This product includes GeoLite2 data created by MaxMind, available from (https://www.maxmind.com).
