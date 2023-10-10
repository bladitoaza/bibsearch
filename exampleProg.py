from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
import re
import pandas as pd

##Read table of algorithms
df= pd.read_excel('table.xlsx')

## Load configuration, read API key
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])

##Initialize variables
pop = []
table =pd.DataFrame()
table1 =pd.DataFrame()
#table_VOS['Authors']=''
#table_VOS['References']=''
##Search each algorithm from the imported excel table
for ind in df.index:
    algraw = df['Algorithm'][ind]
    alg=re.split('\(',algraw)

## Initialize doc search object using ScienceDirect and execute search,
#   retrieving all results
    doc_srch = ElsSearch('TITLE-ABS-KEY("travelling salesman problem" AND "'+alg[0]+ '") AND PUBYEAR > 1964 AND PUBYEAR < 2023','scopus')
   #doc_srch = ElsSearch('TITLE-ABS-KEY("travelling salesman problem" AND "genetic algorithm") AND PUBYEAR > 1964 AND PUBYEAR < 2023','scopus')
    doc_srch.execute(client, get_all = True)
    if 'error' in doc_srch.results:
        print(alg[0], " has ", str(0), "results.")
        pop.append(0)
    else:
        print (alg[0]," has ", doc_srch.tot_num_res, "results...Extracting")
        pop.append(doc_srch.tot_num_res)
        results_df=doc_srch.results_df
        for result in results_df.index:
            resultID=results_df['dc:identifier'][result]
            resultID = re.split(":",resultID)
            scp_doc = AbsDoc(scp_id = int(resultID[1]))

            if scp_doc.read(client):
            #Extracting authors
                if scp_doc.data['authors'] is not None:
                    authors= scp_doc.data['authors']['author']
                    autho=[]
                    authoID=[]
                    for au in authors:
                        autho.append(au['ce:indexed-name'])
                        authoID.append(au['@auid'])
                    autho=[", ".join(autho)]
                    authoID=[";".join(authoID)]
                else:
                    autho=None
                    authoID=None
            #Extracting references
                if scp_doc.data['item']['bibrecord']['tail'] is not None and 'reference' in scp_doc.data['item']['bibrecord']['tail']['bibliography']:
                    ref =[]
                    references= scp_doc.data['item']['bibrecord']['tail']['bibliography']['reference']
                    for indi in references:
                        ref.append(indi['ref-fulltext'])
                    refstring=["; ".join(ref)]
                else:
                     refstring=None

            #Extracting page numbers
                pages =results_df['prism:pageRange'][result]
                if pages is not None:
                    page_start=re.split('-',pages)[0]
                    page_start= re.sub(r'[^0-9]', '',page_start)
                    page_end=re.split('-',pages)[1]
                    page_end=re.sub(r'[^0-9]', '',page_end)
                    page_count = str(int(page_end)-int(page_start))
                else:
                    page_start=None
                    page_end=None
                    page_count=None
            #Extracting affiliaitons
                if 'affiliation' in scp_doc.data:
                    affiliations= scp_doc.data['affiliation']
                    affi=[]
                    if type(affiliations) is dict:
                        if affiliations['affilname'] is None:
                            name= ''
                        else:
                            name=affiliations['affilname']
                        if affiliations['affiliation-city'] is None:
                            city=''
                        else:
                            city=affiliations['affiliation-city']
                        if affiliations['affiliation-country'] is None:
                            country=''
                        else:
                            country=affiliations['affiliation-country']
                        affi =name+', '+city+', '+country
                    else:
                        for aff in affiliations:
                            if aff['affilname'] is None:
                                name= ''
                            else:
                                name=aff['affilname']
                            if aff['affiliation-city'] is None:
                                city=''
                            else:
                                city=aff['affiliation-city']
                            if aff['affiliation-country'] is None:
                                country=''
                            else:
                                country=aff['affiliation-country']
                            af =name+', '+city+', '+country
                            affi.append(af)
                        affi=["; ".join(affi)]
                else:
                    affi=None

            #Extracting keywords
                if scp_doc.data['authkeywords'] is not None:
                    keyw= scp_doc.data['authkeywords']['author-keyword']
                    if type(keyw) is dict:
                        keyword=keyw['$']
                    else:
                        keyword= []
                        for kw in keyw:
                            keyword.append(kw['$'])
                        keyword=["; ".join(keyword)]
                else:
                    keyword=None
            else:
                print ("Read document failed.")

            table_VOS=pd.DataFrame()
            table_VOS['Authors']=autho
            table_VOS['Author(s) ID']=authoID
            table_VOS['Title']=results_df['dc:title'][result]
            table_VOS['Year']=results_df['prism:coverDisplayDate'][result]
            table_VOS['Source title']=results_df['prism:publicationName'][result]
            table_VOS['Volume']=results_df['prism:volume'][result]
            table_VOS['Issue']=results_df['prism:issueIdentifier'][result]
            if 'article-number' in results_df:
                table_VOS['Art. No.']=results_df['article-number'][result]
            else:
                table_VOS['Art. No.']=None
            table_VOS['Page start']=page_start
            table_VOS['Page end']=page_end
            table_VOS['Page count']= page_count
            table_VOS['Cited by']=results_df['citedby-count'][result]
            table_VOS['DOI']=results_df['prism:doi'][result]
            table_VOS['Link']=results_df['link'][result]['self']
            table_VOS['Affiliations']=affi
            #table_VOS['Authors with affiliations']=
            table_VOS['Abstract']=scp_doc.data['coredata']['dc:description']
            table_VOS['Author Keywords']=keyword
            table_VOS['References']=refstring
            if 'dc:publisher' in scp_doc.data['coredata']:
                table_VOS['Publisher']=scp_doc.data['coredata']['dc:publisher']
            else:
                table_VOS['Publisher']=None
            table_VOS['Document Type']=scp_doc.data['coredata']['subtypeDescription']
            table= pd.concat([table,table_VOS], ignore_index = True)
		#Adding the name of algorithm
            list_alg = pd.DataFrame({'Algorithm':[alg[0]]})

            table_with_alg=pd.concat([list_alg, table_VOS], axis="columns")
            table1= pd.concat([table1,table_with_alg], ignore_index = True)
#Filling number of documents per algorithm
df['Impact'] = pop
#Saving documents searched
table.to_csv('scopus_search.csv',index=False)
table1.to_csv('scopus_Search_withnames.csv',index=False)
df.to_excel('table_filled.xlsx')