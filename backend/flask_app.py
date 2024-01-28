import matplotlib.pyplot as plt
from backend_functions import localize_objects, translate_text, generate_text
from iso639 import Lang

import os

# Set the path to your service account key file
os.environ["GCLOUD_PROJECT"] = "purplecow-5bb60"

# if __name__ == "__main__":

def run_main(photoURI):

    # change this
    load_path = photoURI

    # change this
    save_path = "/Users/justin/Desktop/output_image_with_bounds.jpg"

    source_language = 'English'
    target_language = 'French'

    level = 'beginner'

    # Target must be an ISO 639-1 language code.
    target = Lang(target_language).pt1
    source = Lang(source_language).pt1

    # print("source_lang:", source, "target_lang:", target)

    image_annotated, output_path, objects_list_source, objects_list_target = localize_objects(
        load_path, save_path, source, target)
    

    """
    #translate the identified objects into specified target language
    object_translated_list = []

    for i in range(len(objects_list)):
        
        translated_text = translate_text(target, objects_list[i])
        object_translated_list.append(translated_text)
    
    """

    # print the identified objects and their translations
    #print(f'{source_language} :', objects_list_source)

    # print the objects translations
    #print(f'{target_language} :', objects_list_target)

    # save annotated image to GCS
    img_uri = output_path

    example_sentences_list, original_language_text_list = generate_text(
        'purplecow-5bb60', 'northamerica-northeast1', img_uri, objects_list_target, target_language, source, level)

    examples_prepend = translate_text(source, 'Here are example sentences of using the word(s)')
    #print(f'{examples_prepend}: ')

    """
    for i in range(len(example_sentences_list)):
        print(f'{target_language} :', example_sentences_list[i], f'{source_language} :', original_language_text_list[i])
    """

    # display the annotated image
    #plt.imshow(image_annotated[:, :, ::-1])
    #plt.show()
    
    output_dict = {
        'source_language': source_language,
        'target_language': target_language,
        'annotated_image': image_annotated,
        'objects_list_source_language': objects_list_source,
        'objects_list_target_language': objects_list_target,
        'example_sentences_target_language': example_sentences_list,
        'example_sentences_source_language': original_language_text_list
    }

    print(output_dict)

    return output_dict

if __name__ == "__main__":
    run_main("https://scwcontent.affino.com/AcuCustom/Sitename/DAM/011/news-transport-dec17-continentyinter.jpg")
