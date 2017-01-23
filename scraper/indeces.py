
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer as wordnet
from nltk import pos_tag
import MySQLdb as mdb

#should pass in cursor
def getTitle(id,cur):
	#con = mdb.connect('localhost', 'root', 'Jiangft1213', 'stackoverflow')
	#cur = con.cursor()
	#cur.execute("DROP TABLE IF EXISTS question")
	#cur.execute("CREATE TABLE question (id int(5) PRIMARY KEY AUTO_INCREMENT, title varchar(200), link varchar(1500))")
	#cur.execute("INSERT INTO question (title,link) VALUES ('google is a good place to work','http://www.baidu.com') ")
	#con.commit()
 	cur.execute("select title from questions where id="+str(id)+";")
	return cur.fetchone()

#return {filename:[word,word,word],....}, should pass in cursor
def process_tuples(ids,cur):
	stops = set(stopwords.words("english"))
	#add new stop words
	#stops.update(('and','I','A','And','So','arnt','This','When','It','many','Many','so','cant','Yes','yes','No','no','These','these','Could','could','Would','would','be'))
	file_to_terms = {}
	#stemmer = PorterStemmer()
	lemmatiser = wordnet()
	morphy_tag = {'NN':'n','NNP':'n','JJ':'a','VB':'v','RB':'r','VBD':'v','VBP':'v','VBZ':'v','VBG':'v','VBN':'v','NNS':'n','JJS':'a','RBR':'r'}
	for id in ids:
		pattern = re.compile('[\W_]+')
		file_to_terms[id] = str(getTitle(id,cur));
		file_to_terms[id] = pattern.sub(' ',file_to_terms[id])
		re.sub(r'[\W_]+','', file_to_terms[id])
		word_list = file_to_terms[id].split()
		#print word_list
		word_list = [word for word in word_list if word not in stops]
		tagged_list = pos_tag(word_list)
		#print tagged_list
		for i in range(len(tagged_list)):
			#print morphy_tag[tagged_list[i][1]]
			try:
				word_list[i] = lemmatiser.lemmatize(tagged_list[i][0],pos = morphy_tag[tagged_list[i][1]])
			except:
				word_list[i] = lemmatiser.lemmatize(tagged_list[i][0])

		file_to_terms[id] = word_list
	return file_to_terms

#input [word,word,word] which is the return of process_file().values
#return {word:position}
def index_one_file(termlist):
	fileindex = {}
	for index, word in enumerate(termlist):
		if word in fileindex.keys():
			fileindex[word].append(index)
		else:
		 	fileindex[word] = [index]
	return fileindex

#input = {filename: [word1, word2, ...], ...}
#res = {filename: {word: [pos1, pos2, ...]}, ...}
def mk_indeces(termlists):
	indeces = {}
	for filename in termlists.keys():
		indeces[filename] = index_one_file(termlists[filename])
	return indeces

#input = {filename: {word: [pos1, pos2, ...], ... }}
#res = {word: {filename: [pos1, pos2]}, ...}, ...}
def fullIndex(redix):
	total_index = {}
	for filename in redix.keys():
		for word in redix[filename].keys():
			if word in total_index.keys():
				if filename in total_index[word].keys():
					total_index[word][filename] = total_index.extend(redix[filename][word][:])
				else:
					total_index[word][filename] = redix[filename][word]
			else:
				total_index[word] = {filename:redix[filename][word]}
	return total_index

def one_word_query(word, total_index):
	pattern = re.compile('[\W_]+')
	word = pattern.sub(' ',word)
	if word in total_index.keys():
		return [filename for filename in total_index[word].keys()]
	else:
		return []

def free_text_query(string,total_index):
	pattern = re.compile('[\W_]+')
	string = pattern.sub(' ',string)
	res = []
	for word in string.split():
		res += one_word_query(word,total_index)
	return list(set(res))

#return filename which contains the phrase
def phrase_query(string, total_index):
	pattern = re.compile('[\W_]+')
	string = pattern.sub(' ',string)
	listOffiles,res = [],[]
	for word in string.split():
		listOffiles.append(one_word_query(word,total_index))
	setted = set(listOffiles[0]).intersection(*listOffiles)
	for filename in setted:
		i = 0
		listofpos = []
		for word in string.split():
			listofpos.append(total_index[word][filename][:])
		for i in range(len(listofpos)):
			for pos_ind in range(len(listofpos[i])):
				listofpos[i][pos_ind] -= i
		if set(listofpos[0]).intersection(*listofpos):
			res.append(filename)
	return res


#print process_tuples([1])
#total_index = fullIndex(mk_indeces(process_tuples([1],cur)))
#print phrase_query('google is not',total_index)

#print getTitle(1)
