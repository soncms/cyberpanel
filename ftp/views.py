# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import json
from django.shortcuts import render,redirect
from django.http import HttpResponse
from models import Users
from loginSystem.models import Administrator
import plogical.CyberCPLogFileWriter as logging
from loginSystem.views import loadLoginPage
from websiteFunctions.models import Websites
import subprocess
from plogical.virtualHostUtilities import virtualHostUtilities
import shlex
from plogical.ftpUtilities import FTPUtilities
import os
from plogical.acl import ACLManager
# Create your views here.

def loadFTPHome(request):
    try:
        val = request.session['userID']
        return render(request,'ftp/index.html')
    except KeyError:
        return redirect(loadLoginPage)

def createFTPAccount(request):
    try:
        userID = request.session['userID']
        currentACL = ACLManager.loadedACL(userID)

        if currentACL['admin'] == 1:
            pass
        elif currentACL['createFTPAccount'] == 1:
            pass
        else:
            return ACLManager.loadError()


        try:
            admin = Administrator.objects.get(pk=userID)

            if not os.path.exists('/home/cyberpanel/pureftpd'):
                return render(request, "ftp/createFTPAccount.html", {"status": 0})

            websitesName = ACLManager.findAllSites(currentACL, userID)

            return render(request, 'ftp/createFTPAccount.html', {'websiteList':websitesName,'admin':admin.userName, "status": 1})
        except BaseException, msg:
            logging.CyberCPLogFileWriter.writeToFile(str(msg))
            return HttpResponse(str(msg))

    except KeyError:
        return redirect(loadLoginPage)

def submitFTPCreation(request):
    try:
        userID = request.session['userID']
        try:
            if request.method == 'POST':

                currentACL = ACLManager.loadedACL(userID)

                if currentACL['admin'] == 1:
                    pass
                elif currentACL['createFTPAccount'] == 1:
                    pass
                else:
                    return ACLManager.loadErrorJson('creatFTPStatus', 0)


                data = json.loads(request.body)
                userName = data['ftpUserName']
                password = data['ftpPassword']
                path = data['path']
                domainName = data['ftpDomain']

                admin = Administrator.objects.get(id=userID)

                if len(path) > 0:
                    pass
                else:
                    path = 'None'

                execPath = "sudo python " + virtualHostUtilities.cyberPanel + "/plogical/ftpUtilities.py"

                execPath = execPath + " submitFTPCreation --domainName " + domainName + " --userName " + userName \
                           + " --password " + password + " --path " + path + " --owner " + admin.userName


                output = subprocess.check_output(shlex.split(execPath))

                if output.find("1,None") > -1:
                    data_ret = {'creatFTPStatus': 1, 'error_message': 'None'}
                    json_data = json.dumps(data_ret)
                    return HttpResponse(json_data)
                else:
                    data_ret = {'creatFTPStatus': 0, 'error_message': output}
                    json_data = json.dumps(data_ret)
                    return HttpResponse(json_data)

        except BaseException,msg:
            data_ret = {'creatFTPStatus': 0, 'error_message': str(msg)}
            json_data = json.dumps(data_ret)
            return HttpResponse(json_data)
    except KeyError,msg:
        data_ret = {'creatFTPStatus': 0, 'error_message': str(msg)}
        json_data = json.dumps(data_ret)
        return HttpResponse(json_data)

def deleteFTPAccount(request):
    try:
        userID = request.session['userID']
        currentACL = ACLManager.loadedACL(userID)

        if currentACL['admin'] == 1:
            pass
        elif currentACL['deleteFTPAccount'] == 1:
            pass
        else:
            return ACLManager.loadError()
        try:

            if not os.path.exists('/home/cyberpanel/pureftpd'):
                return render(request, "ftp/deleteFTPAccount.html", {"status": 0})

            websitesName = ACLManager.findAllSites(currentACL, userID)

            return render(request, 'ftp/deleteFTPAccount.html', {'websiteList':websitesName, "status": 1})
        except BaseException, msg:
            logging.CyberCPLogFileWriter.writeToFile(str(msg))
            return HttpResponse(str(msg))

    except KeyError:
        return redirect(loadLoginPage)

def fetchFTPAccounts(request):
    try:
        userID = request.session['userID']
        currentACL = ACLManager.loadedACL(userID)

        if currentACL['admin'] == 1:
            pass
        elif currentACL['deleteFTPAccount'] == 1:
            pass
        else:
            return ACLManager.loadErrorJson('fetchStatus', 0)
        try:
            if request.method == 'POST':
                data = json.loads(request.body)
                domain = data['ftpDomain']

                website = Websites.objects.get(domain=domain)

                ftpAccounts = website.users_set.all()

                json_data = "["
                checker = 0

                for items in ftpAccounts:
                    dic = {"userName":items.user}

                    if checker == 0:
                        json_data = json_data + json.dumps(dic)
                        checker = 1
                    else:
                        json_data = json_data + ',' + json.dumps(dic)

                json_data = json_data + ']'
                final_json = json.dumps({'fetchStatus': 1, 'error_message': "None", "data": json_data})
                return HttpResponse(final_json)



        except BaseException,msg:
            data_ret = {'fetchStatus': 0, 'error_message': str(msg)}
            json_data = json.dumps(data_ret)
            return HttpResponse(json_data)
    except KeyError,msg:
        data_ret = {'fetchStatus': 0, 'error_message': str(msg)}
        json_data = json.dumps(data_ret)
        return HttpResponse(json_data)

