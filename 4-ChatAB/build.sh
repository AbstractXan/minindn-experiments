sudo ls
rm -r -d apps
mkdir apps
echo "Rebuilding apps/"
echo "Building A"
g++ ./src/chat_a.cpp -lndn-cxx -lboost_system -lboost_filesystem -o ./apps/chat_a;
echo "Building B"
g++ ./src/chat_b.cpp -lndn-cxx -lboost_system -lboost_filesystem -o ./apps/chat_b;
echo "Copying builds to /tmp/minindn/apps"
sudo rm -r -d /tmp/minindn/apps 2> /dev/null
sudo mkdir /tmp/minindn/apps 2> /dev/null
sudo cp -r apps /tmp/minindn/
echo "Done"
echo " "
echo "You can now run ./run.sh"
