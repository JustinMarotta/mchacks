#Placed Top 5 at McHacks 11 (McGill University Hackathon 2024)!

## Inspiration
We were inspired by Pokemon Go and Duolingo. We believe that exploring the world and learning a new language pair up well together. Associating new vocabulary with real experiences helps you learn better.

- Duolingo but personalized to your immediate environment with computer vision
- Explore the city to build up vocabulary relevant for your environment

## What we’re trying to solve:

Language learning is currently too generic: time is wasted learning words we will never use → needs to be personalised. Learn language relevant to your surroundings while living your daily life.

## What it does
- Explore your surroundings to find landmarks around you. 
- To conquer a landmark you will have to find and photograph objects that represent the vocabulary words we assigned to the land mark. 
- As you conquer landmarks you will level up and more advanced landmarks (with more advanced vocab) will be unlocked.
- Can you conquer all the landmarks and become a Vocab Master?

## How we built it
- We used react native for the app, we used react-native-maps for the map, we used expo camera for the camera, and we used Python for the backend.
- we used Google Cloud Vision API for object recognition and annotated images with identified key object labels
- we used Google Cloud Translate API to translate the names of identified objects to the user's selected target language.
- we used the Gemini API to generate useful questions based on identified objects in the picture the user takes.


## Accomplishments that we're proud of
- Created a unique UI that interfaces with the camera on the user's mobile device
- Creating a landmark exploration map for users to embark on vocabulary challenges
- Creating a quiz functionality using react native that ensures users review their learned vocabulary regularly. This works by requiring users to select the correct translations of words and phrases from previous photos every fifth photo taken.
- Developing a Python backend that takes the URI of an image as input and returns an image annotated with key objects, as well as translations for those objects in selected target language and example sentences using the identified objects in the target language based on the user's surroundings.


## What's next for Pocket Vocab by Purple Cow
-Add additional features to increase social aspects of the app. Such as conquering landmarks by holding the record for largest vocabulary at a certain landmark 
-Incentive business owners to promote themselves through Pocket Vocab by offering to serve as a learning landmark. Increase customer flow!



## Tech Stack:

- Frontend
    - React native
    - Firebase
    - expo-camera

- Backend
    - Flask
    - Python
      - Google Vision, Translate APIs
      - Vertex AI (Gemini API) 
  
