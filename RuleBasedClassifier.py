import numpy as np
import pandas as pd
from sklearn.ensemble import VotingClassifier
import  pyodbc

def get_rules():
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=(localdb)\MSSQLLocalDB;"
                          "Database=ThesisSampleDB;"
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()
    query = "SELECT * FROM [dbo].[Apriori_Rules2] WHERE (CONSEQUENT = 'DENGUE NEXT_HIGH' or CONSEQUENT = 'DENGUE NEXT_LOW') and CONFIDENCE = 1 ORDER BY CONSEQUENT,NUM_ANTECEDENT DESC, LIFT DESC"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    temp = cursor.fetchall()
    for i in range(0, len(temp)):
        temp[i] = tuple(temp[i])
    apriori_rules = pd.DataFrame(temp, columns=columns)

    query = "SELECT * FROM [dbo].[FP_Rules] WHERE (CONSEQUENT = 'DENGUE NEXT_HIGH' or CONSEQUENT = 'DENGUE NEXT_LOW') AND (CONFIDENCE = 1 ) ORDER BY  CONSEQUENT,NUM_ANTECEDENT DESC "
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    temp = cursor.fetchall()
    for i in range(0, len(temp)):
        temp[i] = tuple(temp[i])
    fp_rules = pd.DataFrame(temp, columns=columns)

    return apriori_rules,fp_rules

def find_match(test_data,rules):
    answers = []
    listdata = test_data[test_data.columns[:-1]].values.tolist()
    temp = 0
    ans = False
    for data in listdata:
        for ant,con,n in zip(rules['Antecedent'],rules['Consequent'],rules['Num_Antecedent']):
            if(n > 1):
                antecedents = ant.split(',')
            else:
                antecedents = ant

            ans = set(antecedents) < set(list(data))
            #print("antece")
            #print(antecedents)
            #print("Data")
            #print(data)
            #print("------------")

            if(ans == True):
                answers.append(con)
                if(con == 'DENGUE NEXT_HIGH'):
                    temp+=1
                break
        if(ans == False):
            answers.append('DENGUE_LOW')
    print(temp)
    return answers

def check_accuracy(test_data_dengue,rule_based_answers):
    total = len(test_data_dengue)
    correct = 0
    tp = 0
    fp = 0
    tn = 0
    fn  = 0
    for x,y in zip(test_data_dengue,rule_based_answers):
        if(str(x) == str(y)):
            correct += 1
        if(str(x) == 'DENGUE NEXT_HIGH' and str(y) == 'DENGUE NEXT_HIGH'):
            tp += 1
        elif(str(x) == 'DENGUE NEXT_LOW' and str(y) == 'DENGUE NEXT_HIGH'):
            fp += 1
        elif(str(x) == 'DENGUE NEXT_LOW' and str(y) == 'DENGUE NEXT_LOW'):
            tn += 1
        elif(str(x) == 'DENGUE NEXT_HIGH' and str(y) == 'DENGUE NEXT_LOW'):
            fn += 1
    #return (float(correct/total) * 100)
    return (float((tp+tn)/(total ) * 100) )


def classfiy(test_data):

    apriori_rules,fp_rules = get_rules()
    #apriori_rules = apriori_rules[(apriori_rules['Consequent'] == 'DENGUE NEXT_HIGH') | (apriori_rules['Consequent']== 'DENGUE NEXT_LOW')]#& (apriori_rules['Confidence'] == 1)]
    #fp_rules = fp_rules[(fp_rules['Consequent'] == 'DENGUE NEXT_HIGH') | (fp_rules['Consequent']== 'DENGUE NEXT_LOW' )]# & (fp_rules['Confidence'] == 1)]
    #apriori_rules.sort_values(by=['Confidence'],ascending=[False])
    #apriori_rules.sort_values(by=['Num_Antecedent','Confidence'], ascending=[False,False],inplace=True)
    #apriori_rules.sort_values(by=['Num_Antecedent'], ascending=[False])
    #fp_rules =fp_rules.sort_values(by=['Num_Antecedent','Confidence'], ascending=[False,False])
    #fp_rules.sort_values(by=['Num_Antecedent'],ascending=[False])
    #print(fp_rules)
    #print(test_data[test_data.columns[:-1]])

    prediction_apriori = find_match(test_data,apriori_rules)
    prediction_fp = find_match(test_data,fp_rules)
    #print(prediction_apriori)
    print("---------------")
    #print(prediction_fp)
    print(test_data['dengue_next'])

    #print(test_data[:-1])
    print("APRIORI: " + str(check_accuracy(test_data['dengue_next'],prediction_apriori)))

    print("FP: " + str(check_accuracy(test_data['dengue_next'], prediction_fp)))








