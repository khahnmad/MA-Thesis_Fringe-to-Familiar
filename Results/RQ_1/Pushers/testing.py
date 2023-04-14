# Where did these Ids come from ?
ids = ['1180604763', '1180739884', '1180797884', '1180805854', '1180864984', '1180867187', '1180979329', '1181150894', '1181093294', '1181166302', '1181171125', '1181171981', '1181257565', '1181233008', '1181289535', '1181301840', '1181297052', '1181299740', '1181352688', '1181349616', '1181349608', '1181349601', '1181393711', '1181374977', '1181432240', '1181444474', '1181529865', '1181671147', '1181645731', '1181700133', '1181743425', '1181875555', '1181828626', '1181830947', '1181952577', '1182138253', '1182162813', '1182328847', '1182328834', '1182341845', '1182350022', '1182341834', '1182423890', '1182429127', '1182431315', '1182453553', '1182453557', '1182436454', '1182492938', '1182489188', '1182528676', '1182533123', '1182553316', '1182649575', '1182649608', '1182641115', '1182818268', '1182820597', '1182753117', '1182814252', '1182801147', '1182814311', '1182908470', '1183068450', '1183017076', '1183165258', '1183158002', '1183172481', '1183166946', '1183278837', '1183279736', '1183279720', '1183356679', '1183465601', '1183534270', '1183534263', '1183534257', '1183534252', '1183600622', '1183723710', '1183731498', '1184163973', '1184163976', '1185563132', '1217044748', '1219214912', '1220950607', '1220951745', '1232838665', '1242194820', '1574044245', '1953136908', '1183337168', '1183389456', '1183475805', '1183449681', '1183449667', '1183449699', '1183600620', '1183811646']

import universal_functions as uf

# # datasets = uf.load_all_complete_datasets()
# # for d in datasets:
# #     data = uf.import_csv(d)
# #     for row in data:
# #         if row[0] in ids:
# #             print(d)
# #             if "Left_2-2016" in d:
# #                 print('HEY')
#
# # Left 2016 cosine class appears to already be contaminated - how extensive is this?
#
# # Cosine 97 20
# # cosine_97_loc = f"{uf.nep_location}BertClusteringClassification\\CosineClassification\\Left_2-2016_EmbCOMPLETE.pkl"
# # cosine_98_loc = f"{uf.nep_location}Reconstruction_Phase\\Cosine_Matching\\Left_2-2016_EmbCOMPLETE.pkl"
# #
# # low = uf.import_pkl_file(cosine_97_loc)
# # high = uf.import_pkl_file(cosine_98_loc)
#
# # Inner Layer
# inner_loc_incomplete = f"{uf.nep_location}Reconstruction_Phase\\Keyword_Matching\\Left_2-2016_Emb169000.pkl"
# inner_loc = f"{uf.nep_location}Reconstruction_Phase\\Keyword_Matching\\Left_2-2016_EmbCOMPLETE.pkl"
#
# # incomplete = uf.import_pkl_file(inner_loc_incomplete)
# # complete = uf.import_pkl_file(inner_loc)
# print('check')
#
# # Embeddings
# # emb_loc = f"{uf.thesis_location}locally_createEmbeddings\\Embeddings\\Left_2-2016_embeddings.pkl"
# # data = uf.import_pkl_file(emb_loc)
# print('check')
#
# sro_loc = f"{uf.nep_location}SRO_Instances\\Left_2-2016_SRO.json"
# data= uf.import_json_content(sro_loc)
# print('check')

test = uf.load_all_complete_datasets()
print('check')