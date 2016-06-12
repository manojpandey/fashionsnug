# -*- coding: utf-8 -*-
# @Author: amaneureka
# @Date:   2016-06-11 21:16:26
# @Last Modified by:   amaneureka
# @Last Modified time: 2016-06-12 09:39:31

import os
import cv2
import time
import json
import math
import requests
import httplib,urllib,base64

def ImageColor(imageData, x, y, width, height, fac):
	pixel = imageData[int(x+width/fac),int(y+height/fac)]
	return (pixel[2]*255*255 + pixel[1] * 255 + pixel[0])

faceApiHeader1 = {
 	'Content-Type':'application/json',
 	'Ocp-Apim-Subscription-Key':'fb33b35984114c82a6a29ebfa9fb6356'
}

faceApiParams=urllib.urlencode({
 	'returnFaceId': 'true',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'age,gender,facialHair,glasses,smile',
})

def call_api(imageUrl):
	global faceApiHeader1
	global faceApiParams
#imageUrl = "http://www.bowersoft.in/Mytra-Images/menShirts0.jpg"
	requestBody = {
  		'url' : imageUrl
 	}
	urllib.urlretrieve(imageUrl, "temp.jpg")
	connection = httplib.HTTPSConnection('api.projectoxford.ai')
	connection.request("POST", "/face/v1.0/detect?%s" % faceApiParams, str(requestBody), faceApiHeader1)
	response = connection.getresponse()
	faceData = json.loads(response.read())[0]
	# ---
	imageData = cv2.imread("temp.jpg")
	height, width = imageData.shape[:2]
	values = []
	final_data = {}
	finalFile = open("final.json", "r")
	trained_data = json.load(finalFile)
	for index in range(0, 1500):
		result = {}
		model = trained_data["values"][index]["row"]
		confidence = 0.0
		result["url"] = str("http://www.bowersoft.in/Mytra-Images/menShirts" + str(index) + ".jpg")
		result["facecolor"] = ImageColor(imageData, faceData["faceRectangle"]["left"], faceData["faceRectangle"]["top"], faceData["faceRectangle"]["width"], faceData["faceRectangle"]["height"], 2)
		confidence = abs(result["facecolor"] - model[1])/model[1]
		result["age"] = int(faceData["faceAttributes"]["age"])
		confidence = confidence + abs(result["age"] - model[2])/model[2]
		result["gender"] = faceData["faceAttributes"]["gender"]
		result["beard"] = int(faceData["faceAttributes"]["facialHair"]["beard"] * 10)
		confidence = confidence + abs(result["beard"] - model[4])
		result["moustache"] = int(faceData["faceAttributes"]["facialHair"]["moustache"] * 10)
		confidence = confidence + abs(result["moustache"] - model[5])
		result["eyecolor"] = ImageColor(imageData, faceData["faceLandmarks"]["pupilLeft"]["x"], faceData["faceLandmarks"]["pupilLeft"]["y"], 1.0, 1.0, 2)
		confidence = confidence + abs(result["eyecolor"] - model[6])/model[6]
		result["clothcolor"] = ImageColor(imageData, 0.0, 0.0, width, height, 1.5)
		confidence = confidence + abs(result["clothcolor"] - model[7])/model[7]
		result["height"] = int(math.ceil(faceData["faceLandmarks"]["noseTip"]["y"] - faceData["faceRectangle"]["top"]))
		confidence = confidence + abs(result["height"] - model[8])/model[8]
		result["bodyfit"] = "h2"
		result["confidence"] = 1.0 - confidence
		json_data = []
	 	json_data.append(result["url"])
	 	json_data.append(result["confidence"])
	 	row = {}
	 	row["row"] = json_data
	 	values.append(row)
	final_data["values"] = values
	fucking_data = json.dumps(final_data)
	fucking_header = open("header.json", "r")
	fucking_target = open("api.json", 'wb')
	fucking_target.write(fucking_header.read())
	fucking_target.write(fucking_data[1:-1])
	fucking_target.write("}")
	return fucking_data

# call_api("https://avatars0.githubusercontent.com/u/4750240?v=3&s=460")
