from flask import Flask, jsonify, request,render_template
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv('.env')

DONORLEAD_API=os.environ.get('donorlead_api')
OPENAI_API=os.environ.get('openai_api')


app = Flask(__name__)


# d={"firstName": "Aadhaar", "middleName": "", "lastName": "Narang", "homeStreetAddress": "1270 block c2", "homeStreetAddress2": "palam vihar", "homeCity": "Gurgaon", "homeState": "CO", "homeZip": "122017", "spouseFirst": "", "spouseMiddle": "", "spouseLast": ""} 



@app.route('/')
def post_data():
    # d=request.data.decode("utf-8")
    # d=json.loads(d)
    
    # d['homeStreetAddress']=d['homeStreetAddress'].replace(' ','+')
    # d['homeStreetAddress2']=d['homeStreetAddress2'].replace(' ','+')
    # print(d)
    # # print(jsonify(request.data))
    # # print(type(request.data))
    
    # url=f'https://data.donorlead.net/v2.1?key={DONORLEAD_API}&firstName={d["firstName"]}&middleName={d["middleName"]}&lastName={d["lastName"]}&homeStreetAddress={d["homeStreetAddress"]}&homeStreetAddress2={d["homeStreetAddress2"]}&homeZip={d["homeZip"]}&homeState={d["homeState"]}&homeCity={d["homeCity"]}&spouseFirst={d["spouseFirst"]}&spouseMiddle={d["spouseMiddle"]}&spouseLast={d["spouseLast"]}&Detail=1&ProfileVersion=2'
    # response=requests.get(url)
    # response=response.json()
    # print("Received data:", response.json())
      # Print the data received

    # print(response.json)
    return render_template('form.html')



