try:
    # import redis
    from fastapi import FastAPI, File, UploadFile
    from fastapi.middleware.cors import CORSMiddleware
    import pandas as pd
    import pdftables_api
    from xmlutils.xml2csv import xml2csv
    import os
    import sys
    import json

except Exception as e:
    print("Some modules are missing {}".format(e))


# init app      
app = FastAPI()


# cors added
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",

]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# init redis db
# cli=redis.Redis('localhost', 6379)
# debug == True
# test route
@app.get("/")
def test():
    return {
        "hello" : "world"
    }

# Main    
@app.post("/uploadfile")
async def check(file: UploadFile = File(...)):
 
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file.file)
        df_head = df.head(5)
        df_tail = df.tail(5)
        # cli.set("userId",str(df))
        head = df_head.to_json(orient='records')
        tail = df_tail.to_json(orient='records')
        head = eval(head)
        tail = eval(tail)
        return {
            "head":head,
            "tail":tail
        }

    
    # if file == txt
    elif file.filename.endswith('.txt'):
        read_file = pd.read_csv(file.file)
        read_file.to_csv('txt_to_csv.csv',index=None)
        df = pd.read_csv('txt_to_csv.csv')
        df_head = df.head(5)
        df_tail = df.tail(5)
        # cli.set("userId",str(df))
        head = df_head.to_json(orient='records')
        tail = df_tail.to_json(orient='records')
        head = eval(head)
        tail = eval(tail)
        return {
            "head":head,
            "tail":tail
        }
    
    # if file == pdf
    elif file.filename.endswith('.pdf'):
        c = pdftables_api.Client('upf6leimlx9u')
        c.csv(file.file, 'pdf_to_csv.csv')
        df = pd.read_csv('pdf_to_csv.csv')
        df_head = df.head(5)
        df_tail = df.tail(5)
        # cli.set("userId",str(df))
        head = df_head.to_json(orient='records')
        tail = df_tail.to_json(orient='records')
        head = eval(head)
        tail = eval(tail)
        return {
            "head":head,
            "tail":tail
        }
    
    # if file == xls
    elif file.filename.endswith('.xls'):
        data_xls = pd.read_excel(file.file, 'Sheet1', index_col=None)
        data_xls.to_csv('xls_to_csv.csv', encoding='utf-8')
        df = pd.read_csv('xls_to_csv.csv')
        df_head = df.head(5)
        df_tail = df.tail(5)
        # cli.set("userId",str(df))
        head = df_head.to_json(orient='records')
        tail = df_tail.to_json(orient='records')
        head = eval(head)
        tail = eval(tail)
        return {
            "head":head,
            "tail":tail
        }
    
    # if file == tsv
    elif file.filename.endswith('.tsv'):
        csv_file = pd.read_table(file.file,sep='\t')
        csv_file.to_csv('tsv_to_csv.csv',index=False)
        df = pd.read_csv('tsv_to_csv.csv')
        df_head = df.head(5)
        df_tail = df.tail(5)
        # cli.set("userId",str(df))
        head = df_head.to_json(orient='records')
        tail = df_tail.to_json(orient='records')
        head = eval(head)
        tail = eval(tail)
        return {
            "head":head,
            "tail":tail
        }
    
    # if file == xml
    elif file.filename.endswith('.xml'):
        converter = xml2csv(file.file, "xml_to_csv.csv", encoding="utf-8")
        converter.convert(tag="tag_value_defined_by_user")
        df = pd.read_csv('xml_to_csv.csv')
        df_head = df.head(5)
        df_tail = df.tail(5)
        # cli.set("userId",str(df))
        head = df_head.to_json(orient='records')
        tail = df_tail.to_json(orient='records')
        head = eval(head)
        tail = eval(tail)
        return {
            "head":head,
            "tail":tail
        }

    # if file == tf_record
    elif file.filename.endswith('.tf'):
        pass
        # content = txt_to_csv(file.read())
        # cli.set("uid",content)
        # return {"status":"done"}
    else:
        return {"error": "Enter a vaild file format"}


