from lxml import etree
import functools
import urllib

str1=open('/home/kevin/wsp/underrail-feats.html').read()
root1=etree.fromstring(str1)
xpath1='/table/tr/td/table'
str1=etree.tostring(root1.xpath(xpath1)[0]).decode('utf8')

fname='/home/kevin/win10/underrail/out.tsv'

def writefile(fname, str1):
    f=open(fname, 'w')
    f.write(str1)
    f.close()
    return

def reducereplace(str1):
    to_blank=[str1, "b' ", "\\n'"]
    res_str=functools.reduce(lambda a,b: a.replace(b, ""), to_blank)
    to_space="\\xc2\\xa0"
    res_str=res_str.replace(to_space, " ")
    to_minus="\\xe2\\x80\\x91"
    res_str=res_str.replace(to_minus, "-")
    return res_str

def getfeats(url1):
    url1='http://www.underrail.com'+url1
    print('fetching ' + url1)
    ## get desc page
    root1=etree.HTML(urllib.request.urlopen(url1).read())
    ## description
    # filter1='/html/body/div [@id="content"]/div [@id="bodyContent"]/div [@id="mw-content-text"]/table [@class="infobox"]/tr [2]/td'
    # desc=root1.xpath(filter1)[0].text
    filter1='/html/body/div [@id="content"]/div [@id="bodyContent"]/div [@id="mw-content-text"]/table [@class="infobox"]/tr [2]/td/text()'
    desc=root1.xpath(filter1)
    
    ## requirements
    filter2='/html/body/div [@id="content"]/div [@id="bodyContent"]/div [@id="mw-content-text"]/table [@class="infobox"]/tr [3]/td/ul/li//text()'
    reqs=root1.xpath(filter2)
    reqs=[el for el in reqs if el != ' ']
    reqs=','.join(reqs)
    desc.append(reqs)
    desc=list(map(lambda x: x.replace('\n',''), desc))
    desc=list(map(lambda x: x.replace('\t',' '), desc))
    # print(desc)
    
    return desc
    
    
def exec1():
    filter0='/table/tr/td/table'
    # writefile(fname, etree.tostring(root1.xpath(filter0)[0]).decode('utf8'))
    # filter1='/table/tr/td/table/tr[string-length(td) &gt; 0]'
    filter1='/table/tr/td/table/tr [count(td) > 1]'
    filter2=''

    f=open(fname, 'w')
    for atag1 in root1.xpath(filter1):
        # lvl=etree.tostring(atag.xpath('td[1]')[0].text).decode('utf8')
        # lvl=atag1.xpath('td[1]')[0].text.encode('utf-8', 'ignore').decode('utf8', 'ignore')
        lvl=reducereplace(str(atag1.xpath('td[1]')[0].text.encode('utf-8', 'ignore')))
        # print(lvl)
        ## datas
        for atag2 in atag1.xpath('td[2]/div/a'):
            res=[lvl, atag2.text]

            ## include details
            details=getfeats(atag2.get('href'))
            res.extend(details)

            f.write('\t'.join(res) + '\n')

    f.close()
    return

# root2.xpath('/html/body/div [@id="content"]/div [@id="bodyContent"]/div [@id="mw-content-text"]/')
# etree.tostring(root2.xpath('/html/body/div [@id="content"]/div [@id="bodyContent"]/div [@id="mw-content-text"]/table [@class="infobox"]/tr')[0], pretty_print=True)
# etree.tostring(root2.xpath('/html/body/div [@id="content"]/div [@id="bodyContent"]/div [@id="mw-content-text"]/table [@class="infobox"]/tr [2]/td')[0], pretty_print=True)



exec1()
