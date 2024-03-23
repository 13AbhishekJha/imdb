### Python
Download python 3.6 on the machine using the following link https://www.python.org/ftp/python/3.6.8/python-3.6.8-macosx10.9.pkg which will download python 3.6.8 for macOS.

### Version Control
Clone repo from repository-url by running :-

git clone -b development https://github.com/13AbhishekJha/YoutubeApi.git
cd YoutubeApi

### Setup Virtual Environment
Install virtualenv using command : 
pip3 install virtualenv 
Execute command : virtualenv -p python3 venv 
Execute command : source venv/bin/activate 
Verify python version by running python --version

#### Next Steps
Change to the imdb directory and install python dependencies for project:
`pip3 install -r requirements.txt --use-deprecated=legacy-resolver`

### Setup Mongo
* Download and Install MongoDB: Visit the official MongoDB website to download the appropriate version for your operating system: MongoDBDownload
* Installation: Follow the installation instructions provided for your operating system.

* Start MongoDB Server:
    * Windows: After installation, navigate to the MongoDB installation directory in Command Prompt and run mongod to start the MongoDB server.
    * macOS/Linux: After installation, open a terminal window and run mongod to start the MongoDB server.

* Verify MongoDB is Running: After starting MongoDB, you should see log messages indicating that the server has started successfully. You can also try connecting to the MongoDB server using the mongo shell to verify that it's running:
    mongo
This will open the MongoDB shell where you can execute commands against the MongoDB server.

* Create Database and Collections: You can use the MongoDB shell or a GUI tool (such as MongoDB Compass) to create databases and collections as needed for your application. For example:
    use imdb
    This command switches to the imdb database. You can then create collections and insert documents as required.

* Once MongoDB is running locally and you have created the necessary databases and collections, your Flask application should be able to connect to MongoDB using the connection string specified in the app.py file. Make sure to update the connection string with the correct details if needed.

### Run project
Once setup is complete, run http://127.0.0.1:5000/login on browser