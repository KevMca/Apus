
from microWebSrv import MicroWebSrv
import IMU

# ----------------------------------------------------------------------------

# This is what is returned to the client if a GET for 192.168.0.137/test is 
# requested from the HTTP client
@MicroWebSrv.route('/test', 'GET')
def _httpHandlerTestGet(httpClient, httpResponse) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>TEST GET</title>
        </head>
        <body>
            <h1>TEST GET</h1>
            Client IP address = %s
            <br />
			<form action="/test" method="post" accept-charset="ISO-8859-1">
				First name: <input type="text" name="firstname"><br />
				Last name: <input type="text" name="lastname"><br />
				<input type="submit" value="Submit">
			</form>
        </body>
    </html>
	""" % httpClient.GetIPAddr() # httpClient. - extract information sent by client
	# Write response with the HTML code above using the httpResponse. object
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )

# This is what is run to the client if a POST is sent from 192.168.0.137/test
@MicroWebSrv.route('/test', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
	# Read the data sent from the client using the name from <input> tag
	formData  = httpClient.ReadRequestPostedFormData()
	firstname = formData["firstname"]
	lastname  = formData["lastname"]
	# Update content to reflect POST
	content   = """\
	<!DOCTYPE html>
	<html lang=en>
		<head>
			<meta charset="UTF-8" />
            <title>TEST POST</title>
        </head>
        <body>
            <h1>TEST POST</h1>
            Firstname = %s<br />
            Lastname = %s<br />
        </body>
    </html>
	""" % ( MicroWebSrv.HTMLEscape(firstname),
		    MicroWebSrv.HTMLEscape(lastname) )
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )


@MicroWebSrv.route('/edit/<index>')             # <IP>/edit/123           ->   args['index']=123
@MicroWebSrv.route('/edit/<index>/abc/<foo>')   # <IP>/edit/123/abc/bar   ->   args['index']=123  args['foo']='bar'
@MicroWebSrv.route('/edit')                     # <IP>/edit               ->   args={}
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>TEST EDIT</title>
        </head>
        <body>
	"""
	content += "<h1>EDIT item with {} variable arguments</h1>"\
		.format(len(args))
	
	if 'index' in args :
		content += "<p>index = {}</p>".format(args['index'])
	
	if 'foo' in args :
		content += "<p>foo = {}</p>".format(args['foo'])
	
	content += """
        </body>
    </html>
	"""
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )

# ----------------------------------------------------------------------------

def _acceptWebSocketCallback(webSocket, httpClient) :
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback

def _recvTextCallback(webSocket, msg) :
	print("WS RECV TEXT : %s" % msg)
	matrix = imu.orient()
	webSocket.SendText("%s" % matrix)

def _recvBinaryCallback(webSocket, data) :
	print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
	print("WS CLOSED")

# ----------------------------------------------------------------------------

#routeHandlers = [
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
#]

srv = MicroWebSrv(webPath='www')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= False
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start()

# ----------------------------------------------------------------------------
