# minindn-experiments
Experiments running NDN applications on Mini-NDN.

## Running scenarios
Build using `./build.sh`. Builds producer.cpp and consumer.cpp and copies to `/tmp/minindn/apps`. This could then be accessed by minindn nodes as shown below.

Run minindn: `./run.sh`

### Scenario 1:
Host 'a' is producer with producer already running in back ground. 
Run `<host> ../apps/consumer` in other hosts.

### Scenario 2:
Change `./src/topology.conf` to configure nodes as follow:
1. type : 
	- _Values_ : server/client  (default value: client)
	- Identifies the type of node
2. prefix : 
	- _Values_ :(default: /example/testApp)
	- Configures FIBs of other nodes with the current node as producer of the data prefix 
	- Only valid for **producers**
3. run : (default: '')
	- _Values_ :(default: /example/testApp)
	- Runs NDN application in the background
	- The path provided should be relative to `/tmp/minindn/x` where x is current node
	- Refer to topology.conf for usage
