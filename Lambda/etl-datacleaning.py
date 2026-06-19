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

        #columns and header names
        df.columns = df.columns.str.strip().str.lower()
        headers = ['name', 'grade', 'class']

        #Collects all teacher data and puts it in teachers list
        for i in range(len(df)):
            if (df['role'].astype(str)[i] == 'Teacher'):
                teachers.append([df['name'][i].strip(), str(df['grade'][i]).strip(), df['class'][i].strip()])

        #Creation of dictionary to lower run time (O(1)), is called within nested forloop to get specific val
        for teach in teachers:
            for sub in teach[2].split():
                teacher_lookup[(teach[1], sub)] = teach[0]

        for head in headers:
            d[head] = {}
            lst.append([])

        for i in range(len(df)):
            for col in df.columns:
                if df.loc[i]['role'] == 'Student':
                    
                    #adds each student name and appropriate data
                    if not df.loc[i]['name'].strip() in lst[0]:
                        lst[0].append(df.loc[i]['name'].strip())
                        lst[1].append(str(df.loc[i]['grade']).strip())
                        d['name'] = lst[0]
                        d['grade'] = lst[1]
                        
                        #Code for adding the appropriate class into the dictionary
                        combine = []
                        for j in range(len(df.loc[i]['class'].split())):
                            if not df.loc[i]['class'].split()[j] + str(df.loc[i]['minutes'].split()[j]) in combine:
                                found = teacher_lookup.get((str(df.loc[i]['grade']), df.loc[i]['class'].split()[j]))
                                if found != None:
                                    combine.append(found + " " + df.loc[i]['class'].split()[j] + " " + str(df.loc[i]['minutes'].split()[j]))
                        lst[2].append(combine)
                        
        d['class'] = [','.join(t) for t in lst[2]]
            
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
    
