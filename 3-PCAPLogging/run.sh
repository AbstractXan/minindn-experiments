echo "Running experiment"
sudo python ./src/experiment.py ./src/topology.conf;
# Merge
cd /tmp/minindn/log;
sudo rm merged.pcap
sudo mergecap -w merged.pcap `fd pcap`;
sudo tshark -T text -Y udp -r merged.pcap;
