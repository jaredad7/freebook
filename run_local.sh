#Run the main app using flask

#OS detection
os=${OSTYPE//[0-9.]/}

if [[ "$os" == 'darwin' ]] #Mac
	then
	export FLASK_APP=app.py
	/usr/local/bin/flask run
else #Windows
	echo "Please input instructions for running locally on Windows to run_local.sh"
fi