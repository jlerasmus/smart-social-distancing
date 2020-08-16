import tensorflow as tf
import numpy as np
import pathlib
import time
from libs.detectors.utils.fps_calculator import convert_infr_time_to_fps


def load_model(model_name):
    # base_url = 'Not Available'
    # model_file = model_name + '.tar.gz'
    # model_dir = tf.keras.utils.get_file(
    #     fname=model_name,
    #     origin=base_url + model_file,
    #     untar=True)

    # model_dir = pathlib.Path(model_dir) / "saved_model"
    model_dir = 'data/x86/face_mask'  # TODO: load automatically after providing a proper model

    model = tf.saved_model.load(str(model_dir), None)
    print('Classifier model signatures: ', list(model.signatures.keys()))
    model = model.signatures[
        'predict']  # 'predict' signature was defined during exporting pb model change it if your signiture is someting else

    return model


class Classifier:
    def __init__(self, config):
        self._config = config
        self.model_name = self.config.get_section_dict('Classifier')['Name']
        self.classifier_model = load_model(self.model_name)
        # Frames Per Second
        self.fps = None

    def inference(self, resized_rgb_image):
        input_image = np.expand_dims(resized_rgb_image, axis=0)
        input_tensor = tf.convert_to_tensor(input_image, dtype=tf.float32)
        t_begin = time.perf_counter()
        output_dict = self.detection_model(input_tensor)
        inference_time = time.perf_counter() - t_begin  # Seconds
        # Calculate Frames rate (fps)
        self.fps = convert_infr_time_to_fps(inference_time)

        result = np.argmax(output_dict['scores'].numpy())  # returns class id
        return result
