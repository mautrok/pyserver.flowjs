# pyserver.flowjs
A python's server to upload file with flow.js framework.
The example in 'sample' folder is taken by one of the
many presents into the flowjs packages distributed from 
https://github.com/flowjs/flow.js

## Requirements

After you have cloned the project type
>bower install

into the static folder to have the example working.

Into the main.py file, you can find two methods,
one is simply a redirection to the 'index.html' page into 
static folder, while the second one is the main method for 
the uploading example.

By only importing 'chunkOperationUtil' method from 'fileuploadutils'
class you'll have all you need to saving the uploaded files.

The framework saves the files inside the static folder into a sub folder
called 'upload', after having saved all the chunks inside the sub folder
'tmpdir'(inside static, same as the upload one), but this folder will be
always empty if everything have worked fine during the upload.

## Log

A lot of log messages were saved into the 'log' file into log folder,
under the root of the project, if you want to change the log file it's easy,
you'll have to go into the 'configimpl.py' file, where the file of log is sets.

## Config

Inside the folder 'conf' there are two files for windows or linux 
configuration (the second one it would be ok for mac too). Here you can change
the port for the example in flask, and the folder where to save the temporary file
or the final file too.

## For flask
It's really important to understand one thing about this framework.
Because of the functioning of flowjs the chunkOperationUtil
is structured to immediatly returned a reponse structured in
a way that flowjs continue to send chunks until every chunk
where uploaded, unless one of the uploaded chunk is fall in some
exception. So it's a good to send what 'chunkOperationUtil'
return, directly to the client side.

## In progress
While a setup.py is in progress it's really important to
write that this frameworks work only with Werkzeug 0.10
on windows. The latest version rise a winerror 10038.