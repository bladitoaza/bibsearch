# Bibliometric search 

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Reproducible Capsule](https://img.shields.io/static/v1?label=&message=code+ocean&color=blue)](https://codeocean.com/capsule/0487318/tree/v1)

This is a simple scrypt that allows to use the SCOPUS API to perform multiple queries in a simpler way than using the traditional SCOPUS search when collecting data for bibliometric analysis. 

The example presented performs a bibliometric search of a list algorithms from a **.xlsx** file that can be used in [VOSviewer.](https://www.vosviewer.com/)


## Prerequisites

To run the script you need:
- An Elsevier API key which can be obtained by following the instructions in the [Elsevier Developer Portal.](https://dev.elsevier.com)
- The [elsapy](https://github.com/ElsevierDev/elsapy) Python module.
- A **.xlsx** file with the list of queries accomplishing the [SCOPUS advaced search format](https://service.elsevier.com/app/answers/detail/a_id/11365/supporthub/scopus/#tips) (optional)


## Installation/use

1. Download the file `exampleProg.py.`
1. Insert the Elsevier API it in the file `config.json.` 
1. Write the SCOPUS query or read it from the **.xlsx** file. This example reads the keyword "traveling salesmand problem" and an algorithm from the **.xlsx** file.
```
doc_srch = ElsSearch('TITLE-ABS-KEY("travelling salesman problem" AND "'+alg[0]+ '") AND PUBYEAR > 1964 AND PUBYEAR < 2023','scopus')
```
1. The script arrange all the bibliometric information and save it in the file `scopus_search.csv`

The output file `scopus_search.csv` has the format to be used as input in [VOSviewer.](https://www.vosviewer.com/)


## A note about API keys and IP addresses

The API Key is bound to a set of IP addresses, usually bound to your institution. Therefore, if you are using this for a another application, you must host the application from your institution servers in some way. Also, you cannot access the Scopus API with this key if you are offsite and must VPN into the server or use a computing cluster with an institution IP.


## Contributing

Contrubution and suggestions are welcome via GitHub Pull Requests.
