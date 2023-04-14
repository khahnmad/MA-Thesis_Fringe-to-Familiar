from Results.locations import *
import universal_functions as uf


keyword_dict = uf.import_json_content(f"{uf.nep_location}Reconstruction_Phase\\Keyword_Identification\\valid_keywords."
                                      f"json")

for pipeline in pipelines:
    for topic in  ["Immigration","Islamophobia","Anti-semitism","Transphobia"]:
        # Get cases in which keyword appears in marg & main
        marg_entities = "20_FR_named_entities.json"

