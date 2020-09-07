import requests as r
from bs4 import BeautifulSoup
import os

class mangatoon:

	def __init__(self):
		self.get=r.get
		self.url1="https://mangatoon.mobi/id/search?word="
		self.url2="https://mangatoon.mobi"

	def search(self,keywords):
		try:
			r=self.get(self.url1+keywords)
			soup=BeautifulSoup(r.content, "html.parser")
			find=soup.find("div", class_="recommend-comics-title")
			print(find.text)
		except AttributeError:
			print("Tidak menemukan hasil")
	#finding links from keywords
		find_link=soup.find_all("a", href=True)
		for links in find_link:
			if "/id/detail" in links["href"]:
				get=self.get(self.url2+links["href"])
				soup_link=BeautifulSoup(get.content, "html.parser")
				find_desc=soup_link.find_all("meta")
				for tags in find_desc:
					if "name" in tags.attrs.keys() and tags.attrs["name"].strip().lower() in ["description"]:
						print('\n'+tags.attrs["content"])
				if input("\nLanjut cerita ke episode? ") =="ya":
					episod=self.get(self.url2+links["href"]+"/episodes").text
					soup_episod=BeautifulSoup(episod, "html.parser")
					f=open("episodes.txt","w")
					find_episod=soup_episod.find_all("a", href=True)
					for episodes in find_episod:
						if "/id/watch" in episodes["href"]:
							f.write(episodes["href"]+'\n')
					f.close()
				break

	def episodes(self):
		f=open("episodes.txt","r").readlines()
		print("Total episode:",len(f))
		for baca in f:
			reading=baca.replace("\n","")
			os.system("xdg-open "+self.url2+reading)
			break

mangatoon().search(keywords=input("keywords: "))
mangatoon().episodes()
