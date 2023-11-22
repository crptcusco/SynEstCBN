# # Calculate the Attractors by RDDA and by Signal with Prof Luis Method
# # result = RedRddasModel.assembly_attractor_fields_optimized.remote(oRedRddasModel)
# # oRedRddasModel = ray.get(result)
#
# # return list(set(li1) - set(li2)) + list(set(li2) - set(li1))
# def f_diference(v_e_1, v_e_11):
#     l_res = []
#     for v_pair in v_e_1:
#         if not v_pair in v_e_11:
#             l_res.append(v_pair)
#     return l_res
#
# # return the rdda of each attractor of the pair
# def f_netMapping(v_pair):
#     elements = list()
#     for i in range(2):
#         net_aux = 0
#         for net, rddas_attractor in enumerate(oRedRddasModel.rddas_attractors):
#             net_aux = net
#             check_net = v_pair[i] in rddas_attractor
#             if check_net:
#                 break
#         elements.append(net_aux + 1)
#     return elements
#
# # function to get unique values
# def f_unique(list1):
#     # initialize a null list
#     unique_list = []
#     # traverse for all elements
#     for x in list1:
#         # check if exists in unique_list or not
#         if x not in unique_list:
#             unique_list.append(x)
#     return unique_list
#
# def f_leque(j):
#     pass
#
# # return a subgraph part of attractor field
# def f_visita(v_tam_caminho,v_pair,l_palette):
#     # find the rdd of j in [i,j]
#     v_rdd_aux = f_netMapping(v_pair)[0]
#     l_palette.append(v_rdd_aux)
#     if v_tam_caminho == oRedRddasModel.number_of_rddas and l_palette == oRedRddasModel.number_of_rddas:
#         return v_pair
#     else:
#         if v_tam_caminho <= oRedRddasModel.number_of_rddas and f_leque(v_pair[1]):
#             return []
#     print(l_palette)
#     return [[1,2],[1,3],[3,4]]
#
# # result of the function, format  [[a1,a2],...]
# l_attractors_fields = []  # S
# # number of relations
# v_number_signals = 0
# for oRDDA in oRedRddasModel.list_of_rddas:
#     for oSignal in oRDDA.list_of_signals:
#         v_number_signals = v_number_signals + 1
# # l_paleta = [rdd1,rdd2,...]
# l_palette = []
# v_tam_caminho = 0
# # List of edges of graph pf compatible pairs
# v_e_1 = [[1,2]]
# for l_line in oRedRddasModel.list_signal_pairs:
#     for v_element in l_line:
#         v_e_1.append(v_element)
# # print(v_e_1)
# # List of edges of graph pf compatible pairs
# v_e_11 = [[1,2],[3,4],[4,5]]
#
# print(f_diference(v_e_1,v_e_11))
#
# for v_pair in f_diference(v_e_1,v_e_11):
#     v_e_11 = []
#     l_aux_field = []
#     v_rdd_aux = f_netMapping(v_pair)[0]
#     if v_rdd_aux not in l_palette:
#         l_palette.append(v_rdd_aux)
#     # fill the attractor field
#     v_e_11.append(f_visita(v_tam_caminho,v_pair,l_palette))
#     print(v_e_11)
#     if len(v_e_11) == oRedRddasModel.number_of_rddas:
#         l_aux_field = f_unique([v_aux_pair[i] for i in range(2) for v_aux_pair in v_e_11])
#         print(l_aux_field)
#         l_attractors_fields.append(l_aux_field)
#         print(len(v_e_11))
#         print(oRedRddasModel.number_of_rddas)
#         print(l_aux_field)
#
# print("List of attractor fields")
# for v_field in l_attractors_fields:
#     print(v_field)
# print(l_attractors_fields)
# # Return the List of Attractors
# oRedRddasModel.attractor_fields = l_attractors_fields