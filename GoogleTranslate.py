from googletrans import Translator

def transalation(input_string,input_language,output_language="en"):
    translator=Translator()
    translated = translator.translate(input_string,src=input_language,des=output_language) 
    return translated.text


# print(transalation('veritas lux mea',input_language='la'))