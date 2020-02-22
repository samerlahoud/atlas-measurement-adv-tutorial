# Advanced Tutorial on RIPE Atlas Measurements

This project enables to automate measurements using the RIPE Atlas platform. Measurements (ping and traceroute) are performed between a set probes in different countries towards a set of servers in different destination networks.

The project includes scripts that perform the following tasks: 
- Creating measurements
- Sopping measurements
- Retrying failed measurements
- Getting measurements results

This is a simplified version of the original project provided in https://github.com/georgeshachem/menog-internet-study.

## How to Use this Code

1. Modify the list of countries in ``countries.json``. The source of the measurements will be probes available in these countries.
2. Modify the list of destination networks in ``destionationNetworks.json``. The destination of the measurements will be the hosts in each destination network.
3. Create measurements using ``python createAllMeasurements.py``. You can modify the following parameters:
  
```
ATLAS_API_KEY = " "
max_nb_servers = 3
nb_requested_probes = 3
ping_interval = 10800
traceroute_interval = 10800
tag_list = ["test-code-esib"] 
```
You can find in ``measurements`` folder the results of the creation request including the measurement id.

 