@app.route('/api/openai',methods=['POST'])
def getsummary():
    from openai import OpenAI
    # d=request.data.decode("utf-8")
    print(request.form)

    # print("fdnsjngjsngjfknlgsk")
    # print("fodnfsjonfodsn",d)
    # d=json.loads(d)
    
    homeStreetAddress=request.form['homeStreetAddress'].replace(' ','+')
    homeStreetAddress2=request.form['homeStreetAddress2'].replace(' ','+')
    # print("jkdfhjsfhjsdhlj",d)
    # print(jsonify(request.data))
    # print(type(request.data))
    
    url=f'https://data.donorlead.net/v2.1?key={DONORLEAD_API}&firstName={request.form["firstName"]}&middleName={request.form["middleName"]}&lastName={request.form["lastName"]}&homeStreetAddress={request.form["homeStreetAddress"]}&homeStreetAddress2={request.form["homeStreetAddress2"]}&homeZip={request.form["homeZip"]}&homeState={request.form["homeState"]}&homeCity={request.form["homeCity"]}&spouseFirst={request.form["spouseFirst"]}&spouseMiddle={request.form["spouseMiddle"]}&spouseLast={request.form["spouseLast"]}&clientID={request.form["ClientId"]}&Detail=1&ProfileVersion=2'
    response=requests.get(url)
    response=response.json()

    # print("fddsfsfsdfs",response)

  
      
    summaries={}


    client = OpenAI(api_key=OPENAI_API)
    # s=request.data.decode("utf-8")
    # s=json.loads(s)
    # print("fdsfsdfdskfsdkfsdk",s)
    completion = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
      # {"role": "system", "content": "You are a journalist, summarizing data in the form of an article describing the philanthrophic deeds of name of the person given. You need to describe the person's philanthrophic profile twice, one using chatgpt, and one using the context i am giving , Segregate the two descriptions with a line and be as descriptive as possibl"},
            {"role": "user", "content": f"Give the heading 'Using Chatgpt' ,Describe the philanthrophic profile of {request.form['firstName']} {request.form['lastName']} and {request.form['spouseFirst']} {request.form['spouseLast']} from {request.form['homeCity']}, {request.form['homeState']} . Use bullet points wherever necessary. Describe it as much as possible. If it is not possible to find the person, respond with sorry I cannot seem to find the particular person as per my knowledge. "},
      # {"role":"system","content":"Describe the business profile of the same person in the same manner as before."},
            
      # {"role":"user","content":f"As a second step, Describe the philanthrophic  profile of {request.form['firstName']} {request.form['lastName']} and {request.form['spouseFirst']} {request.form['spouseLast']} from {request.form['homeCity']}, {request.form['homeState']} using the context data that i am giving with this statement, include hard quantifiable facts with the dates wherever available,every entry in the context has a quality score or a score with it, only consider the data where this parameter is above 17.5 while describing the profile without including the score in the summary.Include the dollar value in each entry .I need a summary with structured bullet points . The context is : {response['individual']['Philanthropy']} . Explain each head with data from the context.  Include all the charitable givings from the context data in a concise and factual manner."} ,
      # {"role":"system","content":"Seggregate the two different profiles distincly with heading of the first description as chatgpt description and the second description with the context as donorsearch description."},


       # {"role":"user","content":f"After the generation of the profile leave 2-3 linespaces and generate a comprehensive summary of the json data provided :  {response['individual']['RealEstate']} and {response['individual']['Crunchbase']}  and {response['individual']['Philanthropy']}. Divide the summary generated without context and summary generated using provided json with strong line differentiation, Start the summary generated by the json file as 'the summary of the particular person from the data provided by DONORSEARCH is as follows:'. Properly format the generated summary as presentable to the reader. Get facts and figures from the context json data provided and generate a factual and descriptive summary for that particular person.summarize and explain each head with data from the json iin bullet points and be as comprehensive and detailed with figures as possible."}
      ],
      # response_format={"type":"json_object"}
    )
    print("..................................................................................................")
    print("Chatgpt summary",completion.choices[0].message.content)


    completion1 = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
      # {"role": "system", "content": "You are a journalist, summarizing data in the form of an article describing the philanthrophic deeds of name of the person given. You need to describe the person's philanthrophic profile twice, one using chatgpt, and one using the context i am giving , Segregate the two descriptions with a line and be as descriptive as possible. "},
            # {"role": "user", "content": f"Describe the philanthrophic profile of {request.form['firstName']} {request.form['lastName']} and {request.form['spouseFirst']} {request.form['spouseLast']} from {request.form['homeCity']}, {request.form['homeState']} . Use a bullet points and hard facts associated with the giving entry.  "},
      # {"role":"system","content":"Describe the business profile of the same person in the same manner as before."},
            
      {"role":"user","content":f"Give the heading 'Using the context' Describe the philanthrophic  profile of {request.form['firstName']} {request.form['lastName']} and {request.form['spouseFirst']} {request.form['spouseLast']} from {request.form['homeCity']}, {request.form['homeState']} using the context data that i am giving with this statement, include hard quantifiable facts with the dates wherever available,every entry in the context has a quality score or a score with it, only consider the data where this parameter is above 17.5 while describing the profile without including the score in the summary.Include the dollar value associated with each entry mandatorily.I need a presentable professional summary with structured bullet points mandatorily. The context is : {response['individual']['Philanthropy']} . Explain each head with data from the context.  Include all the charitable givings from the context data in a concise and factual manner.Use only utf-8 encoding in your description mandatorily."} ,
      # {"role":"system","content":"Seggregate the two different profiles distincly with heading of the first description as chatgpt description and the second description with the context as donorsearch description."},


       # {"role":"user","content":f"After the generation of the profile leave 2-3 linespaces and generate a comprehensive summary of the json data provided :  {response['individual']['RealEstate']} and {response['individual']['Crunchbase']}  and {response['individual']['Philanthropy']}. Divide the summary generated without context and summary generated using provided json with strong line differentiation, Start the summary generated by the json file as 'the summary of the particular person from the data provided by DONORSEARCH is as follows:'. Properly format the generated summary as presentable to the reader. Get facts and figures from the context json data provided and generate a factual and descriptive summary for that particular person.summarize and explain each head with data from the json iin bullet points and be as comprehensive and detailed with figures as possible."}
      ],
      # response_format={"type":"json_object"}
    )
    print("...........................................................................................")
    print("context based summary",str(completion1.choices[0].message.content))


    completion2 = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
      # {"role": "system", "content": "You are a journalist, summarizing data in the form of an article describing the philanthrophic deeds of name of the person given. You need to describe the person's philanthrophic profile twice, one using chatgpt, and one using the context i am giving , Segregate the two descriptions with a line and be as descriptive as possible. "},
            # {"role": "user", "content": f"Describe the philanthrophic profile of {request.form['firstName']} {request.form['lastName']} and {request.form['spouseFirst']} {request.form['spouseLast']} from {request.form['homeCity']}, {request.form['homeState']} . Use a bullet points and hard facts associated with the giving entry.  "},
      # {"role":"system","content":"Describe the business profile of the same person in the same manner as before."},
            
      {"role":"user","content":f" Describe the philanthrophic  profile of {request.form['firstName']} {request.form['lastName']} and {request.form['spouseFirst']} {request.form['spouseLast']} from {request.form['homeCity']}, {request.form['homeState']} using the context data that i am giving with this statement, include hard quantifiable facts with the dates wherever available,every entry in the context has a quality score or a score with it, only consider the data where this parameter is below 17.5 while describing the profile without including the score in the summary.Include the dollar value associated with each entry mandatorily.I need a presentable professional summary with structured bullet points mandatorily. The context is : {response['individual']['Philanthropy']} . Explain each head with data from the context.  Include all the charitable givings from the context data in a concise and factual manner.Use only utf-8 encoding in your description mandatorily and without exception."} ,
      # {"role":"system","content":"Seggregate the two different profiles distincly with heading of the first description as chatgpt description and the second description with the context as donorsearch description."},


       # {"role":"user","content":f"After the generation of the profile leave 2-3 linespaces and generate a comprehensive summary of the json data provided :  {response['individual']['RealEstate']} and {response['individual']['Crunchbase']}  and {response['individual']['Philanthropy']}. Divide the summary generated without context and summary generated using provided json with strong line differentiation, Start the summary generated by the json file as 'the summary of the particular person from the data provided by DONORSEARCH is as follows:'. Properly format the generated summary as presentable to the reader. Get facts and figures from the context json data provided and generate a factual and descriptive summary for that particular person.summarize and explain each head with data from the json iin bullet points and be as comprehensive and detailed with figures as possible."}
      ],
      # response_format={"type":"json_object"}
    )
    print("...........................................................................................")
    print("likely matches",str(completion2.choices[0].message.content))


    summaries['chatgpt_summary']=completion.choices[0].message.content
    summaries['donorsearch_context_summary']=completion1.choices[0].message.content
    summaries['less_likely_summary']=completion2.choices[0].message.content

    




    return jsonify(summaries)
  
   
        

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)



