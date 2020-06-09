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


    for host in ndn.net.hosts:
	value = host.params['params'].get('type',"client")
	if (value=="server"):
            data_prefix = host.params['params'].get('prefix',"/example/testApp")
            # For all host, pass ndn.net.hosts or a list, [ndn.net['a'], ..] or [ndn.net.hosts[0],.]
            grh.addOrigin([ndn.net[str(host)]], [data_prefix])
        run_cmd = host.params['params'].get('run',"../apps/consumer")
	host.cmd(run_cmd+' &')
    grh.calculateNPossibleRoutes()

    '''
    prefix "/example/testApp" is advertise from node A, it should be reachable from all other nodes.
    '''
    '''
    routesFromA = ndn.net.cmd("nfdc route | grep -v '/localhost/nfd'")
    if '/ndn/b-site/b' not in routesFromA or \
       '/ndn/c-site/c' not in routesFromA or \
       '/ndn/d-site/d' not in routesFromA:
        info("Route addition failed\n")

    routesToPrefix = ndn.net['b'].cmd("nfdc fib | grep '/example/testApp'")
    if '/example/testApp' not in routesToPrefix:
        info("Missing route to advertised prefix, Route addition failed\n")
        ndn.net.stop()
        sys.exit(1)

    info('Route addition to NFD completed\n')
    '''

    ####### Setting up HOME
    #for host in ndn.net.hosts:
       #host.cmd("export HOME=/tmp/minindn/"+str(host)+"; cd;")
    #ndn.net['a'].cmd("../apps/producer &")
    #######

    MiniNDNCLI(ndn.net)

    ndn.stop()
