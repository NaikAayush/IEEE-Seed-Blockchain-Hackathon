from googletrans import Translator

def transalation(input_string,input_language,output_language="en"):
    translator=Translator()
    translated = translator.translate(input_string,src=input_language,dest=output_language) 
    # print(translated)
    return translated.text


print(transalation('India is seed',input_language='en',output_language='hi'))