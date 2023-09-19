import xml.etree.ElementTree as ET
import Sudoc_SRU as ssru

sru = ssru.Sudoc_SRU()

# --------------- Explain ---------------
res = None
print("\n\n--------------- Explain ---------------")
res = sru.explain()
print("URL :", res.url)
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
print("URL :", res.url)
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
print("URL :", res.url)
print("Response position :",res.response_position)
for term in res.terms:
    print(term.as_string)

# --------------- Search Retrieve ---------------
res = None
print("\n\n--------------- Search Retrieve 1 ---------------")
res = sru.search("mti=renard")
print("URL :", res.url)
print("Query :", res.query)
print("Record Schema :", res.record_schema)
print("Record Packing :", res.record_packing)
print("Maximum Records :", res.maximum_record)
print("Start Record :", res.start_record)
print("Records id : ", str(res.records_id))

res = None
print("\n\n--------------- Search Retrieve 2 ---------------")
res = sru.search(sru.generate_query([
        "(",
        ssru.Part_Of_Query(ssru.SRU_Indexes.MTI, ssru.SRU_Relations.EQUALS, "renard"),
        ssru.Part_Of_Query(ssru.SRU_Indexes.MTI, ssru.SRU_Relations.EQUALS, "poisson", bool_operator=ssru.SRU_Boolean_Operators.OR),
        ")",
        " and APU > 2020"]),
        record_schema=ssru.SRU_Record_Schemas.PICA_XML,
        record_packing=ssru.SRU_Record_Packings.STRING,
        maximum_records="23",
        start_record=None)
print("URL :", res.url)
print("Query :", res.query)
print("Record Schema :", res.record_schema)
print("Record Packing :", res.record_packing)
print("Maximum Records :", res.maximum_record)
print("Start Record :", res.start_record)
print("Records id : ", str(res.records_id))

res = None
print("\n\n--------------- Search Retrieve 3 ---------------")
res = sru.search(sru.generate_query([
        ssru.Part_Of_Query(ssru.SRU_Indexes.AUT, ssru.SRU_Relations.EQUALS, "renard alice"),
        ssru.Part_Of_Query(ssru.SRU_Indexes.NOTE_DE_THESE, ssru.SRU_Relations.EQUALS, "bordeaux 20*")]),
        record_schema="isni-b",
        record_packing="xml")
print("URL :", res.url)
print("Query :", res.query)
print("Record Schema :", res.record_schema)
print("Record Packing :", res.record_packing)
print("Record : ", ET.tostring(res.records[0]))


# --------------- Export Search Retrieve to files for each format ---------------
# res = None
# for schema in ssru.SRU_Record_Schemas:
#     for packing in ssru.SRU_Record_Packings:
#         res = sru.search("aut=Renard alice and apu>2021", record_schema=schema, record_packing=packing)
#         print(f"{schema} as {packing}")
#         with open(f"./samples/Sudoc_SRU/{schema.name}_packed_{packing.name}.xml", mode="wb") as f:
#             f.write(ET.tostring(res.result_as_parsed_xml))