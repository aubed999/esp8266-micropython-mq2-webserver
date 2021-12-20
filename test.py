import utime
res=[]
Smoke=[]
LPG=[]
Methane=[]
Hydrogen=[]
def run():
  global res
  sensor = MQ2(pinData = 0, baseVoltage = 3.3)
  sensor.calibrate()
  print("Calibration completed")
  print("Base resistance:"+str(sensor._ro))
  while True:
    
    Smoke.append(float(sensor.readSmoke()))
    #print(str(Smoke)+'\n')
    
    #LPG.append(float(sensor.readLPG()))
    #print(str(LPG)+'\n')
    
    Methane.append(float(sensor.readMethane()))
    #print(str(Methane)+'\n')
    
    Hydrogen.append(float(sensor.readHydrogen()))
    #print(str(Hydrogen))
    
    #print(Smoke+"\n"+LPG+"\n"+Methane+"\n"+Hydrogen)
    res=[Smoke,Methane,Hydrogen]
    print(res)
    return 0
    #utime.sleep(10)

def webpage():
  run()
  
  html = """<html>
<head>
  <style>html{font-family:Verdana;}</style>
	
<script type="text/javascript">

var canvas ;
var context ;
var Val_max;
var Val_min;
var sections;
var xScale;
var yScale;
		// Values for the Data Plot, they can also be obtained from a external file
var Smoke =  """+str(res[0])+""";
var Methane =  """+str(res[1])+""";
var Hydrogen =  """+str(res[2])+""";  
function init() {
		// set these values for your data 
	sections = 6;
	Val_max = 50;
	Val_min = 0;
	var stepSize = 2;
	var columnSize = 25;
	var rowSize = 25;
	var margin = 2;
	var xAxis = [" ", "135", "275", "415", "555", "695","835"] 
		//
		
	canvas = document.getElementById("canvas");
	context = canvas.getContext("2d");
	context.fillStyle = "#0099ff"
	context.font = "20 pt Verdana"
	
	yScale = (canvas.height - columnSize - margin) / (Val_max - Val_min);
	xScale = (canvas.width - rowSize) / sections;
	
	context.strokeStyle="#009933"; // color of grid lines
	context.beginPath();
		// print Parameters on X axis, and grid lines on the graph
	for (i=1;i<=sections;i++) {
		var x = i * xScale;
		context.fillText(xAxis[i], x,columnSize - margin);
		context.moveTo(x, columnSize);
		context.lineTo(x, canvas.height - margin);
	}
		// print row header and draw horizontal grid lines
	var count =  0;
	for (scale=Val_max;scale>=Val_min;scale = scale - stepSize) {
		var y = columnSize + (yScale * count * stepSize); 
		context.fillText(scale, margin,y + margin);
		context.moveTo(rowSize,y)
		context.lineTo(canvas.width,y)
		count++;
	}
	context.stroke();
	
	context.translate(rowSize,canvas.height + Val_min * yScale);
	context.scale(1,-1 * yScale);
	
		// Color of each dataplot items
		
	context.strokeStyle="#FF0066";
	plotData(Smoke);
	context.strokeStyle="#9933FF";
	plotData(Methane);
	context.strokeStyle="#000";
	plotData(Hydrogen);
}

function plotData(dataSet) {
	context.beginPath();
	context.moveTo(0, dataSet[0]);
	for (i=1;i<sections;i++) {
		context.lineTo(i * xScale, dataSet[i]);
	}
	context.stroke();
}

</script>
<meta http-equiv="refresh" content="150" >
</head>

<body onLoad="init()">
<div align="center">
<h2>gas chart</h2>

<canvas id="canvas" height="400" width="650">
</canvas>
<br>
	<!--Legends for Dataplot -->
<span style="color:#FF0066"> Smoke </span> 
<span style="color:#9933FF"> Methane </span>
<span style="color:#000"> Hydrogen </span>
</div>
</body>
</html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('GET Rquest Content = %s' % request)
        response = webpage()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')







