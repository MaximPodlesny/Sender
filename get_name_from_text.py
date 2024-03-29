# from g4f.client import Client
# # import g4f

# def get_name(text: str) -> str:
#     client = Client()
#     response = client.chat.completions.create(
#         model= "gpt-3.5-turbo",
#         messages=[{"role": "user", "content": f"выдели в этом выражении '{text}' имя человека и пришли мне только имя человека на русском языке, в таком формате: 'Имя человека в данном выражении: Юлия'. Пришли только имя!"}]
#     )
#     return response.choices[0].message.content #.split(' ')[-1]
# # print(response)
# print(get_name('@elena.struchkova_'))

from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)


segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)


def find_name(text):
    try:
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.parse_syntax(syntax_parser)
        doc.tag_ner(ner_tagger)

        
        return [i.text for i in doc.spans if i.type=='PER']
    except:
        return False
    
print(find_name('Нас называли maxim'))