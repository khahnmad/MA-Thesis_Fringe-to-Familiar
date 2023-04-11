import universal_functions as uf

# Kmeans files
kmeans_folder = uf.repo_loc / 'Reconstruction_Phase/Kmeans_Clustering/output'
kmeans_97_20 = [x for x in uf.get_files_from_folder(str(kmeans_folder / 'threshold_97'),"pkl") if "0.2" in x]
kmeans_97_30 = [x for x in uf.get_files_from_folder(str(kmeans_folder / 'threshold_97'),"pkl") if "0.3" in x]

kmeans_98_20 = [x for x in uf.get_files_from_folder(str(kmeans_folder / 'threshold_985'),"pkl") if "0.2" in x]
kmeans_98_30 = [x for x in uf.get_files_from_folder(str(kmeans_folder / 'threshold_985'),"pkl") if "0.3" in x]

