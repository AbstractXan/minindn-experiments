# minindn-experiments
Experiments running NDN applications on Mini-NDN.

## Running scenarios
Build using `./build.sh`. Builds producer.cpp and consumer.cpp and copies to `/tmp/minindn/apps`. This could then be accessed by minindn nodes as shown below.

Run experiment: `./run.sh`

### Scenario 1: Basic
Host 'a' is producer with producer already running in background. 
Run `<host> ../apps/consumer` in other hosts.

### Scenario 2: Topology.conf

[![asciicast](https://asciinema.org/a/gbkU4ITHnt4fs9buS5YcT5r0b.svg)](https://asciinema.org/a/gbkU4ITHnt4fs9buS5YcT5r0b)

Change `./src/topology.conf` to configure nodes as follows:
1. type : 
	- _Values_ : server/client  (default value: client)
	- Identifies the type of node
2. prefix : 
	- _Values_ :(default: /example/testApp)
	- Configures FIBs of other nodes with the current node as producer of the data prefix 
	- Only valid for **servers**
3. run : (default: '')
	- _Values_ :(default: /example/testApp)
	- Runs NDN application in the background
	- The path provided should be relative to `/tmp/minindn/x` where x is current node
	- Refer to topology.conf for usage

Note: Use non-zero delays for ndn_network_helper to correctly add routes to nodes in the network

Host 'a' is producer with producer already running in background. 
Run `<host> ../apps/consumer` in other hosts.

### Scenario 3 : PCAP Logging

[![asciicast](https://asciinema.org/a/WnwGRzs4NTZTU1WVKUHUnNP8I.svg)](https://asciinema.org/a/WnwGRzs4NTZTU1WVKUHUnNP8I)

Default logging done in `/tmp/minindn/log`.
Logging is done using tshark as shown in `src/experiment.py` :
```python
tshark = AppManager(ndn, ndn.net.hosts, Tshark, logFolder="../log/", singleLogFile=True)
```
Change the following parameters in `src/experiment.py` to if required:
1. logFolder : Folder where PCAP file(s) will be stored for each node
2. singleLogFile : Single PCAP file per node, or individual PCAP for each interface

Host 'a' is producer with producer already running in background. 
Run `<host> ../apps/consumer` in other hosts.

Exit MiniNDN, `./run.sh` proceeds- tshark now merges all the `.pcap` files and prints udp packet log.
