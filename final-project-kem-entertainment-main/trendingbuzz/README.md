~~~~~~~~~~~~~~~DEPLOYMENT~~~~~~~~~~~~~~~~~~~
If you wish to deploy this on your own, you will need to setup a google generativeai api key under your respective Google Secrets API.
Make sure to name this api key as 'genai-api-key' under the secrets tab to allow cloudbuild to recognize it.
In addition, for the mood match page, to generate an image using vertex AI, you will need your project id to ensure it works smoothly.

You will also need to create an image in artifact registry using your own GCP project id, with the name of your choice.
When that is complete, replace the following line in the Dockerfile with your project id, name of registry, and a chosen image name respectively.
"us-west2-docker.pkg.dev/{YOUR-PROJECT-ID}/{YOUR-REGISTRY}/{IMAGE-NAME}"

~~~~~~~~~~~~~~~TRENDING BUZZ~~~~~~~~~~~~~~~~
The final design was changed from the original Figma mock to accomodate for the multi-page layout of our app. The elements previously on the left side of the page
have been moved to the right as the left sidebar will be reserved for navigating through pages. There are also new elements present in the form of a section for 
generating the top ten terms of the day, as well as downloading them to your local device. Exact styling specs have also changed, mostly due to time constraints
and focusing on the technical aspects of the project.


~~~~~~~~~~~~~~~MOOD MATCH~~~~~~~~~~~~~~~~
The final design was changed from the original Figma mock to accomodate for the multi-page layout of our app. A side bar was added for navigating through pages. There are also new elements present in the form of generating an image depending on the mood selected, as well as downloading them to your local device. The 'Get Recommendations' button has become automated to reduce the number of buttons a user needs to manually select on the page and make the page loading process even faster.
Some other changes were made to the styling to ensure consistency with my teammates' pages. The color scheme better suited the concept of our app and looks more appealing to the eyes