def submitFTPDelete(request):
    try:
        userID = request.session['userID']
        try:
            if request.method == 'POST':

                currentACL = ACLManager.loadedACL(userID)

                if currentACL['admin'] == 1:
                    pass
                elif currentACL['deleteFTPAccount'] == 1:
                    pass
                else:
                    return ACLManager.loadErrorJson('deleteStatus', 0)

                data = json.loads(request.body)
                ftpUserName = data['ftpUsername']

                FTPUtilities.submitFTPDeletion(ftpUserName)

                final_json = json.dumps({'deleteStatus': 1, 'error_message': "None"})
                return HttpResponse(final_json)

        except BaseException,msg:
            data_ret = {'deleteStatus': 0, 'error_message': str(msg)}
            json_data = json.dumps(data_ret)
            return HttpResponse(json_data)
    except KeyError,msg:
        data_ret = {'deleteStatus': 0, 'error_message': str(msg)}
        json_data = json.dumps(data_ret)
        return HttpResponse(json_data)

def listFTPAccounts(request):
    try:
        userID = request.session['userID']
        currentACL = ACLManager.loadedACL(userID)

        if currentACL['admin'] == 1:
            pass
        elif currentACL['listFTPAccounts'] == 1:
            pass
        else:
            return ACLManager.loadError()
        try:

            if not os.path.exists('/home/cyberpanel/pureftpd'):
                return render(request, "ftp/listFTPAccounts.html", {"status": 0})

            websitesName = ACLManager.findAllSites(currentACL, userID)

            return render(request, 'ftp/listFTPAccounts.html', {'websiteList':websitesName, "status": 1})
        except BaseException, msg:
            logging.CyberCPLogFileWriter.writeToFile(str(msg))
            return HttpResponse(str(msg))

    except KeyError:
        return redirect(loadLoginPage)

def getAllFTPAccounts(request):
    try:
        userID = request.session['userID']
        currentACL = ACLManager.loadedACL(userID)

        if currentACL['admin'] == 1:
            pass
        elif currentACL['listFTPAccounts'] == 1:
            pass
        else:
            return ACLManager.loadErrorJson('fetchStatus', 0)
        try:
            if request.method == 'POST':


                data = json.loads(request.body)
                selectedDomain = data['selectedDomain']

                domain = Websites.objects.get(domain=selectedDomain)

                records = Users.objects.filter(domain=domain)

                json_data = "["
                checker = 0

                for items in records:
                    dic = {'id': items.id,
                           'user': items.user,
                           'dir': items.dir,
                           'quotasize': str(items.quotasize)+"MB",
                           }

                    if checker == 0:
                        json_data = json_data + json.dumps(dic)
                        checker = 1
                    else:
                        json_data = json_data + ',' + json.dumps(dic)


                json_data = json_data + ']'
                final_json = json.dumps({'fetchStatus': 1, 'error_message': "None","data":json_data})
                return HttpResponse(final_json)

        except BaseException,msg:
            final_dic = {'fetchStatus': 0, 'error_message': str(msg)}
            final_json = json.dumps(final_dic)

            return HttpResponse(final_json)
    except KeyError:
        final_dic = {'fetchStatus': 0, 'error_message': "Not Logged In, please refresh the page or login again."}
        final_json = json.dumps(final_dic)
        return HttpResponse(final_json)

def changePassword(request):
    try:
        userID = request.session['userID']
        currentACL = ACLManager.loadedACL(userID)
        if currentACL['admin'] == 1:
            pass
        elif currentACL['listFTPAccounts'] == 1:
            pass
        else:
            return ACLManager.loadErrorJson('changePasswordStatus', 0)
        try:
            if request.method == 'POST':

                data = json.loads(request.body)
                userName = data['ftpUserName']
                password = data['ftpPassword']

                FTPUtilities.changeFTPPassword(userName, password)

                data_ret = {'changePasswordStatus': 1, 'error_message': "None"}
                json_data = json.dumps(data_ret)
                return HttpResponse(json_data)

        except BaseException,msg:
            data_ret = {'changePasswordStatus': 0, 'error_message': str(msg)}
            json_data = json.dumps(data_ret)
            return HttpResponse(json_data)
    except KeyError,msg:
        data_ret = {'changePasswordStatus': 0, 'error_message': str(msg)}
        json_data = json.dumps(data_ret)
        return HttpResponse(json_data)