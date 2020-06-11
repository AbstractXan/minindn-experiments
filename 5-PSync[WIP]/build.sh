sudo ls
rm -r -d apps
mkdir apps
echo "Rebuilding apps/"
echo "Building Consumer"
g++-10 ./src/consumer.cpp -lndn-cxx -lPSync -DBOOST_LOG_DYN_LINK -lboost_system -lboost_filesystem  -lpthread -o ./apps/consumer;
echo "Building Producer"
g++-10 ./src/producer.cpp -lndn-cxx -lPSync -DBOOST_LOG_DYN_LINK -lboost_system -lboost_filesystem -lpthread -o ./apps/producer;
echo "Copying builds to /tmp/minindn/apps"
sudo rm -r -d /tmp/minindn/apps 2> /dev/null
sudo mkdir /tmp/minindn/apps 2> /dev/null
sudo cp -r apps /tmp/minindn/
echo "Done"
echo " "
echo "You can now run ./run.sh"
