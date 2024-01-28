# Pocket Vocab Mobile App
## Placed Top 5 at McHacks 11 (McGill University Hackathon 2024)!

<img width="734" alt="Screenshot 2024-01-28 at 3 34 11 PM" src="https://github.com/JustinMarotta/mchacks/assets/109969478/f7bc9e3b-acb3-4216-8672-804a93a9f6fe"> <img width="207" alt="Screenshot 2024-01-28 at 4 44 59 PM" src="https://github.com/JustinMarotta/mchacks/assets/109969478/f8899b52-6f6f-4804-b570-129e8c14480f">

![d02dd0d969d86320f69d268fbf23fc129c0362ae0cf659a23db663383165aa78 - instasize](https://github.com/JustinMarotta/mchacks/assets/109969478/35c98575-3046-432f-be74-955402c0ef20)

## Inspiration
We were inspired by Pokemon Go and Duolingo. We believe that exploring the world and learning a new language pair up well together. Associating new vocabulary with real experiences helps you learn better.

- Duolingo but personalized to your immediate environment with computer vision
- Explore the city to build up vocabulary relevant for your environment

## Problem we’re trying to solve:

Language learning is currently inefficient and too generic. Time is wasted learning words we will never use → needs to be personalized for faster improvement and better retention. Our solution helps users learn language relevant to their surroundings while living their daily lives.

## What it does
- Explore your surroundings to find landmarks around you. 
- To conquer a landmark you will have to find and photograph objects that represent the vocabulary words we assigned to the landmark. 
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


## What's next for Pocket Vocab
-Add additional features to increase the social aspects of the app. Such as conquering landmarks by holding the record for the largest vocabulary at a certain landmark 
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
  
