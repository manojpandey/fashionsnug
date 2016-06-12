# -*- coding: utf-8 -*-
# @Author: amaneureka
# @Date:   2016-06-11 21:16:26
# @Last Modified by:   amaneureka
# @Last Modified time: 2016-06-12 09:51:01

import os
import cv2
import time
import json
import math
import requests
import httplib,urllib,base64

def ImageColor(imageData, x, y, width, height, fac):
	pixel = imageData[int(x+width/fac),int(y+height/fac)]
	# return (pixel[2]*255*255 + pixel[1] * 255 + pixel[0])
	return str("%02x%02x%02x")%(pixel[2], pixel[1], pixel[0])

faceApiHeader1 = {
 	'Content-Type':'application/json',
 	'Ocp-Apim-Subscription-Key':'fb33b35984114c82a6a29ebfa9fb6356'
}

faceApiParams=urllib.urlencode({
 	'returnFaceId': 'true',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'age,gender,facialHair,glasses,smile',
})

def register_api(imageUrl):
	global faceApiHeader1
	global faceApiParams
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
	result = {}
	result["facecolor"] = ImageColor(imageData, faceData["faceRectangle"]["left"], faceData["faceRectangle"]["top"], faceData["faceRectangle"]["width"], faceData["faceRectangle"]["height"], 2)
	result["age"] = int(faceData["faceAttributes"]["age"])
	result["gender"] = faceData["faceAttributes"]["gender"]
	result["beard"] = int(faceData["faceAttributes"]["facialHair"]["beard"] * 10)
	result["moustache"] = int(faceData["faceAttributes"]["facialHair"]["moustache"] * 10)
	result["eyecolor"] = ImageColor(imageData, faceData["faceLandmarks"]["pupilLeft"]["x"], faceData["faceLandmarks"]["pupilLeft"]["y"], 1.0, 1.0, 2)
	result["clothcolor"] = ImageColor(imageData, 0.0, 0.0, width, height, 1.5)
	result["height"] = int(math.ceil(faceData["faceLandmarks"]["noseTip"]["y"] - faceData["faceRectangle"]["top"]))
	result["bodyfit"] = "h2"
	json_data = []
	# json_data.append(result["url"])
 	json_data.append(result["facecolor"])
 	json_data.append(result["age"])
 	json_data.append(result["gender"])
 	json_data.append(result["beard"])
 	json_data.append(result["moustache"])
 	json_data.append(result["eyecolor"])
 	json_data.append(result["clothcolor"])
 	json_data.append(result["height"])
 	json_data.append(result["bodyfit"])
 	return json.dumps(json_data)

# register_api("https://avatars0.githubusercontent.com/u/4750240?v=3&s=460")
