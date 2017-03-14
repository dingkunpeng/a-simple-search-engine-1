def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node])
            
            newranks[page] = newrank
        ranks = newranks
    return ranks

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ''

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]
        
def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def add_page_to_index(index,url,content):
    words = content.split()
    for word in words:
        add_to_index(index,word,url)

def crawl_web(seed,max_depth):
    tocrawl = [seed]
    crawled = []
    index = {}
    next_depth = []
    graph = {}
    depth = 0
    while tocrawl and depth <= max_depth:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
        if not tocrawl:
            tocrawl,next_depth = next_depth, []
            depth = depth + 1
    return index,graph

def lucky_search(index,ranks,keyword):
    pages = lookup(index,keyword)
    if not pages:
        return None
    best_page = pages[0]
    for condidate in pages:
        if ranks[condidate] > ranks[best_page]:
            best_page = condidate

    return best_page


index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html',3)

ranks = compute_ranks(graph)

print lucky_search(index,ranks,'Hummus')
