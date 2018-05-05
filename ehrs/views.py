from django.shortcuts import render
from django.http import HttpResponse
import requests as r
import random, string, datetime
from .loginform import loginform, newehr, templateselect, vitalcomp, cancercomp
import json, os
import re
import numpy as np
import csv
from sklearn import svm
from sklearn.neural_network import MLPClassifier

token = ""
links = []
username = "not logged in"
template = ""
ehruid = ""
namelist = []
formlist = []


def index(request):
    return HttpResponse(render(request, 'ehrs/index.html'))


def main(request):
    global token, links, username

    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            username = str(form.cleaned_data['user'])
            password = str(form.cleaned_data['password'])
            organization = str(form.cleaned_data['organization'])

            parameters = {"username": username,
                          "password": password,
                          "organization": organization
                          }
            response = r.post('http://localhost:8090/ehr/api/v1/login', params=parameters)

            token = "Bearer " + str(response.json()['token'])
            # fetching user info
            user_resp = r.get('http://localhost:8090/ehr/api/v1/users/' + username, params={"format": "json"},
                              headers={"Authorization": token})
            user_info = user_resp.text.replace(",", "\n").replace("{", "").replace("[", "").replace(":",
                                                                                                    " - ").replace(
                "}", "\n").replace("]", "\n").replace("\"", "")

            # fetching ehr list
            ehrlist_resp = r.get('http://localhost:8090/ehr/api/v1/ehrs', params={"format": "json"},
                                 headers={"Authorization": token})
            ehrlist_json = json.loads(ehrlist_resp.text)
            json_filtered = str(ehrlist_json["ehrs"])
            ehr_list = []
            for i in range(0, len(ehrlist_json["ehrs"])):
                links.append(str(ehrlist_json["ehrs"][i]["uid"]))
                ehr_list.append(
                    str(ehrlist_json["ehrs"][i]["uid"]) + "  ------  " + str(ehrlist_json["ehrs"][i]["dateCreated"]))

            zipped = zip(links, ehr_list)
            return HttpResponse(render(request, 'ehrs/main.html', {"user_info": user_info, "zipped": zipped}))

    if len(token) != 0:
        user_resp = r.get('http://localhost:8090/ehr/api/v1/users/' + username, params={"format": "json"},
                          headers={"Authorization": token})
        user_info = user_resp.text.replace(",", "\n").replace("{", "").replace("[", "").replace(":",
                                                                                                " - ").replace(
            "}", "\n").replace("]", "\n").replace("\"", "")

        # fetching ehr list
        ehrlist_resp = r.get('http://localhost:8090/ehr/api/v1/ehrs', params={"format": "json"},
                             headers={"Authorization": token})
        ehrlist_json = json.loads(ehrlist_resp.text)
        json_filtered = str(ehrlist_json["ehrs"])
        ehr_list = []
        for i in range(0, len(ehrlist_json["ehrs"])):
            links.append(str(ehrlist_json["ehrs"][i]["uid"]))
            ehr_list.append(
                str(ehrlist_json["ehrs"][i]["uid"]) + "  ------  " + str(ehrlist_json["ehrs"][i]["dateCreated"]))

        zipped = zip(links, ehr_list)
        return HttpResponse(render(request, 'ehrs/main.html', {"user_info": user_info, "zipped": zipped}))

    else:
        return HttpResponse("not logged in.")


def ehrinfo(request, uid):
    global ehruid, template
    ehruid = str(request.get_full_path().replace("/ehrs/main/ehrinfo/", ""))

    ehrinfo_resp = r.get('http://localhost:8090/ehr/api/v1/ehrs/ehrUid/' + ehruid, params={"format": "json"},
                         headers={"Authorization": token}).text.replace(",", "\n").replace("{", "").replace("[",
                                                                                                            "").replace(
        ":",
        " - ").replace(
        "}", "\n").replace("]", "\n").replace("\"", "")

    z = json.load(open("C:\\Users\\DELL\\Desktop\\webclinic\\ehrs\\data.json"))

    composition_links = []
    composition_details = []
    indexlist = []
    try:
        for j in range(len(z[ehruid]["compositions"])):
            composition_links.append("Compostion Uid: " + z[ehruid]["compositions"][j]["composition_uid"])
            composition_details.append("Date Created: " + z[ehruid]["compositions"][j]["date_created"] + "\n" + "            Template Type: " + z[ehruid]["compositions"][j]["template_name"])
            indexlist.append(str(j))


    except:
        print("xyz")


    zipped = zip(indexlist, composition_links, composition_details)

    return HttpResponse(render(request, 'ehrs/ehrinfo.html', {"ehrinfo_resp": ehrinfo_resp, "zipped": zipped, "uid": ehruid}))


