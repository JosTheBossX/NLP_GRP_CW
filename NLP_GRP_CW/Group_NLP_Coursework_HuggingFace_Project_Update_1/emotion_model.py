import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa

from constance_data import emotion_track_list, decode_cut_list
from pre_processing_data import preprocessing_data, pre_processing_data_2, text_transform, user_capture


def emotion_predict(sentence: str):
    lr = 1e-3
    wd = 1e-4 * lr
    model = tf.keras.models.load_model("model/nlp_surrey_coursework_hunglenhat")
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=tfa.optimizers.AdamW(learning_rate=lr, weight_decay=wd), metrics=['accuracy'])
    sentence_temp = sentence
    sentence = pre_processing_data_2(sentence)
    if not sentence:
        sentence = preprocessing_data(sentence)

    sentence = text_transform(sentence)
    try:
        sentence = model.predict(sentence)
    except Exception as E:
        print(E)
    index_max = np.argmax(sentence)
    result = emotion_track_list[decode_cut_list[index_max]]
    user_capture(sentence_temp, result)
    return result
