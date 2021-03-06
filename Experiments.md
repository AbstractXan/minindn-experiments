### Scenario 1: Basic
Host 'a' is producer with producer already running in background. 
Run `<host> ../apps/consumer` in other hosts.

### Scenario 2: Topology.conf

[Asciinema demo](https://asciinema.org/a/gbkU4ITHnt4fs9buS5YcT5r0b)

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

[Asciinema demo](https://asciinema.org/a/WnwGRzs4NTZTU1WVKUHUnNP8I)

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

### Scenario 4: ChatAB
Run `./build.sh` followed by `./run.sh`

Run `mini-ndn> xterm a b`

For host 'a': `export HOME=/tmp/minindn/a ; cd ; ../apps/chat_a`
For host 'b': `export HOME=/tmp/minindn/b ; cd ; ../apps/chat_b`

### Scenario 5: PSync

[Asciinema demo](https://asciinema.org/a/2FY57d9WlgROPOAw0DErwI9Ro)

Run `./build.sh` followed by `./run.sh`. This will open mini-ndn.

Run `mini-ndn> a ../apps/producer /sync /a 10 1 &`

Run `mini-ndn> b ../apps/consumer /sync 5`

Change `./src/topology.conf` to configure nodes as follows:
1. type : 
	- _Values_ : producer/consumer  (default value: consumer)
	- Identifies the type of node
	- Setup and displays logs
2. prefix : 
	- _Values_ :(default: /example/testApp)
	- Configures FIBs of other nodes with the current node as producer of the data prefix 
	- **REQUIRED for producer**
