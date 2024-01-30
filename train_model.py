from pathlib import Path
import keras
import datetime

image_size = (256, 256)

parts = ["32316", "32140", "32270", "2780", "32073"]

training_data_path = "./pictures/edited"

training_ds, validation_ds = keras.utils.image_dataset_from_directory(
    training_data_path,
    labels="inferred",
    label_mode="int",
    class_names=parts,
    color_mode="grayscale",
    batch_size=32,
    image_size=image_size,
    seed=1234,
    validation_split=0.2,
    subset="both",
)


model = keras.Sequential([
    keras.Input(shape=image_size),
    keras.layers.Flatten(),
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(5)
])


model.compile(optimizer='adam',
              loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.fit(training_ds,
          epochs=10,
          validation_data=validation_ds,
          callbacks=[tensorboard_callback])

test_loss, test_acc = model.evaluate(validation_ds, verbose=2)

print('\nTest accuracy:', test_acc)

Path("models/").mkdir(parents=True, exist_ok=True)
model.save("models/model1.keras")
