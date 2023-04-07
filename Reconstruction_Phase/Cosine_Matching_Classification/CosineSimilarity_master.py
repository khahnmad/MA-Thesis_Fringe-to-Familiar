from Reconstruction_Phase.Cosine_Matching_Classification import High_CosineSimilarity_Classification as update
from Reconstruction_Phase.Cosine_Matching_Classification import Low_CosineSimilarity_Classification as classify

if __name__ == '__main__':
    # Classify new files with 0.97
    classify.run_cosine_classification_low_threshold()
    # Check if old files can be updated
    update.run_cosineimilarity_update()
    # Classify new files with 0.985 threshold
    classify.run_cosine_classification_high_threshold()



