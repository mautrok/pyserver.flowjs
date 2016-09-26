import logging, sys,json,configimpl,os
"""
the werkzeug's module version is the 0.10.*
the latest give me a winerror 10038, on windows,
and i was unable to find a solution 
"""
from werkzeug import secure_filename

from fileuploadutils import chunkOperationUtil

from flask import render_template, url_for, redirect, Flask, request,Response, current_app

app = Flask(__name__)
#file where to find the log configurations
logging.basicConfig(filename=configimpl.config.get('fileconfig','logpath'),level=logging.INFO)
#path where file will be saved
uploadpath=configimpl.config.get('fileconfig','uploadedpath')

"""
        this metthod take cover
        of the CORS options
"""
def corsbuildresponse(responseflask,requestflaskorigin):
	responseflask.headers['Access-Control-Allow-Credentials']='true'
	responseflask.headers['Access-Control-Allow-Origin']=requestflaskorigin
	responseflask.headers['Access-Control-Allow-Headers']='content-type'
	responseflask.headers['Access-Control-Allow-Methods']='POST, GET, OPTIONS,DELETE,PUT'

@app.route('/')
def index():
	return redirect(url_for('static', filename='index.html'))

@app.route('/upload',methods=['GET','POST'])
def upload():
	resp=Response()
	filename=None
	responseTotalChunks=None
	"""
        flow js always send a get befora a post, the first
        one give some information for the program to use to
        build the file when the upload is finished
        """
	if (request.method == 'GET'):
		#check the validity of the file
		filename=str(request.args.get('flowFilename'))
		responseTotalChunks={'totalchunks':request.args.get('flowTotalChunks')}
		n = json.dumps(responseTotalChunks)
		resp.data=n
		resp.status='400'
		return resp
	else:
                filename=request.form['flowFilename']
                chunkOperationUtil(request,resp)
                if os.path.isfile(uploadpath+configimpl.config.get('fileconfig','folderlike')+filename):
                        path=str(configimpl.config.get('fileconfig','uploadforhtml')+filename)
                        responseTotalChunks={'msg':'file upload complete','address':path,'filename':filename}
                else:
                        logging.info('file not yet completed %s ' % str(request.form['flowChunkNumber']))
                n = json.dumps(responseTotalChunks)
                resp.data=n
                return resp

if __name__ == '__main__':
        app.debug=configimpl.config.getboolean('flask','debug')
        app.run(host=configimpl.config.get('flask','host'),port=configimpl.config.getint('flask','port'))
