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

    info("\nConfiguring nodes\n\n")
    for host in ndn.net.hosts:
        value = host.params['params'].get('type',"consumer")
        if (value=="producer"):
            host.cmd('export NDN_LOG=examples.PartialSyncProducerApp=INFO')
        if (value=="consumer"):
            host.cmd('export NDN_LOG=examples.PartialSyncConsumerApp=INFO')

        #### Multiple prefixes
        data = host.params['params'].get('prefix',"")
        if(data):
            data = data.split("+")
            for data_prefix in data:
                grh.addOrigin([ndn.net[str(host)]], [data_prefix])
                info(str(host) + " declared producer for " + data_prefix+"\n")
        #####

        run_cmd = host.params['params'].get('run')    
        if(run_cmd):
            run_cmd = run_cmd.replace("+"," ")
            host.cmd(run_cmd+' &')
            info(str(host) + " is running "+ run_cmd+"\n")

    info("\n")
    grh.calculateNPossibleRoutes()

    MiniNDNCLI(ndn.net)

    ndn.stop()
