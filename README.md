Company Name: GreenSight Mapping Solutions

Backstory: GreenSight Mapping Solutions is a startup company founded in 2022 by a team of passionate geospatial data scientists and machine learning experts. The company's mission is to revolutionize the way maps are created and analyzed by leveraging cutting-edge technology and innovative approaches.

The founders recognized a significant challenge in the mapping industry: the time-consuming and labor-intensive process of manually identifying and mapping trees from aerial imagery. They saw an opportunity to automate this process using machine learning algorithms, which would not only save time and resources but also provide more accurate and up-to-date information about tree coverage.ה

As a startup, GreenSight Mapping Solutions is working under tight deadlines and limited resources. They have recently started exploring Amazon Web Services (AWS) as a potential platform to deploy their solution, but they are still unsure about the best approach to take.

The company's main objective is to develop a prototype of their tree detection system within a month. They have a dataset of .tif files, which are high-resolution aerial images of various landscapes. The goal is to create a machine learning model that can automatically detect and map trees from these images.

GreenSight Mapping Solutions believes that their automated tree detection system will have a significant impact on various industries, such as urban planning, environmental conservation, and forestry management. By providing accurate and timely information about tree coverage, they can help organizations make better decisions and take action to protect and preserve green spaces.


Technical: 
Machine Learning Model: The tree detection model is based on the Detectree model (https://github.com/martibosch/detectree), which is a state-of-the-art deep learning model specifically designed for tree detection in aerial imagery. The Detectree model utilizes a convolutional neural network (CNN) architecture to identify and locate trees in the input images.

the Model pkl file is: “tree_model_new” is use by the next code:

    clf = pickle.load(open('tree_model_new', 'rb'))
    clf_model = dtr.Classifier(clf=clf)


and predict by:

clf_model.predict_img(f'{OUTPUT_PNG_SPLIT}/{png_name}')


The implementation of this project is based on 3 pipelines:

![IO Diagram](diagrams/green-architecture-diagram.drawio.png)
![IO Diagram](gree-architectur-diagram-continue.drawio.png)
