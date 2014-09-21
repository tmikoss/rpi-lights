HOST=raspberrypi.local.net
USER=pi
APP_NAME=rpi-lights
APP_DIR="/home/$USER/$APP_NAME"

DEPLOY_SCRIPT="
sudo stop $APP_NAME;
cd $APP_DIR;
git pull;
sudo pip install -r requirements.txt;
sudo start $APP_NAME;
"

echo "Deploying..."
ssh $USER@$HOST $DEPLOY_SCRIPT
