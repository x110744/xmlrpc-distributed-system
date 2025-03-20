from xmlrpc.server import SimpleXMLRPCServer
import wikipedia

server = SimpleXMLRPCServer(("localhost", 1234))

def d2xml(d):
	# converts dictionary into formatted xml string
	r = "<data>"
	for t in d: # for each topic
		r = r + f"\n\t<topic name=\"{t}\">"
		for n in d[t]: # for each note
			r = r + f"\n\t\t<note name=\"{n}\">"
			r = r + f"\n\t\t\t<text>{d[t][n][0]}</text>"
			r = r + f"\n\t\t\t<timestamp>{d[t][n][1]}</timestamp>"
			r = r + f"\n\t\t</note>"
		r = r + f"\n\t</topic>"
	return r+"\n</data>"

def xml2d():
	# converts xml into a dictionary
	r = {}
	topic=''
	note=''
	text=''
	time=''
	try:
		with open('mockdb', 'r') as f:
			for l in f:
				if(not l or l.strip()=="<data>" or l.strip()[0:2]=="</"):

					continue
				elif(l[0:3]=="\t<t"):
					topic = l[14:14+l[14:].find("\"")]
				elif(l[0:4]=="\t\t<n"):
					note = l[14:14+l[14:].find("\"")]
				elif(l[0:6]=="\t\t\t<te"):
					text = l[9:9+l[9:].find("</text>\n")]
				elif(l[0:6]=="\t\t\t<ti"):
					time = l[14:14+l[14:].find("<")]
					# add to dictionary
					r[topic]={}
					r[topic][note] = (text, time)
	except:
		print("No database (\"mockdb\" file) found")
	return r

data = xml2d()

def save(topic, note, text, date):
	def save_help(t, n, x, d):
		data[t][n] = (x, d)
		with open('mockdb', 'w') as f:
			f.write(d2xml(data))
			return 0
	for t in data:
		if topic in t:
			# append note to existing topic
			return save_help(topic, note, text, date)
	# create new topic
	data[topic] = {}
	return save_help(topic, note, text, date)

def list_topics():
	# returns a list of all topic names
	r = []
	for i in data:
		r.append(i)
	return r

def list_notes(t):
	# returns a list of note names for a given topic
	r = []
	if t not in data:
		return r
	for i in data[t]:
		r.append(i)
	return r

def read_note(t, n):
	# returns the note children
	if t not in data or n not in data[t]:
		return ("", "")
	return data[t][n]

def test():
	return 0

def get_summary(article):
	r = wikipedia.summary(article, sentences=1)
	return r

server.register_function(save, "save")
server.register_function(list_topics, "list_topics")
server.register_function(list_notes, "list_notes")
server.register_function(read_note, "read_note")
server.register_function(get_summary, "get_summary")
server.register_function(test, "test")

server.serve_forever()
