# download and inflate google chromedriver to bin directory
mkdir -p usmle_cal/bin
version=`curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE`
download_url="https://chromedriver.storage.googleapis.com/$version/chromedriver_mac64.zip"
curl "$download_url" > bin/chromedriver_mac64.zip
cd bin
unzip -o chromedriver_mac64.zip
rm -rf chromedriver_mac64.zip
cd ..
