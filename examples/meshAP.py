#!/usr/bin/python

'This example shows how to create wireless link between two APs'

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference)

    info("*** Creating nodes\n")
    #h1 = net.addHost('h1')
    #h2 = net.addHost('h2')
    
    d1 = net.addDocker('d1', ip='10.0.0.251', dimage="ubuntu:trusty")
    d2 = net.addDocker('d2', ip='10.0.0.252', dimage="ubuntu:trusty")
    
    #sta1 = net.addStation('sta1', mac='00:00:00:00:00:11', position='1,1,0')
    #sta2 = net.addStation('sta2', mac='00:00:00:00:00:12', position='31,11,0')
    
    ap1 = net.addAccessPoint('ap1', wlans=1, position='10,10,0')
    ap2 = net.addAccessPoint('ap2', wlans=1, position='30,10,0')
    c0 = net.addController('c0')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating Stations\n")
    net.addLink(d1, ap1)
    net.addLink(d2, ap2)
    net.addLink(ap1, intf='ap1-wlan1', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap2, intf='ap2-wlan1', cls=mesh, ssid='mesh-ssid', channel=5)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
