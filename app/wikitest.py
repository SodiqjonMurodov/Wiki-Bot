import wikipedia

# wikipedia.set_lang("ru")
# print(wikipedia.summary("Wikipedia"))

a = wikipedia.search("Apple III", results=3)
print(a)