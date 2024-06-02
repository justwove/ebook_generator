from wrtn_api import make_requests

from json import dumps
from tqdm import tqdm
from icecream import ic

import asyncio


ebook_subject: str = """
    Je voudrais que tu me crée, en utilisant l'exmple ci dessous, une table des matières pour un ebook qui parlerait
    de {subjet} et qui aurait {number_of_chapters} chapitres. Chaque chapitre aurait {number_of_subchapters} sous-chapitres.

    L'audience cible de cet ebook serait les {target_audience}.

    Pour le tire de l'ebook, rédige un titre court et accrocheur qui s'adresse clairement à notre lecteur, qui comporte moins de 9 mots et qui propose une « grande promesse » qui ne manquera pas d'attirer l'attention du lecteur.

    Tu devras impérativement traduire tous les éléments en {language} sans exception.

    Utilise l'exemple pour créer la table des matières et uniquement la table des matières, ne l'explique pas, ne la présente pas et ne rajoute pas de saut de ligne, donne moi UNIQUEMENT les information demandé...

    Répond moi uniquement sous la forme de la templaate, ne rajoute pas de saut de ligne, ne rajoute pas de caractère supplémentaire, ne rajoute pas de ponctuation, ne rajoute pas de caractère spécial, ne rajoute pas de caractère de fin de ligne, ne rajoute pas de caractère de fin de fichier, ne rajoute pas de caractère de fin de texte, ne rajoute pas de caractère de fin de document, ne rajoute pas de caractère de fin de message, ne rajoute pas de caractère de fin de conversation, ne rajoute pas de caractère de fin de discussion, ne rajoute pas de caractère de fin de chat
    
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
    Je voudrais que tu me developpe le sous chapitre {subchapter} de l'ebook que tu as crée précédemment. Ce chapitre devra contenir entre 450 et 600 mots.
    Le sujet global de l'ebook est {subjet} et le chapitre que tu vas écrire doit être en lien avec ce sujet tout en respectant le {chapter} et le {subchapter} que tu as crée précédemment.
    
    Le résultat doit être aussi utile que possible au lecteur. Inclure des faits quantitatifs et des statistiques, avec des références. 
    Approfondissez autant que nécessaire. Vous pouvez diviser ceci en plusieurs paragraphes si vous le souhaitez. 
    Le résultat doit également être présenté sous forme de paragraphes cohérents. 
    
    Tu devras impérativement parler du {subchapter} en lien avec le sujet global de l'ebook en {language} sans exception

    N'incluez pas de parties « [Insérer ___] » qui nécessiteront une édition manuelle par la suite. 
    Si vous vous trouvez dans l'obligation d'insérer [blanc] n'importe où, ne le faites pas (c'est très important). 
    Si vous ne savez pas quelque chose ou que vous n'avez pas assez d'information, ne l'incluez pas dans le résultat. 
    
    Tu devras impérativement traduire tous les éléments en {language} sans exception.

    Utilise l'exemple ci-dessous pour créer le sous-chapitre et uniquement le sous-chapitre, ne l'explique pas, ne le présente pas...

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum at blandit mauris. In vitae iaculis felis. In sed laoreet ligula, ut molestie urna. Quisque tellus velit, placerat eget aliquam sed, imperdiet et libero. Nam ut magna et sapien varius lacinia quis sed tortor. Phasellus dapibus mi nec sapien fringilla aliquam. Donec hendrerit mauris eu pellentesque facilisis.

    Nunc et nisi eros. Donec diam mauris, finibus quis hendrerit ut, scelerisque vitae sem. Sed eleifend consequat nunc sed tincidunt. Donec id lectus molestie, mollis ante eu, vulputate tellus. Aliquam turpis felis, consequat nec pulvinar non, interdum sit amet turpis. Nulla porttitor quis nisl nec varius. Maecenas porttitor dignissim nisl, eu mollis mauris efficitur eu. Suspendisse vel magna diam. Morbi consequat iaculis arcu, id congue elit facilisis eu. Vivamus posuere ultricies volutpat. Integer vehicula feugiat interdum. Nullam id mi volutpat, malesuada elit eget, iaculis augue. Interdum et malesuada fames ac ante ipsum primis in faucibus. Duis nisl arcu, aliquet et diam at, faucibus bibendum nibh. Nullam dui nunc, efficitur ut efficitur eget, pretium non felis. In et nisl in urna eleifend sodales eget sit amet massa.

    Quisque ultricies lorem sem. Quisque massa nisl, imperdiet condimentum imperdiet nec, fringilla vitae libero. Aenean ac rutrum ipsum. Praesent tincidunt libero lorem, sed ultricies tellus laoreet eu. Proin elementum libero non rutrum sollicitudin. Nulla id sollicitudin tortor. Nam commodo tortor in pellentesque vehicula. Vivamus vel odio diam. Sed convallis ligula enim, sit amet porttitor mauris vulputate condimentum. Aenean eget viverra nisl. Integer pharetra quam nec eros malesuada, vel ultricies enim iaculis.

    Proin bibendum lacus eu lorem blandit, ut luctus lorem venenatis. Sed aliquam consequat varius. Etiam vestibulum lectus sed faucibus pretium. Sed efficitur dui non arcu molestie, vel auctor turpis rutrum. Phasellus mollis est quis dolor tincidunt, eget tincidunt nulla imperdiet. Donec non sem eget ligula ultricies commodo. Curabitur id lacus ut nisi ultricies fermentum in eget urna.

    Integer sed placerat odio. In ex tortor, tristique ut elit vitae, condimentum congue dolor. Nam facilisis enim ac quam vulputate, et fringilla nisi porttitor. Pellentesque efficitur, quam eget ultrices sollicitudin, lectus metus aliquam lorem, vel molestie tortor lectus eget felis. Donec dignissim mauris nec sollicitudin porttitor. Phasellus velit diam, lobortis at dignissim et, placerat vitae enim. Ut ultrices a sem vel rutrum. Aliquam varius placerat ex, at scelerisque erat dictum id. Integer eget leo a elit sagittis porttitor at pretium elit. Nam ornare vestibulum cursus.

    In mollis enim et erat sagittis auctor. Aliquam erat volutpat. Donec blandit dictum massa. Aliquam rhoncus a lorem quis ultricies. Donec eget metus rutrum, rhoncus arcu in, auctor elit. Quisque lacinia bibendum sagittis. Sed eu tincidunt ex. Maecenas porta enim feugiat leo eleifend, eget consequat risus ultricies. Suspendisse rutrum, est sed pretium porta, libero libero viverra mauris, vitae sagittis diam nunc laoreet velit. Fusce eget porta elit. Nulla facilisi. Nullam lacinia blandit interdum. Sed ac viverra sem, at semper metus.

    Sed at ligula tempor, commodo nulla nec, facilisis risus. Vivamus commodo volutpat arcu, in scelerisque massa finibus at. Nullam velit nisl, sollicitudin et lorem id.
"""

