import Sudoc_SRU as ssru

sru = ssru.Sudoc_SRU()

# --------------- Explain ---------------
res = None
print("\n\n--------------- Explain ---------------")
res = sru.explain()
print("Gouping indexes :")
for grouping_index in res.grouping_indexes:
    print(" - ", grouping_index.as_string)
print("Indexes (only 5) :")
temp = 0
for index in res.indexes:
    print(" - ", index.as_string)
    temp += 1
    if temp >= 5:
        break
print("Record Schemas (only 3) :")
temp = 0
for record_schema in res.record_schemas:
    print(" - ", record_schema.as_string)
    temp += 1
    if temp >= 3:
        break
print("Sort keys (only 3) :")
temp = 0
for sort_key in res.sort_keys:
    print(" - ", sort_key.as_string)
    temp += 1
    if temp >= 3:
        break

# --------------- Scans ---------------
res = None
print("\n\n--------------- Scan 1 ---------------")
res = sru.scan("mti=poisson")
print("Response position :",res.response_position)
print("Maximum terms :",res.maximum_terms)
for term in res.terms:
    print(term.as_string)

res = None
print("\n\n--------------- Scan 2 ---------------")
res = sru.scan(sru.generate_scan_clause(
                    ssru.Part_Of_Query(ssru.SRU_Indexes.MTI,
                    ssru.SRU_Relations.EQUALS, "renard")),
                maximum_terms=4,
                response_position="-1")
print("Response position :",res.response_position)
for term in res.terms:
    print(term.as_string)

# --------------- Search Retrieve ---------------
res = None
print("\n\n--------------- Search Retrieve 1 ---------------")
# res = sru.scan("mti=poisson")
# print("Response position :",res.response_position)
# print("Maximum terms :",res.maximum_terms)
# for term in res.terms:
#     print(term.as_string)




# --------------- Export Search Retrieve to files for each format ---------------
# import xml.etree.ElementTree as ET
# res = None
# for schema in ssru.SRU_Record_Schemas:
#     for packing in ssru.SRU_Record_Packings:
#         res = sru.search_retrieve("aut=Renard alice and apu>2021", record_schema=schema, record_packing=packing)
#         print(f"{schema} as {packing}")
#         with open(f"./samples/Sudoc_SRU/{schema.name}_packed_{packing.name}.xml", mode="wb") as f:
#             f.write(ET.tostring(res.result_as_parsed_xml))