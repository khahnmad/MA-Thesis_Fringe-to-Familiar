from NarrativeExtractionPipeline.Reconstruction_Phase.Pipeline import CosineSimilarity_Update as update
from NarrativeExtractionPipeline.Reconstruction_Phase.Pipeline import CosineSimilarity_Classification as classify

if __name__ == '__main__':
    # Classify new files with 0.97
    # classify.run_cosine_classification_low_threshold()
    # Check if old files can be updated
    update.run_cosineimilarity_update()
    # Classify new files with 0.985 threshold
    classify.run_cosine_classification_high_threshold()