def init_ebook(token, subjet, number_of_chapters, number_of_subchapters, target_audience, language, ebook_subject, chapter_creation):
    ebook_subject: str = ebook_subject.format(subjet=subjet, number_of_chapters=number_of_chapters, number_of_subchapters=number_of_subchapters, target_audience=target_audience, language=language)
    ic('Asking AI to create ebook table of content')
    ai_answer: list[str|list[str]] = make_requests(token, ebook_subject)
    # ic(ai_answer)
    ai_answer = ai_answer.split('Chapter')
    title = ai_answer[0].partition(':')[-1].strip()
    # ic('Book started')
    ic(title)
    ic(ai_answer)

    chapters = { 
        f'Chapter ' + chapter.split('\n')[0] : {
            f'Subchapter {subchapter.split(":")[0].strip()}': {'name': ''.join(subchapter.split(":")[-1]).strip()}
            for subchapter in chapter.split('\n')[1:] 
            if (subchapter.split(':') != ([''] or ['\n'] or ['\t']) and subchapter != '')
        } 
        for chapter in ai_answer[1:]
    }

    ic('Chapters splited and created', chapters)
    for chapter, sub_chapters in chapters.items():
        for sub_chapter_id, sub_chapter_dict in tqdm(sub_chapters.items()):
            sub_chapter_name = f'{sub_chapter_id} : {sub_chapter_dict["name"]}'
            chapter_creation: str = chapter_creation.format(subchapter=sub_chapter_name, subjet=subjet, chapter=chapter, language=language)
            ai_answer: str = make_requests(token, chapter_creation)
            chapters[chapter][sub_chapter_id]['content'] = ai_answer.partition(':')[-1].replace('\n', '\n\n')
    # ic(title, chapters)
    print(title)
    with open(f'output/{title}.json', 'w') as f:
        f.write(dumps(chapters, indent=4))
    # print(dumps(chapters, indent=4))
    # return chapters, title


if __name__ == '__main__':
    init_ebook(token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1MWU5NjJmYzY2OWRmYjAxNTgxYjk3OSIsImVtYWlsIjoic2dhc3NhY2t5c0BnbWFpbC5jb20iLCJ3cnRuVWlkIjoiOHV6dnFDUDQ2VTgtR0dLT1FVVlVTamhGIiwiaXNzdWVyIjoid3J0biIsImlhdCI6MTcxNzI0OTQ2NywiZXhwIjoxNzE3MjUzMDY3fQ.1PqaZZPZElhn-QJW8J7o6nxQmqato01xlH2QS4CXF18',
        subjet='Comment les pandas sont passé d\'ours carnivore en ce que nous conaissont aujourd\'hui', 
        number_of_chapters=5, number_of_subchapters=4, target_audience='Jeunes enfants entre 10 à 15 ans', language='anglais',
        ebook_subject=ebook_subject, chapter_creation=chapter_creation
    )