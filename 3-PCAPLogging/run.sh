echo "Running experiment"
sudo python ./src/experiment.py ./src/topology.conf;
# Merge
echo " "
echo "Mininet closed gracefully"
echo "Merging logs"
cd /tmp/minindn/log;
sudo rm merged.pcap 2> /dev/null
sudo mergecap -w merged.pcap `find *.pcap`
sudo tshark -T text -Y udp -r merged.pcap
echo "Logs merged to /tmp/minindn/log/merged.pcap"
echo "Experiment completed"