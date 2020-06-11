sudo ls
rm -r -d apps
mkdir apps
echo "Rebuilding apps/"
echo "Building Consumer"
g++ -DBOOST_LOG_DYN_LINK -c ./src/consumer.cpp
g++ consumer.o -lndn-cxx -lPSync -lboost_system -lboost_log -lpthread -o ./apps/consumer
rm consumer.o
echo "Building Producer"
g++ -DBOOST_LOG_DYN_LINK -c ./src/producer.cpp
g++ producer.o -lndn-cxx -lPSync -lboost_system -lboost_log -lpthread -o ./apps/producer
rm producer.o
echo "Copying builds to /tmp/minindn/apps"
sudo rm -r -d /tmp/minindn/apps 2> /dev/null
sudo mkdir /tmp/minindn/apps 2> /dev/null
sudo cp -r apps /tmp/minindn/
echo "Done"
echo " "
echo "You can now run ./run.sh"