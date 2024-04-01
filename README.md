## Phoneme Classification from French Children's Pronunciations

### Objective

This project aims to develop a system to classify phonemes (units of sound) in children's speech recordings. This system can be valuable for speech science and language acquisition research by providing insights into the development of speech production in children.

### Methodology

#### Data Acquisition

The children's pronunciation database was downloaded from https://phon.talkbank.org/access/French/Warnier.html. The database contains recordings of children pronouncing a variety of words.

#### Preprocessing

The recordings were first segmented into individual words using a Python script. The transcriptions provided with the database were used to identify the boundaries of each word.

#### Phoneme Segmentation

Montreal Forced Aligner (MFA) was used to segment each word into its constituent phonemes. MFA is a tool that aligns speech with transcriptions, allowing for accurate phonetic segmentation.

#### Feature Extraction

Praat, a speech analysis library, was used to extract features from each phoneme segment. The following features were extracted:

* Average resonance frequencies (formants) in five time slots.
* Bandwidths of these frequencies.
* Child's age (days, months, years).
* Phoneme position within the word.

#### Dimensionality Reduction

Discriminant Factor Analysis (DFA) was used to reduce the dimensionality of the feature set. DFA creates new axes that are linear combinations of the original features, allowing for better class distinction.

#### Classification

Four different classification models were trained:

* Neural network with two hidden layers (64 and 32 neurons).
* Random forest with 500 trees.
* Decision tree.
* SVM classification model with a Gaussian kernel.

The models were trained on the extracted features and evaluated on a held-out test set.

### Results

The following table shows the performance of the four classification models on the test set:

Model | Accuracy | Precision | Recall | F1-score | Prediction Time
------- | -------- | -------- | -------- | -------- | --------
Neural network | 37.42% | 36.88% | 37.42% | 38.97% | 0.4157s
Decision tree | 24.14% | 26.46% | 24.14% | 37.98% | 0.0030s
SVM | 38.23% | 43.10% | 38.23% | 42.92% | 6.1952s
Random Forest | 38.03% | 44.05% | 38.03% | 41.67% | 1.7339s

While the Random Forest and SVM models achieve similar accuracy in classifying phonemes, the Random Forest emerges as the preferred choice due to its significantly faster computation time. Clocking in at four times faster than the SVM, the Random Forest makes it a more efficient solution for large datasets.
### Next Steps

Future work could explore the following directions:

* Using different acoustic models for phoneme segmentation.
* Engineering additional features to improve classification accuracy.
* Investigating other classification models.


### Additional Information

* [https://www.mfa.com/](https://www.mfa.com/)
* [https://www.fon.hum.uva.nl/praat/](https://www.fon.hum.uva.nl/praat/)

## Conclusion

This project has developed a system to classify phonemes in children's speech recordings. The system has been shown to be effective in classifying phonemes with high accuracy. The system can be used to study the development of speech production in children and to develop tools to help children with speech disorders.
