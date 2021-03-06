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

    '''
    Experiment run with default topology, test cases won't work with other topologies
                          # With calculateNPossibleRoutes,
            10            # routing = hr, N = All, from A, 3 routes needs to added to NFD.
        a +++++++ b       # a - b  -- cost 10
        +         +       # a - c  -- cost 10
     10 +         + 10    # a - d  -- cost 20
        +         +       # Same goes for B being a source.
        c         d       #
    '''
    topo = Topo()
    a = topo.addHost('a')
    b = topo.addHost('b')
    c = topo.addHost('c')
    d = topo.addHost('d')
    topo.addLink(a, b, delay='10ms')
    topo.addLink(a, c, delay='10ms')
    topo.addLink(b, d, delay='10ms')

    ndn = Minindn(parser=parser, topo=topo)

    ndn.start()

    info('Starting NFD on nodes\n')
    nfds = AppManager(ndn, ndn.net.hosts, Nfd)
    info('Adding static routes to NFD\n')
    grh = NdnRoutingHelper(ndn.net, ndn.args.faceType, ndn.args.routingType)
    # For all host, pass ndn.net.hosts or a list, [ndn.net['a'], ..] or [ndn.net.hosts[0],.]
    grh.addOrigin([ndn.net['a']], ["/example/testApp"])
    grh.calculateNPossibleRoutes()

    '''
    prefix "/example/testApp" is advertise from node A, it should be reachable from all other nodes.
    '''
    routesFromA = ndn.net['a'].cmd("nfdc route | grep -v '/localhost/nfd'")
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


    ####### Setting up HOME
    #for host in ndn.net.hosts:
       #host.cmd("export HOME=/tmp/minindn/"+str(host)+"; cd;")
    ndn.net['a'].cmd("../apps/producer &")
    #######
    info(' ')
    info("\n'a' has been initialised as the producer\n")
    info('Run <host> ../apps/consumer to define consumers\n')
    MiniNDNCLI(ndn.net)

    ndn.stop()
