# Import microWebSrv and IMU libraries
import os, ujson
from microWebSrv import MicroWebSrv

# Web sockets
# ----------------------------------------------------------------------------

# Web socket initialisation
def _acceptWebSocketCallback(webSocket, httpClient) :
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback

# Response to received
def _recvTextCallback(webSocket, msg) :
	sendStr = "1.00"
	webSocket.SendText("%s" % sendStr)

# Print received message
def _recvBinaryCallback(webSocket, data) :
	print("WS RECV DATA : %s" % data)

# Web socket closure
def _closedCallback(webSocket) :
	print("WS CLOSED")


# Http
# ----------------------------------------------------------------------------
@MicroWebSrv.route('/pid', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
	formData  = httpClient.ReadRequestContentAsJSON()
	jsonObj = ujson.loads(str(formData).replace("'", '"'))
	with open("/Web/www/pid.json", "w") as f:
		ujson.dump(jsonObj, f)
	#with open("www/pid.json", "r") as f:
    #	print(f.read())
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = None,
								  contentCharset = None,
								  content 		 = None )

@MicroWebSrv.route('/autre', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
	formData  = httpClient.ReadRequestContentAsJSON()
	jsonObj = ujson.loads(str(formData).replace("'", '"'))
	with open("/Web/www/autre.json", "w") as f:
		ujson.dump(jsonObj, f)
	#with open("www/pid.json", "r") as f:
    #	print(f.read())
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = None,
								  contentCharset = None,
								  content 		 = None )
# Start server
# ----------------------------------------------------------------------------

srv = MicroWebSrv(webPath='Web/www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= False
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start(threaded=True)

# ----------------------------------------------------------------------------
