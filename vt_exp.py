import vt

client = vt.Client("af9889b1ac5252295be7c42329e58745cda16cfabe652225fb80a22230464dea")

# file = client.get_object("/Users/jessica/Downloads/dataSample/0A32eTdBKayjCWhZqDOQ.bytes")

with open("/Users/jessica/Downloads/dataSample/0A32eTdBKayjCWhZqDOQ.bytes", "rb") as f:
    analysis = client.scan_file(f, wait_for_completion=True)
    
print(analysis.results)