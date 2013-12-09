#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import urllib2, re, time


def main() :
  global text_file
  global log_file
  
  log_file = open("Output.log", "a")
  
  log_file.write("Start of Thesaurus_Parser")
    
  start_time = time.time()
  
  thesaurus_parser()
   
  print("All Done")
  seconds = time.time() - start_time, "seconds"
  log_file.write("End of Thesaurus_Parser")
  log_file.write("Runtime is %s seconds"%seconds)
  log_file.close()

def thesaurus_parser() :

  alphabet_range = map(chr, range(97, 123))
  for each_letter in alphabet_range :
    alphabetical_link = "http://www.thesaurus.com/list/%s" %each_letter
    text_file = open("%s.txt"%each_letter, "a")
    text_file.write("Letter %s )"%each_letter )
    text_file.write("\n")
    text_file.write("\n")
    alphabetical_parser(alphabetical_link)
    text_file.close()
    print ("Parsed Letter %s" %each_letter)
    
    
def alphabetical_parser(alphabetical_link) :
  
  opener = urllib2.build_opener()
  opener.addheaders = [("User-agent", "Mozilla/5.0")]
  alphabetical_page = opener.open(alphabetical_link)
  
  alphabetical_soup = BeautifulSoup(alphabetical_page)
  
  for link in alphabetical_soup.find_all("a", "result_link"):
    section_link = link.get("href")
    section_parser(section_link)
   
def section_parser(section_link) :
  
  opener = urllib2.build_opener()
  opener.addheaders = [("User-agent", "Mozilla/5.0")] 
  section_page = opener.open(section_link)
  
  section_soup = BeautifulSoup(section_page)
  
  for link in section_soup.find_all("a", "result_link"):  
    word_link = link.get("href")
    text_file.write("%s"%word_link)
    text_file.write("\n")
    word_parser(word_link)

def word_parser(word_link) :

  opener = urllib2.build_opener()
  opener.addheaders = [("User-agent", "Mozilla/5.0")] 
  word_page = opener.open(word_link)
  word_soup = BeautifulSoup(word_page)  
  
  
  the_word = re.sub('http://thesaurus.com/browse/', '', str(word_link))
  
  word_check = the_word
  word_check_class = None
  word_extract = "Start"  
  
  while word_extract != None :
    
    word_extract = re.search(re.compile('<table cellspacing="5" class="the_content">.*?</table>', re.DOTALL), str(word_soup)).group()
    word_extract_soup = BeautifulSoup(word_extract)
    for link in word_extract_soup.find_all("a", "nud"):
      word_check = link.get_text()
    
    if word_check != the_word : break
    
    word_check_class = word_extract_soup.find_all("div", "adjHdg")
    if str(word_check_class) != "[]" : break
    
    parser_core(word_extract)
     
    word_soup = re.sub(re.compile('<table cellspacing="5" class="the_content">.*?</table>', re.DOTALL), '\n', str(word_soup), 1)
    
    word_extract_none = re.search(re.compile('<table cellspacing="5" class="the_content">.*?</table>', re.DOTALL), str(word_soup))
    if word_extract_none == None : break

def parser_core(word_extract) :
   
  parse_soup = BeautifulSoup(word_extract)
  
  text_file.write("Main Word:")
  text_file.write("\n")
  for word in parse_soup.find_all("b"):  
    text_file.write(word.get_text())
    text_file.write("\n")
  
  text_file.write('\n')
  
  text_file.write("Part of Speech:")
  text_file.write("\n")
  for word in parse_soup.find_all("i"):  
    text_file.write(word.get_text())
    text_file.write("\n")
    
  text_file.write("\n")  
  
  text_file.write("Definition:")
  text_file.write("\n")
  definition = re.search(re.compile('<td>(?!<).*</td>'), str(word_extract)).group()
  Definition_Soup = BeautifulSoup(definition)
  for word in Definition_Soup.find_all("td"):  
    text_file.write(word.get_text())
    text_file.write("\n")
    
  text_file.write("\n")  
  
  text_file.write("Synonyms:")
  text_file.write("\n")
  
  while True :
    check_syn = re.search(re.compile('<td><span>.*?</span></td>', re.DOTALL), str(word_extract))
    
    if check_syn == None :
      text_file.write("None")
      text_file.write("\n")
      break
      
    syn_ant = re.search(re.compile('<td><span>.*?</span></td>', re.DOTALL), str(word_extract)).group()
    synonyms_soup = BeautifulSoup(syn_ant)
    for word in synonyms_soup.find_all("span"):
      parser_synonyms = word.get_text()
      parser_synonyms = re.sub('^\n', '', str(parser_synonyms))
      parser_synonyms = re.sub(',[ \t]', ',\n', str(parser_synonyms))
      parser_synonyms = re.sub(',', '', str(parser_synonyms))
      text_file.write(parser_synonyms)
      text_file.write("\n")
      
    if True : break    
  
  text_file.write("\n")
  
  
  text_file.write("Antonyms:") 
  text_file.write("\n")
  syn_ant = re.sub(re.compile('<td><span>.*?</span></td>', re.DOTALL), '', str(syn_ant), 1)
  
  while True :
    check_ant = re.search(re.compile('<td><span>.*?</span></td>', re.DOTALL), str(syn_ant))
    
    if check_ant == None : 
      text_file.write("None")
      text_file.write("\n")
      text_file.write("\n")
      break
      
    syn_ant = re.search(re.compile('<td><span>.*?</span></td>', re.DOTALL), str(syn_ant)).group()
    antonyms_soup = BeautifulSoup(syn_ant)
    for word in antonyms_soup.find_all("span"):
      parser_antonyms = word.get_text()
      parser_antonyms = re.sub('^\n', '', str(parser_antonyms))
      parser_antonyms = re.sub(',[ \t]', ',\n', str(parser_antonyms))
      parser_antonyms = re.sub(',', '', str(parser_antonyms))
      text_file.write(parser_antonyms)
      text_file.write("\n")
      text_file.write("\n")
      
    if True : break
    
    
if __name__ == "__main__" :
  main()