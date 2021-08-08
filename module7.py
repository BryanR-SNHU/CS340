#!/usr/bin/python
import sys
from pymongo import MongoClient
import datetime
import json
from bson import json_util
from collections import OrderedDict
import bottle
from bottle import route,run,request,post,abort,static_file

# HTML home page for graphical use
@route('/index',method='GET')
def index():
  page = """
  <!DOCTYPE html>
  <html>
  <body>
  <h4>Search for stock by name:</h4><br>
  <form action="none" method="GET" id="getStockForm">
  <input type="text" placeholder="stock name" name="stockname">
  <input type="submit" value="Search">
  </form><br>
  <h4>Search for stocks by industry:</h4><br>
  <form action="none" method="GET" id="getIndustryForm">
  <input type="text" placeholder="industry" name="industry">
  <input type="submit" value="Search">
  </form><br>
  <script type="text/javascript" src="module7.js"></script>

  </body>
  </html>"""

  return bottle.HTTPResponse(status=200, body=page)

# Create a new entry using a json request
@route('/stocks/api/v1.0/createStock',method='POST')
def apicreate():
  
  try:
    result = collection.insert_one(request.json)
  except Exception as e:
    return bottle.HTTPResponse(status=200, body=str(e) + "\n")
  
  return bottle.HTTPResponse(status=200, body="Document inserted with id " + result.inserted_id + "\n")

# Get a stock by the ticker symbol passed as final part of url
@route('/stocks/api/v1.0/getStock/<url>',method='GET')
def apiticker(url):
  ticker = url
  resultList = ""
  
  try:
    result = list( collection.find({"Ticker": ticker}))
  except Exception as e:
    return bottle.HTTPResponse(status=200, body=str(e) + "\n")
  
  if len(result) == 0:
    return bottle.HTTPResponse(status=404, body="No documents found\n")
  
  for item in result:
    resultList = resultList + str(item) + "\n"
  
  return bottle.HTTPResponse(status=200, body=resultList + "\n")

# Get a list of stocks by ticker by passing a high and low average as json
@route('/stocks/api/v1.0/getAverage',method=['GET','POST'])
def apiaverage():
  
  low = request.json.get('low')
  high = request.json.get('high')
  resultList = ""
  
  try:
    result = list( collection.find({"$and": [{"50-Day Simple Moving Average": {"$gt": float(low)}},{"50-Day Simple Moving Average": {"$lt": float(high)}}]},{"_id": 0,"Ticker": 1,"50-Day Simple Moving Average": 1}))
  except Exception as e:
    return bottle.HTTPResponse(status=200, body=str(e) + "\n")
  
  if len(result) == 0:
    return bottle.HTTPResponse(status=404, body="No documents found\n")
  
  for item in result:
    resultList = resultList + str(item) + "\n"
  
  return bottle.HTTPResponse(status=200, body=resultList + "\n")

# Get a list of stocks by ticker using the industry passed as last part of url
@route('/stocks/api/v1.0/getIndustry/<url>',method='GET')
def apiindustry(url):
  
  industry = url.replace("+"," ")
  resultList = ""
  
  try:
    result = list( collection.find({"Industry": industry},{"_id": 0,"Ticker": 1}))
  except Exception as e:
    return bottle.HTTPResponse(status=200, body=str(e) + "\n")
  
  if len(result) == 0:
    return bottle.HTTPResponse(status=404, body="No documents found\n")
  
  for item in result: 
    resultList = resultList + str(item) + "\n"
  
  return bottle.HTTPResponse(status=200, body=resultList + "\n")

