'''def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


ListToChunk = input("Give me some text to chunk")

AfterChunking = chunks(ListToChunk, 5)

print(AfterChunking)'''

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

ListToChunk = input("Give me some text to chunk")

AfterChunking = chunks(ListToChunk, 5)

print(AfterChunking)