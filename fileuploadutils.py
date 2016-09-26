import os,shutil,logging,subprocess,configimpl

#path where to save the file
uploadpath=configimpl.config.get('fileconfig','uploadedpath')
#configuration for using pyserver.flowjs in windows o linux
#where to change the path separator
folderlike=configimpl.config.get('fileconfig','folderlike')

def cleantmp(arg0):
        try:
                for f in os.listdir(arg0):
                        os.remove(arg0+f)
                        logging.info('trying to remove %s ' % percorsotemporaneo)
                        shutil.rmtree(percorsotemporaneo)
        except:
                loggin.exception("message")

def createFileFromChunk(filename,chunksize,totalsize,tempPath,flowTotalChunks):
        total_files=0
        if not os.path.exists('tmpdir'):
                os.makedirs('tmpdir')
        for f in os.listdir(tempPath):
                if f.index(filename)!=-1:
                        total_files=total_files+1
        if total_files<1:
                return 'UPLOAD'
        if(total_files * int(chunksize))>=(int(totalsize)-int(chunksize) + 1):
                f=open(uploadpath+filename,'wb')
                logging.info('ending file %s ' % f)
                for i in range(1,total_files+1):
                        newFile=tempPath+filename+'.'+'part'+str(i)
                        logging.info('apro un nuovo file %s' % newFile)
                        file=open(newFile,'rb')
                        try:
                                f.write(file.read())
                        except:
                                logging.exception("message")
                        file.close()
                f.close()
                logging.info('the total chunks is %s' %str(flowTotalChunks))
                logging.info('in tmppath folder there is %s chunk'%str(total_files))
                if(flowTotalChunks==total_files):
                        cleantmp(tempPath)
        else:
                return 'UPLOAD'

def chunkOperationUtil(request,response):
	flowFileName=None
	flowChunkSize=None
	flowTotalSize=None
	flowChunkNumber=None
	if (request.method == 'GET'):
                flowChunkSize=str(request.args.get('flowChunkSize'))
                flowFileName=str(request.args.get('flowFilename'))
                flowTotalSize=str(request.args.get('flowTotalSize'))
                flowTotalChunks=str(request.args.get('flowTotalChunks'))
                flowChunkNumber=str(request.args.get('flowChunkNumber'))
                response.status="400"
	else:
                flowChunkNumber=str(request.form['flowChunkNumber'])
                flowChunkSize=str(request.form['flowChunkSize'])
                flowFileName=request.form['flowFilename']
                flowTotalSize=str(request.form['flowTotalSize'])
                flowTotalChunks=str(request.form['flowTotalChunks'])
                logging.info('file info: flowchuncknumber = %s; flowchunksize = %s; flowfilename = %s; flowtotalsize = %s;' % (flowChunkNumber, flowChunkSize, flowFileName, flowTotalSize))
                percorsotemporaneo=configimpl.config.get('fileconfig','tmppath')+flowFileName+folderlike
                logging.info('creo un percorso temporaneo')
                try:
                        os.mkdir(percorsotemporaneo)
                except:
                        logging.info("the foledr allready exists")
                chunk_file = str(flowFileName)+'.part'+str(flowChunkNumber)
                if os.path.exists(percorsotemporaneo+chunk_file)==False:
                        logging.info('temporary path %s ' % percorsotemporaneo)
                        chunkpath=percorsotemporaneo+chunk_file
                        try:
                                chunk=open(chunkpath,'wb')
                                chunk.write(request.files['file'].read())
                                chunk.close()
                                logging.info('file completed name is %s ' % chunkpath)
                        except:
                                logging.exception("message")
                else:
                        logging.info("file allready exist")
                response.status="200"
                return createFileFromChunk(flowFileName,flowChunkSize,flowTotalSize,percorsotemporaneo,flowTotalChunks)