def ehrcreate(request):
    return HttpResponse(render(request, "ehrs/ehrcreate.html"))


def createsuccess(request):
    if request.method == 'POST':
        form = newehr(request.POST)
        print("a")
        if form.is_valid():
            print("b")
            ehruid = str(form.cleaned_data["ehruid"])
            subuid = str(form.cleaned_data["subuid"])
            if len(ehruid) == 0:
                print("c")
                ehruid = ''.join(
                    [random.choice(string.ascii_letters + string.digits) for n in range(36)])
                response = r.post("http://localhost:8090/ehr/api/v1/ehrs",
                                  params={"format": "json", "uid": ehruid, "subjectUid": subuid}, headers={"Authorization": token})
                print("response: " + response.text)

                z = json.load(open("C:\\Users\\DELL\\Desktop\\webclinic\\ehrs\\data.json"))
                z[ehruid] = {"compositions": []}
                json.dump(z, open("C:\\Users\\DELL\\Desktop\\webclinic\\ehrs\\data.json", 'w'))
            else:
                print("d")
                response = r.post("http://localhost:8090/ehr/api/v1/ehrs",
                                  params={"format": "json", "uid": ehruid, "subjectUid": subuid},
                                  headers={"Authorization": token})
                print("response: " + response.text)
                z = json.load(open("C:\\Users\\DELL\\Desktop\\webclinic\\ehrs\\data.json"))
                z[ehruid] = {"compositions": []}
                json.dump(z, open("C:\\Users\\DELL\\Desktop\\webclinic\\ehrs\\data.json", 'w'))
    print("e")
    return HttpResponse(render(request, 'ehrs/createsuccess.html'))


def compcreate(request):
    global template, ehruid, namelist, formlist
    if request.method == 'GET':
        form = templateselect(request.GET)
        print("a")
        if form.is_valid():
            print("b")
            template = str(form.cleaned_data["template"])
            if template == "Vital Signs":
                formlist = ["Age", "Sex", "Chest Pain Type (1-4)", "Resting blood pressure (mm Hg)",
                            "serum cholestoral (mg/dl)", "fasting blood sugar>120 mg/dl (1 = true; 0 = false)",
                            "resting electrocardiographic results: (class 0-2): ",
                            "maximum heart rate achieved", "exercise induced angina (1 = yes; 0 = no)",
                            "ST depression induced by exercise relative to rest",
                            "the slope of the peak exercise ST segment: (class 1-3)",
                            "number of major vessels (0-3)",
                            " thal: 3 = normal, 6 = fixed defect, 7 = reversable defect"]
                namelist = ["age", "sex", "cpt", "rbp", "chol", "fbsugar", "regc", "maxhr", "exang", "std", "slope",
                            "ves", "thal"]
            elif template == "Cancer Signs":
                formlist = ["Clump Thickness(1-10)", "Uniformity of Cell Size(1-10)", "Uniformity of Cell Shape(1-10)",
                            "Marginal Adhesion(1-10)", "Single Epithelial Cell Size(1-10)", "Bare Nuclei(1-10)",
                            "Bland Chromatin(1-10)", "Normal Nucleoli(1-10)", "Mitoses(1-10)"]
                namelist = ["clump", "cellsize", "cellshape", "marg", "epicell",
                            "bare", "bland", "nucleoli", "mitoses"]



            zipped = zip(formlist, namelist)
            return HttpResponse(render(request, 'ehrs/compcreate.html', {"zipped": zipped}))


