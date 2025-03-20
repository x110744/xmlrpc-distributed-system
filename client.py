from xmlrpc.client import ServerProxy, Fault
from datetime import datetime

def print_menu():
	print("1. New note")
	print("2. Browse topics")
	print("3. Wikipedia search")
	print("0. Exit")

def new_note(server):
	topic_name = input("Topic name: ")
	note_name = input("Note name: ")
	note_text = input("Note text: ")
	timestamp = datetime.utcnow().strftime("%d/%m/%Y - %H:%M:%S")
	try:
		server.save(topic_name, note_name, note_text, timestamp)
	except Fault as f:
		# print(f)
		print("Server error, data not saved.")

def browse(server):
	try:
		topics_list = server.list_topics()
	except:
		print("Disconnected from server unexpectedly")
		return 1
	if(topics_list==[]):
		print("The notebook is empty. Start adding notes!")
		return 0
	for i in topics_list:
		print(i)
	print("Exit")
	topic = input("Select a topic: ")
	if(topic.lower()=="exit"):
		return 0
	try:
		notes_list = server.list_notes(topic)
	except:
		print("Disconnected from server unexpectedly")
		return 1
	if(notes_list==[]):
		print("There are no notes on this topic")
		return 0
	for i in notes_list:
		print(i)
	print("Exit")
	note = input("Select a note: ")
	if(note.lower()=="exit"):
		return 0
	try:
		note_content = server.read_note(topic, note)
		if(note_content==["",""]):
			print(f"No note \"{note}\" in topic \"{topic}\".")
			return 0
		print("\n"+topic + " -> " + note)
	except:
		print("Disconnected from server unexpectedly")
		return 1
	print("@ "+ note_content[1]+"\n")
	print(note_content[0]+"\n\n")

def wiki(server):
	selection = input("Search for an article: ")
	try:
		summary = server.get_summary(selection)
		print(summary)
	except:	
		print("Could not find an article based on your query.")
		return 1
	add = input("Do you want to add the result to a topic? (y/N) ")
	if(add.lower()=="y"):
		topic = input("Which topic? ")
		timestamp=datetime.utcnow().strftime("%d/%m/%Y - %H:%M:%S")
		try:
			server.save(topic, selection, summary, timestamp)
		except Fault as f:
			# print(f)
			print("Server error, data not saved.")
	return 0

s = ServerProxy("http://localhost:1234")

if __name__ == "__main__":
	while(True):
		try:
			s.test()
		except:
			retry = input("Server unreachable. Retry? (y/N) ")
			if(retry.lower()=="y"):
				continue
			break
		print_menu()
		opt = input("Enter command: ")
		if(opt=="0"):
			print("Quitting app...")
			break
		elif(opt=="1"):
			new_note(s)
		elif(opt=="2"):
			browse(s)
		elif(opt=="3"):
			wiki(s)
		else:
			print(opt + " not recognized.")

