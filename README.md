This project introduces a sophisticated curb detection and segmentation system developed to address the challenges in autonomous driving and road feature analysis. The system is built on a robust framework that combines cutting-edge deep learning models with an intuitive user interface, ensuring efficient processing and user-friendly interaction.

### Backend Architecture

The backbone of the project's backend is the YOLOv7 network, known for its superior object detection capabilities. This network is augmented with a fully convolutional neural network (FCNN) for semantic segmentation, enabling the precise identification and segmentation of curbs from video data. The FCNN operates by extracting a feature matrix from the images, allowing for detailed analysis and segmentation beyond traditional detection methods. This innovative approach ensures the system's capability to handle complex visual data and perform segmentation with high accuracy.

### Frontend Design

On the frontend, the project utilizes PyQt for its graphical user interface (GUI), providing users with a straightforward and efficient means to interact with the system. The GUI supports video loading, playback control, model management, and data labeling functionalities. User actions, such as clicking buttons or adjusting settings, trigger backend processes via a signal-slot mechanism, facilitating seamless operation between the user interface and the processing backend.

### Model Training and Parameter Tuning

Model training and parameter tuning are crucial for achieving optimal system performance. The project leverages a curated dataset from the Mapillary Vistas, consisting of 18,000 high-resolution images. This dataset was meticulously prepared, selecting six representative classes from 60 instance types, ensuring a comprehensive training set. Preprocessing steps include resizing images to 640x650 pixels and scaling pixel values to a 0-1 range, enhancing numerical stability and model compatibility.

Data augmentation techniques, such as Mosaic and Mixup, were employed to enhance the dataset's diversity and improve the model's generalization ability. These techniques are vital for preparing the model to handle various road conditions, curb types, and environmental factors.



### Conclusion

Developed as an undergraduate graduation project over the course of four months, this system showcases the application of advanced deep learning techniques to solve practical problems in the field of autonomous driving. It stands as a testament to the developer's ability to independently tackle complex challenges in computer vision and deep learning, from the initial design phase through to the implementation of both the backend processing mechanisms and the frontend user interface.

You can check out the [demo video](https://4jm33x-my.sharepoint.com/:p:/g/personal/aaronjiahao0210_4jm33x_onmicrosoft_com/EV7jwsTTtZBBhXNPpRSAiLABdm6HQUgkF_ZCHdbRNKgYdQ?e=7e76rQ).