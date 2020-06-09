sudo ls
rm -r -d apps
mkdir apps
echo "Rebuilding apps/"
echo "Building Consumer"
g++ ./src/consumer.cpp -lndn-cxx -lboost_system -lboost_filesystem -o ./apps/consumer;
echo "Building Producer"
g++ ./src/producer.cpp -lndn-cxx -lboost_system -lboost_filesystem -o ./apps/producer;
echo "Copying builds to /tmp/minindn/apps"
sudo rm -r -d /tmp/minindn/apps 2> /dev/null
sudo mkdir /tmp/minindn/apps 2> /dev/null
sudo cp -r apps /tmp/minindn/
echo "Done"
echo " "
echo "You can now run ./run.sh"
