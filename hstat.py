from subprocess import Popen, PIPE
from flask import Flask, url_for, render_template

# create app
app = Flask(__name__)
app.config.from_object(__name__)

# variables for templates
def shell(cmd):
	proc = Popen(cmd, shell=True, stdout=PIPE, )
	stdout, stderr = proc.communicate()
	return stdout

@app.context_processor
def hostname():
	hostname = shell('hostname')
	return dict(hostname=hostname)

@app.context_processor
def dist():
	dist = shell('head -n1 /etc/issue').replace("\l", "").replace("\\n", "")
	return dict(dist=dist)

@app.context_processor
def linux():
	linux = shell('uname -srm')
	return dict(linux=linux)

@app.context_processor
def mem():
	mem = shell('grep MemTotal /proc/meminfo')
	return dict(mem=mem)

@app.context_processor
def uptime():
	uptime = shell('uptime')
	return dict(uptime=uptime)	

@app.context_processor
def cpu():
	cpu = []
	cpus = shell('grep \"model name\" /proc/cpuinfo').split("\n")
	for i in range(0, len(cpus)-1):
		c = cpus[i].replace("model name\t: ", "CPU" + str(i) + ": ")
		cpu.append(c)
	return dict(cpu=cpu)

@app.context_processor
def who():
	who = shell('w').split("\n")
	return dict(who=who)

@app.context_processor
def free():
	free = shell('free -m').split("\n")
	return dict(free=free)	

@app.context_processor
def sensors():
	_sensors = shell('sensors').split("\n")
	sensors = []
	for s in _sensors:
		if (len(s) > 0):
			sensors.append(s.decode('utf8'))
	return dict(sensors=sensors)

# routes
@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/live')
def live():
	return render_template('live.html')

# start
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)	