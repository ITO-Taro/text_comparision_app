import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# import os


CONJUNC_ADJECT = "conjunctions_and_unnecessary_words.txt"
REPLACE = [':', '.', ',', '(', ')']
IRRELEVANT = 'remove_from_resume.txt'

class Ignore:

    def __init__(self):
        self.ignore = self.conjunc_adject_list()
    
    def conjunc_adject_list(self):
        '''
        reads the file that contains words to be removed and turns them into a list
        returns a list of those words
        '''

        with open(CONJUNC_ADJECT, 'r') as file:
            data = file.readlines()
            data = data[0].lower().split(',')
            return data

class JobDescriptionCleaner(Ignore):
    '''
    1. set the working directory path
    2. specify the file that contains words to remove from job description
    3. set the symbols/characters to be removed from texts
    4. specify the file that contains unncessary words to be removed from the resume (e.g., 'Location', 'Company')
    \ to improve the accuracy of match score
    5. set the folder where job descriptions are stored
    '''

    def __init__(self, description):
        '''
        1. reads the file that contains words to be removed and turns them into a list
        2. asks for the input file path (i.e., the job description)
        3. clean the job description and turns it into a list of words
        4. count how many times each word appeared in the job description
        '''
        super().__init__()
        self.ignore = Ignore().ignore
        self.infile = description
        self.cleaned_description = self.remove_conjunc_adject(self.infile)
        self.word_counted_description = self.count_words(self.cleaned_description)
        # self.output_file = self.outfile()
        # self.processed_description = self.go_no_go(self.word_counted_description, self.output_file)

        # self.out(self.word_counted_description)

    # def conjunc_adject_list(self):
    #     '''
    #     reads the file that contains words to be removed and turns them into a list
    #     returns a list of those words
    #     '''
    #     # file_path = self.PATH+self.CONJUNC_ADJECT
    #     with open(CONJUNC_ADJECT, 'r') as file:
    #         data = file.readlines()
    #         data = data[0].lower().split(',')
    #         return data
    
    def remove_conjunc_adject(self, input_file):
        '''
        removes the unnecessary words from the text data
        param: text file
        return: list of words 
        '''
        res = []
        with open(input_file, 'r') as infile:
            in_data = infile.readline().splitlines()
            while in_data:
                if in_data != ['']:
                    in_data = in_data[0].replace('/', ' ').lower().split()
                    for word in in_data:
                        word = self.__chr_cleaner(word)
                        if not word in self.ignore:
                            res.append(word)
                in_data = infile.readline().splitlines()
        return res
    
    def count_words(self, data):
        '''
        counts how many times each word in a list appeared in the list passed
        returns the result in dict format (e.g., {'collaboration': 3})\
            which is sorted by counts in descnding order
        '''
        res = dict()
        for word in data:
            if word in res.keys():
                res[word] += 1
            else:
                res[word] = 1
        res = sorted(res.items(), key=lambda x: x[1], reverse=True)
        return res

    # def export(self, infile, outfile):
    #     '''
    #     writes the input data out to a specified file
    #     '''
    #     with open(self.PATH+outfile, 'a') as file:
    #         for word in infile:
    #             file.write(f"{word[0]}: {word[1]}'\n")
    
    def __chr_cleaner(self, word):
        '''
        replaces the symbols/characters deemed unnecessary
        '''
        return ''.join([i for i in word if i not in REPLACE]).lower()
    
    def out(self, data):
        return data
    
    # def __infile(self):
    #     '''
    #     user specifies the input job description file
    #     '''
    #     input_file =  input("Load the file to read from: ")
    #     res = self.DESCRIPTION+input_file
    #     return res
    
    # def outfile(self):
    #     '''
    #     user specifies the file to write to
    #     '''
    #     return input("Specify the file to write to: ")
    
    # def __export(self, outfile, res=None):
    #     '''
    #     ask user for confirmation to write
    #     returns the answer in string
    #     '''
    #     confirmation = input(f"Export to the {outfile} now? (Y or no): ")
    #     if confirmation == 'Y' or 'y':
    #         res = True
    #     else:
    #         res = False
    #     return res
    
    # def go_no_go(self, infile, outfile):
    #     '''
    #     If the user confirms, the export function will be called.
    #     If NOT, the process terminates itself
    #     '''
    #     if self.__export(outfile):
    #         self.export(infile, outfile)
    #     else:
    #         return

