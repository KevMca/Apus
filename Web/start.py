# Import microWebSrv and IMU libraries
import os, ujson
from microWebSrv import MicroWebSrv
#os.chdir("..")
#import orient
#os.chdir("Web")

# Web sockets
# ----------------------------------------------------------------------------
'''
# Web socket initialisation
def _acceptWebSocketCallback(webSocket, httpClient) :
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback

# Response to received
def _recvTextCallback(webSocket, msg) :
	print("WS RECV TEXT : %s" % msg)
	matrix = orient.getOrient()
	m_str = "{},{},{};{},{},{};{},{},{}".format(matrix.vect_x.vect[0], matrix.vect_x.vect[1], matrix.vect_x.vect[2], #east
		matrix.vect_y.vect[0], matrix.vect_y.vect[1], matrix.vect_y.vect[2], #north
		matrix.vect_z.vect[0], matrix.vect_z.vect[1], matrix.vect_z.vect[2]) #down
	webSocket.SendText("%s" % m_str)

# Print received message
def _recvBinaryCallback(webSocket, data) :
	print("WS RECV DATA : %s" % data)

# Web socket closure
def _closedCallback(webSocket) :
	print("WS CLOSED")
'''
@MicroWebSrv.route('/pid', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
	formData  = httpClient.ReadRequestContentAsJSON()
	jsonObj = ujson.loads(str(formData).replace("'", '"'))
	with open("www/pid.json", "w") as f:
		ujson.dump(jsonObj, f)
	#with open("www/pid.json", "r") as f:
    #	print(f.read())
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = None,
								  contentCharset = None,
								  content 		 = None )
# Start server
# ----------------------------------------------------------------------------

srv = MicroWebSrv(webPath='www')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= False
#srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start(threaded=True)

# ----------------------------------------------------------------------------
