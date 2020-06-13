import argparse
import sys

from mininet.log import setLogLevel, info
from mininet.topo import Topo

from minindn.minindn import Minindn
from minindn.util import MiniNDNCLI
from minindn.apps.app_manager import AppManager
from minindn.apps.nfd import Nfd
from minindn.helpers.ndn_routing_helper import NdnRoutingHelper

if __name__ == '__main__':
    setLogLevel('info')

    Minindn.cleanUp()
    Minindn.verifyDependencies()

    parser = argparse.ArgumentParser()
    parser.add_argument('--face-type', dest='faceType', default='udp', choices=['udp', 'tcp'])
    parser.add_argument('--routing', dest='routingType', default='link-state',
                         choices=['link-state', 'hr', 'dry'],
                         help='''Choose routing type, dry = link-state is used
                                 but hr is calculated for comparision.''')

    ndn = Minindn(parser=parser)

    ndn.start()

    info('Starting NFD on nodes\n')
    nfds = AppManager(ndn, ndn.net.hosts, Nfd)
    info('Adding static routes to NFD\n')
    grh = NdnRoutingHelper(ndn.net, ndn.args.faceType, ndn.args.routingType)

    ####### Configuring nodes based on input parameters
    info("\nConfiguring nodes\n\n")
    for host in ndn.net.hosts:
	value = host.params['params'].get('type',"client")
	if (value=="server"):
            data_prefix = host.params['params'].get('prefix',"/example/testApp")
            # For all host, pass ndn.net.hosts or a list, [ndn.net['a'], ..] or [ndn.net.hosts[0],.]
            grh.addOrigin([ndn.net[str(host)]], [data_prefix])
            info(str(host) + " declared producer for " + data_prefix+"\n")
        run_cmd = host.params['params'].get('run')
	if(run_cmd):
	    host.cmd(run_cmd+' &')
            info(str(host) + " is running "+ run_cmd+"\n")
    info("\n")
    grh.calculateNPossibleRoutes()
    ######## 

    info("\n'a' has been initialised as the producer\n")
    info('Run <host> ../apps/consumer to define consumers\n')

    MiniNDNCLI(ndn.net)

    ndn.stop()
