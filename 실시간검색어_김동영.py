from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen  # URL open import
from urllib.parse import quote

import time
import pandas as pd
import numpy as np

from wordcloud import WordCloud
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import messagebox

class main:
    def __init__(self, window):
        self.t = []
        self.n = {}
        self.d = {}
        self.naverbutton = []
        self.daumbutton = []
        self.mw = [[], []]
        self.naverl = []
        self.dauml = []
        self.name = ["naver", "daum"]

        self.window = window
        self.Seasonal()

    def Seasonal(self):
        self.f = Frame(self.window, bg="snow");
        self.f.pack()
        self.ls = Label(self.f, text="주기를 입력하시오 (단위: 분) ", font=("Malgun Gothic", 11), bg="snow");
        self.ls.pack(side="left", ipadx=10, ipady=10)
        self.es = Entry(self.f);
        self.es.pack(side="left", ipadx=10, ipady=10)
        self.bs = Button(self.f, text="입력", command=self.insertData, font=("Malgun Gothic", 11), bg="snow2");
        self.bs.pack(side="left", padx=10, pady=10)

    def insertData(self):
        self.seasonal = int(self.es.get())
        self.f.pack_forget()
        self.showInfo()

    def showInfo(self):
        self.window.geometry("825x970")
        self.window.resizable(False, False)
        self.f1 = Frame(self.window, bg="snow");
        self.f1.grid(row=0, column=0, columnspan=2)
        self.f5 = Frame(self.window, height=50, bg="snow");
        self.f5.grid(row=1, column=0, columnspan=2)
        self.f2 = Frame(self.window, width=400, height=600, relief="solid", bg="snow");
        self.f2.grid(row=2, column=0)
        self.f3 = Frame(self.window, width=400, height=600, relief="solid", bg="snow");
        self.f3.grid(row=2, column=1)

        self.f2_1 = Frame(self.f2, width=300, relief="solid", bd=2, bg="ghost white");
        self.f2_1.pack(pady=5)
        self.f3_1 = Frame(self.f3, width=300, relief="solid", bd=2, bg="ghost white");
        self.f3_1.pack(pady=5)
        self.f4 = Frame(self.window, height=50, relief="solid", bd=2, bg="white");
        self.f4.grid(row=3, column=0, columnspan=2)
        self.f6 = Frame(self.window, height=50, bg="snow");
        self.f6.grid(row=4, column=0, columnspan=2, ipady=2)

        # wordcloud
        self.l1 = Label(self.f1, image=None);
        self.l1.grid(row=0, column=0, padx=3.5, pady=3)
        self.l2 = Label(self.f1, image=None);
        self.l2.grid(row=0, column=1, padx=3.5, pady=3)
        # 진입 빈도
        self.l0_1 = Label(self.f1, text="[ 사이트별 진입한 검색어 횟수 TOP 5 ]", font=("Malgun Gothic", 12, "bold"), fg="deep Pink",
                          bg="snow");
        self.l0_1.grid(row=1, column=0, columnspan=2, padx=10, pady=3)
        self.l1_2 = Label(self.f1, image=None);
        self.l1_2.grid(row=2, column=0, padx=3.5, pady=3)
        self.l2_2 = Label(self.f1, image=None);
        self.l2_2.grid(row=2, column=1, padx=3.5, pady=3)
        # 검색어 입력
        self.l3 = Label(self.f2_1, text="Naver", font=("Arial", 14, "bold"), bg="lawn green");
        self.l3.grid(row=0, column=0, columnspan=2, ipadx=165)
        self.l4 = Label(self.f3_1, text="Daum ", font=("Arial", 14, "bold"), bg="royalBlue1");
        self.l4.grid(row=0, column=0, columnspan=2, ipadx=165)
        # 검색어 순위 차이
        self.l5 = Label(self.f4, text=None, font=("Malgun Gothic", 12, "bold"), fg="firebrick4", bg="white");
        self.l5.grid(row=0, column=0, padx=10, pady=3)
        self.l6 = Label(self.f4, text=None, font=("Malgun Gothic", 12, "bold"), fg="firebrick4", bg="white");
        self.l6.grid(row=0, column=1, padx=10, pady=3)
        self.l8 = Label(self.f5, text=None, font=("Malgun Gothic", 10), fg="blue", bg="snow");
        self.l8.pack(padx=5, pady=3)
        # 종료 버튼
        self.bt = Button(self.f6, text="종료", command=self.end, font=("Malgun Gothic", 11), fg="red", bg="white");
        self.bt.pack()

        self.countdown(self.seasonal * 60)
        self.crawl()

    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining
        if self.remaining > 0:
            self.l8.configure(text="update after %d sec" % self.remaining)  # 남은 시간을 표시
            self.remaining = self.remaining - 1
            self.window.after(1000, self.countdown)  # 1000ms(1초)가 지날 때마다 시간을 체크
        if self.remaining == 0:  # 모든 시간이 경과한 경우
            # 변수 초기화
            self.n = {}
            self.d = {}
            self.naverbutton = []
            self.daumbutton = []
            self.mw = [[], []]
            self.remaining = self.seasonal * 60  # 다음번에 다시 사용하기 위해

            # 크롤링
            self.crawl()

    def crawl(self):
        # naver
        now = time.localtime()  # 현재 시간
        h = now.tm_hour
        m = now.tm_min

        tim = """//*[@id="content"]/div/div[2]/div[1]/div[1]/div/div/div/div[2]/a[3]/span[1]"""
        tim = ndriver.find_element_by_xpath(tim).click()

        # 현재시간
        hou = """//*[@id="u.c.layer.time"]/div[6]/a[1]"""
        hour = ndriver.find_element_by_xpath(hou).click()

        ok = """//*[@id="u.c.layer.time"]/div[6]/a[2]"""
        send = ndriver.find_element_by_xpath(ok).click()

        html1 = ndriver.page_source
        soup1 = BeautifulSoup(html1, 'html.parser')
        rank1 = soup1.find_all("span", {"class": "item_title"})
        self.naver = []
        for i in range(10):
            for a in rank1[i]:
                self.naver.append(a)  # naver 검색어 10개 저장
        self.naverl.append(self.naver)

        # daum
        url = "https://www.daum.net/"
        page = urlopen(url)  ## web page read
        soup2 = BeautifulSoup(page, 'html.parser')
        rank2 = soup2.find_all("a", {"class": "link_issue"})
        self.daum = []
        for i in range(20):
            self.daum.append(rank2[i].text)  # 다음 검색어 10개 저장
        self.daum = self.daum[::2]
        self.dauml.append(self.daum)

        self.t.append(str(now.tm_mon) + "/" + str(now.tm_mday) + " " + str(h) + ":" + str(m))  # 시간 저장

        # 분석과 시각화에 필요한 데이터의 형태로 바꿔주기 위한 전처리 함수
        self.preprocess()

    def preprocess(self):
        self.naverday = pd.DataFrame({"word": self.naver, "rank": range(10)})
        self.naverday["rank"] += 1

        self.daumday = pd.DataFrame({"word": self.daum, "rank": range(10)})
        self.daumday["rank"] += 1

        self.totalword = pd.concat([self.naverday["word"], self.daumday["word"]]).unique()
        # 차이 구하는 용
        self.td = pd.DataFrame(0, index=range(len(self.totalword)), columns=["totalword", "naver", "daum"])
        self.td["totalword"] = self.totalword

        for i in range(10):
            for j in range(len(self.td["totalword"])):
                if self.naverday.iloc[i, 0] == self.td.iloc[j, 0]:
                    self.td.iloc[j, 1] = self.naverday.iloc[i, 1]
                if self.daumday.iloc[i, 0] == self.td.iloc[j, 0]:
                    self.td.iloc[j, 1] = self.naverday.iloc[i, 1]

        # wordcloud용
        for i in range(10):
            self.n[self.naverday.loc[i, "word"]] = 11 - self.naverday.loc[i, "rank"]
            self.d[self.daumday.loc[i, "word"]] = 11 - self.daumday.loc[i, "rank"]

        # 상관관계, 그래프용
        self.nd = pd.DataFrame(np.nan, index=self.totalword, columns=self.t)
        self.dd = pd.DataFrame(np.nan, index=self.totalword, columns=self.t)
        nl = [0] * len(self.nd.index)
        dl = [0] * len(self.dd.index)

        for i in range(len(self.t)):
            for j in range(len(self.nd.index)):
                for k in range(10):
                    if self.naverl[i][k] == self.nd.index[j]:
                        self.nd.iloc[j, i] = k + 1
                        nl[j] += 1
        self.nd["site"] = "Naver"

        for i in range(len(self.t)):
            for j in range(len(self.dd.index)):
                for k in range(10):
                    if self.dauml[i][k] == self.dd.index[j]:
                        self.dd.iloc[j, i] = k + 1
                        dl[j] += 1
        self.dd["site"] = "Daum"

        # 진입 횟수용
        self.ni = pd.DataFrame({"word": self.nd.index, "진입": nl})
        self.di = pd.DataFrame({"word": self.dd.index, "진입": dl})

        self.findDiff()
        self.wordcloud()
        self.inserttop()
        self.printWord()
        self.corrcoef(self.nd.iloc[:, -2], self.dd.iloc[:, -2], 1)

    def wordcloud(self):
        colors = ["#BF0A30", "#002868"]
        cmap = LinearSegmentedColormap.from_list("mycmap", colors)

        # 네이버
        wordcloud = WordCloud(font_path="BMJUA_ttf.ttf", background_color="white", random_state=5, min_font_size=10,
                              max_font_size=80, colormap=cmap).generate_from_frequencies(self.n)
        fig = plt.figure(figsize=[4, 1.6])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        fig.savefig(self.name[0] + ".png")
        plt.clf()

        self.imga = PhotoImage(file=self.name[0] + ".png")
        self.l1.config(image=self.imga)

        # 다음
        wordcloud = WordCloud(font_path="BMJUA_ttf.ttf", background_color="white", random_state=5, min_font_size=10,
                              max_font_size=80, colormap=cmap).generate_from_frequencies(self.d)
        fig = plt.figure(figsize=[4, 1.6])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        fig.savefig(self.name[1] + ".png")

        self.imgb = PhotoImage(file=self.name[1] + ".png")
        self.l2.config(image=self.imgb)
        self.l1.image = self.imga
        self.l2.image = self.imgb

    def inserttop(self):
        plt.rc('font', family="Malgun Gothic")
        plt.rcParams.update({'figure.max_open_warning': 0})

        # 순위 안으로 진입한 횟수가 많은 순으로 정렬 + 상위 5개 선택
        self.ni = self.ni.sort_values(by="진입", ascending=False)
        self.topni = self.ni[:5]
        self.di = self.di.sort_values(by="진입", ascending=False)
        self.topdi = self.di[:5]

        labels = []
        for i in range(5):
            labels.append(self.topni.iloc[i, 0] + "(" + str(self.topni.iloc[i, 1]) + ")")

        fig3 = plt.figure(figsize=[4, 2])
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'orange']
        explode = (0.1, 0.1, 0.1, 0.1, 0.1)
        # 네이버 pie plot
        plt.pie(self.topni["진입"], explode=explode, labels=labels, autopct='%1.1f%%', colors=colors, shadow=True,
                startangle=140)
        plt.axis('equal')
        fig3.savefig("np.png")
        plt.clf()

        labels = []
        for i in range(5):
            labels.append(self.topdi.iloc[i, 0] + "(" + str(self.topdi.iloc[i, 1]) + ")")

        fig4 = plt.figure(figsize=[4, 2])
        # 다음 pie plot
        plt.pie(self.topdi["진입"], explode=explode, labels=labels, autopct='%1.1f%%', colors=colors, shadow=True,
                startangle=140)
        plt.axis('equal')
        fig4.savefig("dp.png")

        self.np = PhotoImage(file="np.png")
        self.dp = PhotoImage(file="dp.png")
        self.l1_2.config(image=self.np)
        self.l2_2.config(image=self.dp)
        self.l1_2.image = self.np
        self.l2_2.image = self.dp

    def printWord(self):
        # 검색어 시각화
        self.labels = []
        for i in range(10):
            c = lambda index=i: self.create_window(self.naver[index])
            self.naverbutton.append(
                Button(self.f2_1, text=self.naver[i], command=c, font=("Malgun Gothic", 11), width=30, bg="white"))
            self.labels.append(
                Label(self.f2_1, text=str(i + 1) + "위", font=("Malgun Gothic", 11, 'bold'), bg="ghost white"))
            self.labels[i].grid(row=i + 1, column=0, padx=10, pady=2)
            self.naverbutton[i].grid(row=i + 1, column=1, padx=10, pady=2)

        self.labels = []
        for i in range(10):
            c = lambda index=i: self.create_window(self.daum[index])
            self.daumbutton.append(
                Button(self.f3_1, text=self.daum[i], command=c, font=("Malgun Gothic", 11), width=30, bg="white"))
            self.labels.append(
                Label(self.f3_1, text=str(i + 1) + "위", font=("Malgun Gothic", 11, 'bold'), bg="ghost white"))
            self.labels[i].grid(row=i + 1, column=0, padx=10, pady=2)
            self.daumbutton[i].grid(row=i + 1, column=1, padx=10, pady=2)

    def findDiff(self):
        # 포털별 순위차이가 가장 큰/작은 검색어 분석
        self.td["absdiff"] = abs(self.td["naver"] - self.td["daum"])
        maxdiff = self.td["absdiff"].max()
        mindiff = self.td["absdiff"].min()
        for i in range(len(self.td)):
            if self.td.loc[i, "absdiff"] == maxdiff:
                self.mw[0].append(self.td.loc[i, "totalword"])
            if self.td.loc[i, "absdiff"] == mindiff:
                self.mw[1].append(self.td.loc[i, "totalword"])

        self.l5.config(
            text="포털별 순위차이가 가장 큰 검색어: " + ", ".join(self.mw[0]) + "\n포털별 순위차이가 가장 작은 검색어: " + ", ".join(self.mw[1]))

    def relate(self):
        # 네이버 연관검색어
        url="https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=" + quote(self.w)
        page = urlopen(url)
        soup2 = BeautifulSoup(page, 'html.parser')
        rank2 = soup2.find_all("a", {"data-area": "*q"})
        self.relateword = []
        for i in range(len(rank2)):
            self.relateword.append(rank2[i].text)

        # 다음 연관검색어
        url="https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&q=" + quote(self.w)
        page = urlopen(url)
        soup2 = BeautifulSoup(page, 'html.parser')
        rank2 = soup2.find_all("a", {"class": "keyword"})
        for i in range(len(rank2)):
            self.relateword.append(rank2[i].text)

        # 연관 뉴스
        url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + quote(self.w)
        page = urlopen(url)
        soup2 = BeautifulSoup(page, 'html.parser')
        rank2 = soup2.find_all("a", {"class": "_sp_each_title"})
        self.relatenews = []
        for i in range(4):
            self.relatenews.append(rank2[i].text)

        # 연관 검색어와 뉴스의 포털별 중복 제거
        self.relateword = list(set(self.relateword))
        self.relatenews = list(set(self.relatenews))

        self.lt = Label(self.rel, text=" [ 연관 검색어 ] ", font=("Malgun Gothic", 15), bg="snow")
        self.lt.grid(row=0, column=0, columnspan=4)

        self.rw = []
        self.rn = []
        length = len(self.relateword) // 4 + 1
        cnt = 0
        if len(self.relateword) == 0:
            self.words = Label(self.rel, text="없음", font=("Malgun Gothic", 12), bg="snow");
            self.words.grid(row=1, column=0, columnspan=4)
        else:
            for i in range(length):
                for j in range(4):
                    if i * 4 + j != len(self.relateword):
                        self.rw.append(
                            Label(self.rel, text=self.relateword[cnt], font=("Malgun Gothic", 11), bg="snow"))
                        self.rw[cnt].grid(row=i + 1, column=j, padx=10, pady=2)
                        cnt += 1
                    else:
                        break

        self.lt = Label(self.rel, text=" [ 연관 뉴스 ] ", font=("Malgun Gothic", 15), bg="snow")
        self.lt.grid(row=length + 2, column=0, columnspan=4)
        cnt = 0
        if len(self.relatenews) == 0:
            self.news = Label(self.rel, text="없음", font=("Malgun Gothic", 12), bg="snow");
            self.news.grid(row=1, column=0, columnspan=4)
        else:
            for i in range(len(self.relatenews)):
                self.rn.append(Label(self.rel, text=self.relatenews[cnt], font=("Malgun Gothic", 11), bg="snow"))
                self.rn[cnt].grid(row=length + i + 3, column=0, columnspan=4, padx=10, pady=2)
                cnt += 1

    def findPlot(self):
        plt.rc('font', family="Malgun Gothic")
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams.update({'figure.max_open_warning': 0})

        # 선택한 단어와 맞는 순위 만을 가져와 시간에 따른 순위 변화를 시각화
        np = self.nd[self.nd.index == self.w]
        dp = self.dd[self.dd.index == self.w]
        p = pd.concat([np, dp])
        p2 = p.reset_index(drop=True)
        p3 = p2.set_index('site')
        del p3.index.name
        self.df = p3.T

        fig2 = plt.figure(figsize=[8, 4])
        plt.plot(self.df["Daum"], marker="o", lw=2, label="Daum")
        plt.plot(self.df["Naver"], marker="x", lw=2, ms=11, label="Naver")
        plt.title(self.w + "의 순위 변화")
        plt.ylim(11, -1)
        plt.xlabel("시간")
        plt.ylabel("실시간 검색어 순위 (단위:위)")
        plt.legend()
        can = FigureCanvasTkAgg(fig2, self.canvas)
        can.get_tk_widget().pack()

    # 상관관계
    def corrcoef(self, a, b, num):
        a=a.copy() # 순위값이 변하면 안되므로 copy
        b=b.copy() # 순위값이 변하면 안되므로 copy
        for i in range(len(a)):
            if a.iloc[i]!=np.nan:
                a.iloc[i]=12-a.iloc[i]
            if b.iloc[i]!=np.nan:
                b.iloc[i]=12-b.iloc[i]
        a = a.fillna(1)
        b = b.fillna(1)

        if num == 1:  # 포털사이트 별 전체 순위의 상관관계
            ndfl = a.tolist()
            ddfl = b.tolist()
            self.coco = round(np.corrcoef(ndfl, ddfl)[0, 1], 3)
            self.l6.config(text="포털별 상관관계 정도 : " + str(round(self.coco, 3)))

        if num == 2:  # 선택한 특정 검색어의 시간에 따른 순위 변화의 상관관계
            ndfl = [0]+a.tolist()
            ddfl = [0]+b.tolist()
            self.coco = round(np.corrcoef(ndfl, ddfl)[0, 1], 3)
            self.co.config(text="시간별 상관관계 정도 : " + str(round(self.coco, 3)))

    def video(self):
        self.ydriver = webdriver.Chrome('driver/chromedriver')  # 크롬 드라이버 지정 - 유투브
        self.ydriver.get("https://www.youtube.com/results?search_query="+self.w)

    def image(self):
        self.gdriver = webdriver.Chrome('driver/chromedriver')  # 크롬 드라이버 지정 - 구글
        self.gdriver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")
        self.gdriver.find_element_by_name('q').send_keys(self.w)
        self.gdriver.find_element_by_xpath("""//*[@id="sbtc"]/button/div/span""").click()

    def create_window(self, w):
        self.w = w
        self.window2 = Tk()
        self.window2.title(w)
        self.window2.config(bg="snow")
        self.co = Label(self.window2, text=None, font=("Malgun Gothic", 14, "bold"), fg="firebrick4", bg="snow");
        self.co.pack()
        # create the canvas
        self.canvas = Canvas(self.window2, bg="white");
        self.canvas.pack(expand=YES, fill=BOTH)
        self.rel = Frame(self.window2, bg="snow");
        self.rel.pack()
        self.searching = Frame(self.window2, bg="snow");
        self.searching.pack()
        self.searchvideo = Button(self.searching, text="영상 검색", command=self.video, font=("Malgun Gothic", 11),
                                  bg="white");
        self.searchvideo.grid(row=0, column=0, ipadx=15, ipady=2)
        self.searchimage = Button(self.searching, text="이미지 검색", command=self.image, bg="white",
                                  font=("Malgun Gothic", 11));
        self.searchimage.grid(row=0, column=3, ipadx=15, ipady=2)
        self.back = Button(self.window2, text="되돌아가기", command=self.window2.destroy, font=("Malgun Gothic", 11),
                           fg="red", bg="white");
        self.back.pack()

        self.relate()
        self.findPlot()
        self.corrcoef(self.df["Naver"], self.df["Daum"], 2)

        self.window2.mainloop()

    def end(self):
        self.window.destroy()
        ndriver.close()

ndriver = webdriver.Chrome('driver/chromedriver')  # 크롬 드라이버 지정 - 네이버
ndriver.get("https://datalab.naver.com/keyword/realtimeList.naver?where=main")

window = Tk()
window.title("검색어 비교")
window.config(bg="snow")
main(window)
window.mainloop()
