from google.cloud import vision
from google.cloud import translate_v2 as translate
import cv2
import numpy as np
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import urllib
import numpy as np
from google.cloud import storage
from PIL import Image
import io

def save_image_jpg(image_array):

    # Create a PIL Image from the NumPy array
    pil_image = Image.fromarray(image_array)

    # Save the image as a JPEG in memory
    jpeg_bytes = io.BytesIO()
    pil_image.save(jpeg_bytes, format='JPEG')

    return jpeg_bytes.getvalue()


#function to translate text into a target language

def translate_text(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """


    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    #print("Text: {}".format(result["input"]))
    #print("Translation: {}".format(result["translatedText"]))
    #print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result["translatedText"]


#Function to annotate image

def annotate_image(objects_list, bounds_list, path, save_path):

    """
    # Load the image
    image_path = path  # Replace with the path to your image
    image = cv2.imread(image_path)
    """
    
    url_response = urllib.request.urlopen(path)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
    image = cv2.imdecode(img_array, -1)

    # Define multiple bounds and corresponding labels
    all_bounds = bounds_list

    #define multiple object labels
    labels = objects_list

    # Convert bounds from float to image coordinates
    height, width, _ = image.shape
    scaled_all_bounds = [
        [(int(b[0] * width), int(b[1] * height)) for b in bounds] for bounds in all_bounds
    ]

    # Draw rectangles, filled rectangles, and labels on the image
    color = (0, 255, 0)  # RGB color, here it's green
    thickness = 2  # Thickness of the rectangle
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    rect_color = (0, 0, 0)  # RGB color, here it's red
    image_with_bounds = image.copy()

    for bounds, label in zip(scaled_all_bounds, labels):
        # Draw the rectangle
        cv2.polylines(image_with_bounds, [np.array(bounds)], isClosed=True, color=color, thickness=thickness)

        # Calculate the position for the text label
        label_position = (bounds[0][0], bounds[0][1] - 10)  # Adjust the offset as needed

        # Check if the label is outside the image dimensions and adjust its position
        label_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]

        # Ensure label stays within the image dimensions
        label_position = (
            max(0, min(label_position[0], width - label_size[0] - 1)),
            max(label_size[1], min(label_position[1], height - 1))
        )

        # Draw the filled rectangle behind the text label
        rect_position = (label_position[0] - 5, label_position[1] - label_size[1] - 5)
        rect_size = (label_size[0] + 10, label_size[1] + 10)

        # Ensure the filled rectangle stays within the image dimensions
        rect_position = (
            max(0, min(rect_position[0], width - 1)),
            max(0, min(rect_position[1], height - 1))
        )

        rect_size = (
            min(rect_size[0], width - rect_position[0]),
            min(rect_size[1], height - rect_position[1])
        )

        cv2.rectangle(image_with_bounds, rect_position, (rect_position[0] + rect_size[0], rect_position[1] + rect_size[1]), rect_color, -1)

        # Add the text label to the image
        cv2.putText(image_with_bounds, label, label_position, font, font_scale, color, font_thickness, cv2.LINE_AA)

    # Save or display the image with bounds
    # cv2.imwrite(save_path, image_with_bounds)

    # Convert OpenCV image to bytes
    _, image_bytes = cv2.imencode('.jpg', image_with_bounds)
    image_bytes = image_bytes.tobytes()
    
    # Save the image to GCS
    BUCKET_NAME = "purplecow-5bb60"
    SOURCE_FILE_NAME = image_bytes
    DESTINATION_FILE_NAME = "annotated_image.jpg"

    upload_blob(BUCKET_NAME, SOURCE_FILE_NAME, DESTINATION_FILE_NAME)
    
    #path to GCS file
    output_path = f"gs://{BUCKET_NAME}/{DESTINATION_FILE_NAME}"
    
    #save image as jpeg
    jpg_image = save_image_jpg(image_with_bounds)
    
    return jpg_image, output_path



#Function to identify objects in an image and return the annotated image as well as a list of the identified objects

def localize_objects(path, save_path, src_language, tgt_language):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    client = vision.ImageAnnotatorClient()

    """
    #open image from file path
    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    """
    
    #image from URI

    image = vision.Image()
    image.source.image_uri = path

    objects = client.object_localization(image=image).localized_object_annotations

    #print(f"Number of objects found: {len(objects)}")
    
    objects_list = [] #get the identified objects
    bounds_list = [] #get the coordinates of the bounding box
    for object_ in objects:
        objects_list.append(object_.name)
        #print(f"\n{object_.name} (confidence: {object_.score})")
        #print("Normalized bounding polygon vertices: ")
        bounds_per_object = []
        for vertex in object_.bounding_poly.normalized_vertices:
            bounds_per_object.append((vertex.x, vertex.y))
            #print(f" - ({vertex.x}, {vertex.y})")
        bounds_list.append(bounds_per_object)
        
    #translate objects list to user input source language (since Vision automaticaly uses english)
    src_translated_object_list = []
    tgt_translated_object_list = []
    for i in range(len(objects_list)):

        src_translated_text = translate_text(src_language, objects_list[i])
        src_translated_object_list.append(src_translated_text)
        
        tgt_translated_text = translate_text(tgt_language, objects_list[i])
        tgt_translated_object_list.append(tgt_translated_text)
        
        
        
    #pass the target translated object list to the annotate_image function
    
    #output objects list in source language
    #objects_list = src_translated_object_list
        
    image_annotated, output_path = annotate_image(tgt_translated_object_list, bounds_list, path, save_path)
    

            
    return image_annotated, output_path, src_translated_object_list, tgt_translated_object_list


#this function will generate the text for the user to practice speaking the target language
#the input is the image uri, the list of objects translated into the target language, the target language, and the difficulty level of the questions
#a project id and location must be specified for the Vertex AI model API to be used (uses Gemini)

#the output text will be 3 questions in the target language that the user can use to practice speaking the target language
#these questions incorporate the identified objects in the image

def generate_text(project_id: str, location: str, img_uri, object_translated_list, target_language, source_language, level) -> str:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    # Load the model
    multimodal_model = GenerativeModel("gemini-pro-vision")
    # Query the model
    response = multimodal_model.generate_content(
        [
            # Add an example image
            Part.from_uri(
                img_uri, mime_type="image/jpeg"
            ),
            # Add an example query
            f"I am trying to imrpove my {target_language} speaking ability. The provided photo displays what I am currently seeing in my environment, please create 3 {level} questions in the {target_language} language using these words '{object_translated_list}'  that I could use to practice learning {target_language} given my surroundings. Ensure there is a question focuses on a different one of the 5 W's (who, what, when, where, why) or how. Do not preface the examples, just provide them. Separate each example with a newline character. Provide numbered examples."
            ,
        ]
    )
    #print(response)
    
    #convert example sentences to list by newline character
    example_sentences_list = response.text.splitlines()
    #print(example_sentences_list)
    
    original_language_text_list = []

    #transale each sentence in list back to english
    for i in range(len(example_sentences_list)):
        
        original_language_text = translate_text(source_language, example_sentences_list[i])
        original_language_text_list.append(original_language_text)
        
    #print(original_language_text_list)
    
    return example_sentences_list, original_language_text_list


#to upload annotated image to GCS

def upload_blob(bucket_name, source_file_bytes, destination_blob_name):
    """Uploads a file to the bucket"""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    #blob.upload_from_filename(source_file_name)
    # Upload the image data to the blob
    blob.upload_from_string(source_file_bytes, content_type='image/jpeg')
