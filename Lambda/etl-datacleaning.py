import json
import boto3 #Official python libray
import pandas as pd #Import pandas
import io #Access file
import os

s3 = boto3.client('s3') #Connection to s3

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        print(f"Processing for s3://{bucket}/{key} has began")

        response = s3.get_object(Bucket = bucket, Key = key)
        df = pd.read_csv(io.BytesIO(response['Body'].read()))

        d = {}
        lst = []
        teachers = []
        teacher_lookup = {}
        s_class = {}
        s_min = {}
        
        #columns and header names
        df.columns = df.columns.str.strip().str.lower()
        headers = ['name', 'grade', 'class', 'unlisted']
        
        #Collects all teacher data and puts it in teachers list
        for i in range(len(df)):
            if (df['role'].astype(str)[i] == 'Teacher'):
                teachers.append([df['name'][i].strip(), str(df['grade'][i]).strip(), df['class'][i].strip()])
        
        #Creation of dictionary to lower run time, is called within nested forloop to get specific val
        for teach in teachers:
            for sub in teach[2].split():
                teacher_lookup[(teach[1], sub)] = teach[0]
        
        #Creates dictionary list with appropriate lenght
        for head in headers:
            d[head] = {}
            lst.append([])
        
        #Makes a student dictionary for easy lookup with associated class and associated minutes
        for i in range(len(df)):
            if df.loc[i]['role'] == 'Student':
                s_class[df.loc[i]['name'].strip(), str(df.loc[i]['grade'])] = df.loc[i]['class'].split()
                s_min[df.loc[i]['name'].strip(), str(df.loc[i]['grade'])] = df.loc[i]['minutes'].split()
        
        #Creates a set seen to check if name has already been seen agmost students
        seen = set()
        for i in range(len(df)):
            if df.loc[i]['role'] == 'Student':
                
                #checks if name is in set then adds name and 
                name = df.loc[i]['name'].strip()
                if name not in seen:
                    seen.add(name)
                    
                    #Appends name and grade to respective place
                    lst[0].append(name)
                    lst[1].append(str(df.loc[i]['grade']).strip())
                    d['name'] = lst[0]
                    d['grade'] = lst[1]
                    
                    #Two sets, found and not found, adds teachers if found in combine and vice versa
                    f_combine = set()
                    nf_combine = set()
                    for k in range(len(s_class[df.loc[i]['name'].strip(), str(df.loc[i]['grade'])])):
                        
                        #Creates variables minutes and class to reduce complexity
                        mins = str(s_min[(df.loc[i]['name'].strip(), str(df.loc[i]['grade']))] [k])
                        clss = s_class[(df.loc[i]['name'].strip(), str(df.loc[i]['grade']))][k]
                        
                        #Found statement
                        found = teacher_lookup.get((str(df.loc[i]['grade']), clss))
                        
                        #In the event if no teacher is found
                        if found == None:
                            
                            #Checks if class is sped and adds to found
                            sped_teacher = teacher_lookup.get((str(df.loc[i]['grade']), 'Sped'))
                            if sped_teacher:
                                entry = f"{sped_teacher} {clss} {mins}"
                                if entry not in f_combine:
                                    f_combine.add(entry)
                                    
                            #If not Sped adds to not found
                            else:
                                entry = f"Not Listed {clss} {mins}"
                                if entry not in nf_combine:
                                    nf_combine.add(entry)
                                    
                        #If teacher is found adds to found           
                        if found != None:
                            entry = f"{found} {clss} {mins}"
                            if entry not in f_combine:
                                f_combine.add(entry)
                    
                    #Adds to respective list
                    lst[2].append(f_combine)
                    lst[3].append(nf_combine)
        
        d['class'] = [','.join(t) for t in lst[2]]
        d['unlisted'] = [','.join(t) for t in lst[3]]
        
        e_df = pd.DataFrame(d)


        output_key = f"processed/ETL_{os.path.basename(key)}"
        buffer = io.StringIO()
        e_df.to_csv(buffer, index = False)

        s3.put_object(Bucket = bucket, Key = output_key, Body = buffer.getvalue(), ContentType = 'text/csv')
        print(f"Processing for s3://{bucket}/{key} has ended")

        return {
            'statusCode': 200,
            'body': f"Cleaned file written to s3://{bucket}/{output_key}"
        }

    except Exception as e:
        print(e)
        raise(e)
    