class ResumeCleaner(JobDescriptionCleaner):

    def __init__(self, resume):
        '''
        1. asks to specify the path to resume file
        2. creates a list of irrelevant words identified beforehand
        3. use the list of irrelevant words and the list of conjunctions\
            to clean the resume
        4. count how many times each word in resume appeared 
        '''
        # super().__init__()
        self.ignore = Ignore().ignore
        self.resume = resume
        self.remove_words = self.__unnecessaries_list()
        self.cleaned_resume = self.remove_conjunc_adject(self.resume)
        self.very_clean_resume = self.finalized_resume()
        self.word_counted_resume = self.count_words(self.very_clean_resume)
        # self.output_file = self.outfile()
        # self.processed_resume = self.go_no_go(self.word_counted_resume, self.output_file)
        # self.out(self.word_counted_resume)
    
    def finalized_resume(self):
        '''
        param: list of words found in resume, AFTER the conjunction words are removed
        remove irrelevant words from the resume
        '''
        res = []
        for word in self.cleaned_resume:
            word = word.lower()
            if not word in self.remove_words:
                res.append(word)
        return res

    def __unnecessaries_list(self):
        '''
        read the file IRRELEVANT and turns the content into a list
        '''
        # file_path = self.PATH+self.IRRELEVANT
        with open(IRRELEVANT, 'r') as file:
            words = file.readlines()
            words = words[0].lower().split(',')
            return words

    # def __resume_reader(self):
    #     '''
    #     asks user to specify the path to resume
    #     '''
    #     file = input("Load you resume here: ")
    #     return file

class DocComparision(ResumeCleaner):
    '''
    the primary objectives of this class are:\
        1. create a pd.DataFrame of all words appered in job description and resume\
            and the counts
        2. use sklearn package to compares the two lists of words\
            were extracted from resume and job description\
                calculates a number to represent the extent\
                    to which the two data under analysys\
                        resemble one another
    '''

    def __init__(self, resume, description):
        '''
        1. convert job description words & counts in tupel back into a key-value pair object
        2. convert resume words & counts in tupel back into a key-value pair object 
        3. consolidates the two key-value pair objects created in above into one\
            that can be processed by pandas
        4. create a pd.DataFrame with consolidated data
        5. converts each list of words (resume and job description)\
            into a long string of words, so that they can be processed for similarities\
                by sklearn
        6. calculate how similar the two data are
        7. ask user to specify the file path to write all the result to
        8. writes the result

        '''
        # super().__init__()
        descript = JobDescriptionCleaner(description)
        resm = ResumeCleaner(resume)
        self.employers_words = self.__tup_to_dict(descript.word_counted_description)
        self.my_words = self.__tup_to_dict(resm.word_counted_resume)
        self.processed_data = self.__check_counts(self.employers_words, self.my_words)
        self.df = self.to_dataframe(self.processed_data)
        self.resume_text = ' '.join(resm.very_clean_resume)
        self.description_text = ' '.join(descript.cleaned_description)
        self.match_score = self.__match_score(self.description_text, self.resume_text)
        # self.output_file = self.outfile()
        # self.write_output(self.output_file)

        # self.out(self.__finalized_data())
        self.result = self.__finalized_data()
        
    
    def to_dataframe(self, data_dict):
        '''
        create pd.DataFrame from consolidated dict object
        '''
        df = pd.DataFrame.from_dict({(k): data_dict[k] for k in data_dict.keys() for v in data_dict[k].keys()}, orient='index')
        df.sort_values(by='employer', inplace=True, ascending=False)
        return df
    
    # def write_output(self, outfile):
    #     '''
    #     write finalized data to file specified by user
    #     '''
    #     data = self.__finalized_data()
    #     with open(self.PATH+"Comparison_Outputs/"+outfile, 'w') as file:
    #         file.write(data)

            
    def __check_counts(self, employers_dict, my_dict):
        '''
        Compares dict_1 and dict_2 and writes a new dict
        param: 2 dictionaries
        return: the new dict (keys == words
        \ vals == {'employer: num, 'me': num})
        '''
        res = dict()
        emp_words = employers_dict.keys()
        my_words = my_dict.keys()
        for word in my_dict.keys():
            if word in emp_words:
                res[word] = {'employer': employers_dict[word], 'me': my_dict[word]}
            else:
                res[word] = {'employer': 0, 'me': my_dict[word]}
        
        for word in employers_dict.keys():
            if not word in my_words:
                res[word] = {'employer': employers_dict[word], 'me': 0}
        
        return res
                
    def __tup_to_dict(self, tup_lst):
        '''
        turns tutple into dict object
        '''
        res = dict()
        for tup in tup_lst:
            res[tup[0]] = tup[1]
        return res
    
    def __match_score(self, description, resume):
        '''
        calculate similarity between two objects
        '''
        description_resume_text = [description, resume]
        cv = CountVectorizer()
        comparison_matrix = cv.fit_transform(description_resume_text)
        res = round(cosine_similarity(comparison_matrix)[0][1]*100, 4)
        return res
    
    def __finalized_data(self):
        '''
        returns string of text that includes similarity score in percentage and all data in the pd.DataFrame
        '''
        res = dict()
        res["score"] = f"The similarity between resume and job description is: {self.match_score}%"
        # df = self.df.to_string(header=True, index=True)
        # res = score+'\n\n'+df
        res["df"] = self.df
        
        return res
    
    # def __str__(self):
    #     return self.__finalized_data()


# LinkedIn_link https://www.linkedin.com/pulse/does-my-resume-look-like-job-description-taro-ito