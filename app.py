from flask import Flask, redirect, request, render_template, url_for
import requests
from bs4 import BeautifulSoup
from datetime import datetime
app = Flask("__main__")


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36",
}


def read(filename):
    try:
        file = open(filename, "r").read()
    except:
        file = open(filename, "w+")
        file = open(filename, "r").read()
    return (file.splitlines())


def write(content, filename, mode):
    f = open(filename, mode)
    f.write(content)
    f.close


def dataresults(arr, filename):
    data = read(filename)
    for i in range(1, len(data)):
        dataline = data[i].split("++")
        arr.append(dataline)
    return arr


def calCryptoJobs(cat, filename):
    url = "https://crypto-job.com/jobs?location=&q=" + \
        cat+"&category=&job_type=&exp_level="
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    listing = soup.find_all(class_="job-listing", href=True)
    today = str(datetime.now().day) + "\n"
    write(today, filename, mode="w")
    for i in listing:
        position = i.find(class_="job-listing-title").text
        company = i.find(class_="job-listing-company").text
        lurl = i['href']
        c = ' '.join(company.split())
        content = position + "++" + c+"++"+lurl+"\n"
        write(content, filename=filename, mode="a")


def datafromcryptojobs(cat):
    filename = cat+"cj.txt"
    arr = []

    data = read(filename)

    if len(data) != 0:
        if not (int(data[0])+3) < datetime.now().day:
            return dataresults(arr, filename)
        else:
            calCryptoJobs(cat, filename)
    else:
        calCryptoJobs(cat, filename)
    return dataresults(arr, filename)


def cryptojoblist(cat, filename):
    url = "https://cryptojobslist.com/" + cat
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    listing = soup.find_all(
        class_="JobPreviewInline_JobPreviewInline__uAIxU JobPreviewInline_featured__u3eGF undefined duration-300")
    today = str(datetime.now().day) + "\n"
    write(today, filename, mode="w")
    for i in listing:
        position = i.find(class_="JobPreviewInline_companyName__5ffOt").text
        company = i.find(
            class_="JobPreviewInline_jobTitle__WYzmv text-brand-blue dark:text-white", href=True)
        lurl = "https://cryptojobslist.com"+company['href']
        content = company.text + "++" + position+"++"+lurl+"\n"
        write(content, filename=filename, mode="a")


def datafromcryptojoblist(cat):
    filename = cat+"cjl.txt"
    arr = []

    data = read(filename)

    if len(data) != 0:
        if not (int(data[0])+3) < datetime.now().day:
            return dataresults(arr, filename)
        else:
            cryptojoblist(cat, filename)
    else:
        cryptojoblist(cat, filename)
    return dataresults(arr, filename)


@app.route("/", methods=["POST", "GET"])
def index1():
    if request.method == "POST":
        cat = request.form.get("category")
        host = request.host_url
        red = host+cat
        return redirect(red)
    return render_template("index.html")


@app.route("/<cat>", methods=["POST", "GET"])
def result(cat):
    data1 = (datafromcryptojobs(cat))
    data2 = (datafromcryptojoblist(cat))
    return render_template("results.html", res=data1, resu=data2)


if __name__ == "__main__":

    app.run(debug=True)