# Update the volume of a stock by passing the ticker as the url and the volume in json
@route('/stocks/api/v1.0/updateStock/<url>',method=['GET','PUT'])
def apiupdate(url):
  
  ticker = url
  json_request = request.json
  #ticker = json_request.get('Ticker')
  volume = request.json.get('Volume')
  
  try:
    if not (int(volume) > 0):
      return bottle.HTTPResponse(status=200,body="Volume must be greater than 0\n")
  except ValueError:
    return bottle.HTTPResponse(status=200,body="Volume must be a number\n")
  
  try:
    updateResult = collection.updateOne({"Ticker": ticker},{"$set": {"Volume": volume}})
  except Exception as e:
    return bottle.HTTPResponse(status=200, body=str(e) + "\n")
  
  if updateResult.aknowledged:
    return bottle.HTTPResponse(status=201, body="Update Succesfull\n")
  else:
    return bottle.HTTPResponse(status=200, body="Update unsuccesfull\n")

# Delete a stock by passing the ticker as the end of the url
@route('/stocks/api/v1.0/deleteStock/<url>',method=['GET','DELETE'])
def apidelete(url):
  
  ticker = url
  
  try:
    deleteResult = collection.delete_many({"Ticker": ticker})
  except Exception as e:
    return bottle.HTTPResponse(status=200, body=str(e) + "\n")
  
  return bottle.HTTPResponse(status=200, body=str(deleteResult.deleted_count) + " documents deleted\n")

# Get the information for a variety of stocks by passing a json array
@route('/stocks/api/v1.0/stockReport',method='POST')
def stocksreport():
  
  resultList = ""
  tickers = request.json
  
  try:
    result = list( collection.find({"Ticker": {"$in": tickers}}))
  except Exception as e:
    return bottle.HTTPResponse(status=200, body=str(e) + "\n")
  
  if len(result) == 0:
    return bottle.HTTPResponse(status=404, body="No documents found\n")
  
  for item in result: 
    resultList = resultList + str(item) + "\n"
  
  return bottle.HTTPResponse(status=200, body=resultList + "\n")
  
  
  return

# Get the top 5 stocks in an industry by passing it as the end of the url
@route('/stocks/api/v1.0/industryReport/<url>',method='GET')
def industryreport(url):
  
  resultList = ""
  industry = url.replace("+"," ")
  pipeline = [{"$match": {"Industry": industry}},{"$sort": OrderedDict([("50-Day Simple Moving Average", -1)])},{"$limit": 5},{"$project": {"_id":0,"Ticker":1,"50-Day Simple Moving Average":1}}]
  
  try:
    result = list( collection.aggregate(pipeline))
  except Exception as e:
    return bottle.HTTPResponse(status=200, body=str(e) + "\n")
  
  if len(result) == 0:
    return bottle.HTTPResponse(status=404, body="No documents found\n")
  
  for item in result: 
    resultList = resultList + str(item) + "\n"
  
  return bottle.HTTPResponse(status=200, body=resultList + "\n")

# Get a list of outstanding shares in industries in the same sector as the company passed by url
@route('/stocks/api/v1.0/portfolio/<url>',method='GET')
def portfolio(url):
  
  resultList = ""
  company = url.replace("+"," ")
  
  try:
    firstResult = collection.find_one({"Company": company})
  except Exception as e:
    return bottle.HTTPResponse(status=200, body=str(e) + "\n")
  
  if firstResult == None:
    return bottle.HTTPResponse(status=404, body="No documents found\n")
  
  sector = firstResult.get('Sector')
  
  pipeline = [{"$match": {"Sector": sector}},{"$group": {"_id": "$Industry", "total outstanding shares": {"$sum": "$Shares Outstanding"}}},{"$sort": {"total outstanding shares": -1}}]
  
  result = list( collection.aggregate(pipeline))
  
  if len(result) == 0:
    return bottle.HTTPResponse(status=404, body="No documents found\n")
  
  for item in result: 
    resultList = resultList + str(item) + "\n"
  
  return bottle.HTTPResponse(status=200, body=resultList + "\n")

@route('/<filename:path>', name='static')
def serve_static(filename):
  return static_file(filename, root='./')

if __name__=='__main__':
  
  # Establish a connection to the MongoDB server.
  connection = MongoClient('localhost', 27017)
  db = connection['market']
  collection = db['stocks']
  
  # Start the Bottle server.
  run(host='localhost',port=8080)