def compsuccess(request):
    global template, namelist, formlist, ehruid
    if request.method == 'POST':
        if template == "Vital Signs":
            form = vitalcomp(request.POST)
            if form.is_valid():
                vitaldata = []

                vitaldata.append(form.cleaned_data["age"])
                vitaldata.append(form.cleaned_data["sex"])
                vitaldata.append(form.cleaned_data["cpt"])
                vitaldata.append(form.cleaned_data["rbp"])
                vitaldata.append(form.cleaned_data["chol"])
                vitaldata.append(form.cleaned_data["fbsugar"])
                vitaldata.append(form.cleaned_data["regc"])
                vitaldata.append(form.cleaned_data["maxhr"])
                vitaldata.append(form.cleaned_data["exang"])
                vitaldata.append(form.cleaned_data["std"])
                vitaldata.append(form.cleaned_data["slope"])
                vitaldata.append(form.cleaned_data["ves"])
                vitaldata.append(form.cleaned_data["thal"])

                z = json.load(open("C:\\Users\\DELL\\Desktop\\webclinic\\ehrs\\data.json"))



                composition_uid = ''.join(
                    [random.choice(string.ascii_letters + string.digits) for n in range(20)])
                date_created = str(datetime.datetime.now().strftime("%I:%M%p on %B %d %Y"))
                healthdata = {"composition_uid": composition_uid, "date_created": date_created, "template_name": template}
                for x, y in zip(namelist, vitaldata):
                    healthdata[str(x)] = str(y)
                z[ehruid]["compositions"].append(healthdata)
                json.dump(z, open("C:\\Users\\DELL\\Desktop\\webclinic\\ehrs\\data.json", 'w'))
                return HttpResponse(render(request, 'ehrs/compsuccess.html'))

        elif template == 'Cancer Signs':
            form2 = cancercomp(request.POST)
            if form2.is_valid():
                cancerdata = []
                cancerdata.append(form2.cleaned_data["clump"])
                cancerdata.append(form2.cleaned_data["cellsize"])
                cancerdata.append(form2.cleaned_data["cellshape"])
                cancerdata.append(form2.cleaned_data["marg"])
                cancerdata.append(form2.cleaned_data["epicell"])
                cancerdata.append(form2.cleaned_data["bare"])
                cancerdata.append(form2.cleaned_data["bland"])
                cancerdata.append(form2.cleaned_data["nucleoli"])
                cancerdata.append(form2.cleaned_data["mitoses"])

                z = json.load(open("C:\\Users\\DELL\\Desktop\\webclinic\\ehrs\\data.json"))


                composition_uid = ''.join(
                    [random.choice(string.ascii_letters + string.digits) for n in range(20)])
                date_created = str(datetime.datetime.now().strftime("%I:%M%p on %B %d %Y"))
                healthdata = {"composition_uid": composition_uid, "date_created": date_created,
                              "template_name": template}

                for x, y in zip(namelist, cancerdata):
                    healthdata[str(x)] = str(y)
                z[ehruid]["compositions"].append(healthdata)
                json.dump(z, open("C:\\Users\\DELL\\Desktop\\webclinic\\ehrs\\data.json", 'w'))
                return HttpResponse(render(request, 'ehrs/compsuccess.html'))



