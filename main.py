import keras


parts = ["32316", "32140", "32270", "2780", "32073"]

model = keras.saving.load_model("models/model1.keras")

test_loss, test_acc = model.evaluate(validation_ds, verbose=2)

print("\nTest accuracy:", test_acc)
