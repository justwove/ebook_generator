from wrtn_api import make_requests

ebook_subject: str = """
    Je voudrais que tu me crée, en utilisant l'exmple ci dessous, une table des matières pour un ebook qui parlerait
    de {subjet} et qui aurait {number_of_chapters} chapitres. Chaque chapitre aurait {number_of_subchapters} sous-chapitres.

    L'audience cible de cet ebook serait les {target_audience}.

    Tu devras traduire tous les éléments en {language}

    Utilise l'exemple pour créer la table des matières et uniquement la table des matières, ne l'explique pas, ne la présente pas...


    Template:
    Name of the ebook: XXX

    Chapter 1: XXX
    1.1: XXX
    1.2: XXX
    1.3: XXX
    1.4: XXX
    Chapter 2: XXX
    2.1: XXX
    2.2: XXX
    2.3: XXX
    2.4: XXX
    Chapter 3: XXX
    3.1: XXX
    3.2: XXX
    3.3: XXX
    3.4: XXX
    Chapter 4: XXX
    4.1: XXX
    4.2: XXX
    4.3: XXX
    4.4: XXX
    Chapter 5: XXX
    5.1: XXX
    5.2: XXX
    5.3: XXX
    5.4: XXX
"""

chapter_creation: str = """
    
"""

def init_ebook(token, subjet, number_of_chapters, number_of_subchapters, target_audience, language):
    ebook_subject: str = ebook_subject.format(subjet=subjet, number_of_chapters=number_of_chapters, number_of_subchapters=number_of_subchapters, target_audience=target_audience, language=language)
    ai_answer: list[str|list[str]] = make_requests(ebook_subject).split('Chapter')
    title = ai_answer[0].split('Name of the ebook: ')[1].strip()

    chapters = { 
        f'Chapter {chapter.split("\n")[0].strip()}' : {
            f'Subchapter {subchapter.split(":")[0].strip()}': {'name': ''.join(subchapter.split(":")[1]).strip()}
            for subchapter in chapter.split('\n')[1:] 
            if subchapter.split(':') != ['']
        } 
        for chapter in ai_answer[1:]
    }
    for chapter in chapters.values():
        for sub_chapter in chapter.values():
            sub_chapter_name = sub_chapter['name']


if __name__ == '__main__':
    init_ebook(token='',
        subjet='Comment les pandas sont passé d\'ours carnivore en ce que nous conaissont aujourd\'hui', 
        number_of_chapters=5, number_of_subchapters=4, target_audience='Jeunes enfants entre 10 à 15 ans', language='anglais'
    )