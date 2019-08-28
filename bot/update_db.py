#!/usr/bin/python3
from html.parser import HTMLParser
from html.entities import name2codepoint
import os

class Parser(HTMLParser):
	lasttypef=""
	file=""
	started=False
	def handle_starttag(self, tag, attrs):
		if tag == "h2":
			# This is a new category
			print("Found A new category")
			self.lasttypef = "Category"
			self.started=True
		elif tag == "td" and self.started:
			print("found a problem")
			self.lasttypef="Problem"
		elif tag == "a" and self.lasttypef == "Problem":
			print("Found a problem link")
			f=open(self.file,"a+")
			for name,val in attrs:
				if name == "href":
					f.write("https://cses.fi/"+val)
			f.close()
			self.lasttypef="Problemname"
		elif tag == "small" and self.lasttypef == "Problem":
			self.lasttypef="Problemcount"

	def handle_endtag(self, tag):
		if tag == "td":
			self.lasttypef=""

	def handle_data(self, data):
		if self.lasttypef == "Category":
			self.file="problems/"+data+".txt"
			self.lasttypef=""
		elif self.lasttypef == "Problemname":
		#	f=open(self.file,"a+")
		#	f.write(" "+data)
		#	f.close()
			self.lasttypef="Problem"
		elif self.lasttypef == "Problemcount":
			f=open(self.file,"a+")
			f.write(" "+data+"\n")
			f.close()
			self.lasttypef="Problem"

def init():
	print("Deleting old files")
	os.system("rm -vf index.html")
	os.system("rm -vrf problems")
	print("Downloading the problems page")
	os.system("wget https://cses.fi/problemset/")
	os.system("mkdir -pv problems")

def parse():
	f=open("index.html", "r")
	cont=f.read()
	parser=Parser()
	parser.feed(cont)

def cleanup():
	os.system("rm -fv problems/General.txt")
	os.system("rm -fv index.html")

def main():
	init()
	parse()
	cleanup()

if __name__== "__main__":
	main()