def compdisplay(request, uid, index):
    global template, formlist, namelist
    abbr = zip([], [])
    url = request.get_full_path()
    x = url.replace("/ehrs/main/ehrinfo/", "").replace("compdisplay/", "")
    ehruid, ci = x.split("/")
    compindex = int(ci)
    print(ehruid)
    print(compindex)

    z = json.load(open("C:\\Users\\DELL\\Desktop\\webclinic\\ehrs\\data.json"))
    compdata = str(z[ehruid]["compositions"][compindex])
    dictdata = z[ehruid]["compositions"][compindex]
    predarraystr = list(dictdata.values())[3:]
    predarray = [float(i) for i in predarraystr]
    print("array is: ", predarray)


    print(type(compdata))
    compdata2 = compdata.replace(",", "\n").replace("{", "").replace("}", "").replace("\'", "").replace(":", " : ")
    print(compdata2)
    X = 0
    y = 0
    template = z[ehruid]["compositions"][compindex]["template_name"]
    # svm algorithm
    if template == "Vital Signs":
        reader = csv.reader(open("C:\\Users\\DELL\\Desktop\\webclinic\\neural\\cleveland_data.csv"), delimiter=",")
        x = list(reader)
        result = np.array(x).astype("float")

        X = result[:, :13]
        y = result[:, 13]
        formlist = ["Age", "Sex", "Chest Pain Type (1-4)", "Resting blood pressure (mm Hg)",
                    "serum cholestoral (mg/dl)", "fasting blood sugar>120 mg/dl (1 = true; 0 = false)",
                    "resting electrocardiographic results: (class 0-2): ",
                    "maximum heart rate achieved", "exercise induced angina (1 = yes; 0 = no)",
                    "ST depression induced by exercise relative to rest",
                    "the slope of the peak exercise ST segment: (class 1-3)",
                    "number of major vessels (0-3)",
                    " thal: 3 = normal, 6 = fixed defect, 7 = reversable defect"]
        namelist = ["age", "sex", "cpt", "rbp", "chol", "fbsugar", "regc", "maxhr", "exang", "std", "slope",
                    "ves", "thal"]
        abbr = zip(namelist, formlist)
        notation = "0 stands for no heart disease,\n1 stands for heart related disease."
        clf = svm.SVC()
        clf.fit(X, y)
        pred1 = clf.predict([predarray])
        pred1a = pred1
        if pred1>0:
            pred1 = 1
        print("SVM prediction: ", pred1)

        vitalfloat = [float(i) for i in predarray]
        vitalfloat.append(int(pred1a))
        with open("C:\\Users\\DELL\\Desktop\\webclinic\\ehrs\\cleveland_data.csv", "a") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows([vitalfloat])

        # neural algo
        for i in range(len(y)):
            if y[i] > 0:
                y[i] = 1

        clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                            hidden_layer_sizes=(13, 10, 5), random_state=1)

        clf.fit(X, y)

        pred2 = clf.predict([predarray])
        print("Neural prediction: ", pred2)



    elif template == "Cancer Signs":
        reader = csv.reader(open("C:\\Users\\DELL\\Desktop\\webclinic\\neural\\cancer.csv"), delimiter=",")
        x = list(reader)
        result = np.array(x).astype("int")
        # svm pred
        X = result[:, :9]
        y = result[:, 9]
        formlist = ["Clump Thickness", "Uniformity of Cell Size", "Uniformity of Cell Shape",
                    "Marginal Adhesion", "Single Epithelial Cell Size", "Bare Nuclei",
                    "Bland Chromatin", "Normal Nucleoli", "Mitoses"]
        namelist = ["clump", "cellsize", "cellshape", "marg", "epicell",
                    "bare", "bland", "nucleoli", "mitoses"]
        abbr = zip(namelist, formlist)
        notation = "0 stands for benign tumor, which is not harmful,\n1 stands for malignant tumor, which is harmful."
        clf = svm.SVC()
        clf.fit(X, y)
        pred1 = clf.predict([predarray])
        if pred1 == 2:
            pred1 = 0
        else:
            pred1 = 1
        print("SVM prediction: ", pred1)

        id = random.randrange(890000, 990000)
        cancerint1 = [id]
        cancerint2 = [int(i) for i in predarray]
        cancerint = cancerint1+cancerint2
        if pred1 == 0:
            addpred = 2
        else:
            addpred = 4
            cancerint.append(addpred)
        with open("C:\\Users\\DELL\\Desktop\\webclinic\\neural\\cancer.csv", "a") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows([cancerint])


        # neural pred
        for i in range(len(y)):
            if y[i] == 2:
                y[i] = 0
            elif y[i] == 4:
                y[i] = 1

        clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                            hidden_layer_sizes=(13, 10, 5), random_state=1)

        clf.fit(X, y)

        pred2 = clf.predict([predarray])
        if pred2>0:
            pred2 = 1
        print("Neural prediction: ", pred2)


    return HttpResponse(render(request, 'ehrs/compdisplay.html', {"compdata2": compdata2, "abbr": abbr, "pred1": pred1, "pred2": pred2, "notation": notation}))


