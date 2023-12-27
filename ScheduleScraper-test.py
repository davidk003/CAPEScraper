import pandas as pd
from bs4 import BeautifulSoup
with open("test.html")as f:
    soup = BeautifulSoup(BeautifulSoup(f, "lxml").prettify(), "lxml")
thing = soup.findAll("table")[1]

toRemove = thing.findAll(["br", "img"])
for item in toRemove:
    item.decompose()
toUnwrap = thing.findAll(["span", "a"])
for item in toUnwrap:
    item.unwrap()


print(len(thing.findAll("td", {"colspan" : "13"})))
print(thing.findAll("td", {"colspan" : "13"})[2].decompose())

with open("table.html", "w") as f:
    f.write(str(thing.prettify()))
    frames = pd.read_html("table.html")

# tds = thing.findAll("td")
# arr = []
# for str in tds[101].replace_with():
#     print(str)
# for td in tds:
#     if td is None:
#         print(td.children)
#     else:
#         arr.append(td.string.strip())
# print(arr)

thingy = thing.findAll(class_=["sectxt", "nonenrtxt"])

x = frames[0].map(lambda x: x.strip() if isinstance(x, str) else x)
# print(x)
# print(x.columns)
# print(x.iloc[:3,])

with open("test.txt", "w") as f:
    f.write(x.to_string())

with open("table-thingy.html", "w") as f:
    for t in thingy:
        f.write(str(t))


x.to_csv("table.csv")