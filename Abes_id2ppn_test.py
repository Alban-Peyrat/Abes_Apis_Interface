import Abes_id2ppn as id2ppn

i2p = id2ppn.Abes_id2ppn()

# Check ISBN validity
print("\n\n--------------- Invalid ISBN with check ---------------")
res = i2p.get_matching_ppn("LoveColoredMasterSpark")
print("Input ISBN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_id_used())
print("URL :", res.url)
print("Results :", str(res.get_results()))

# Do not check ISBN validity
print("\n\n--------------- Invalid ISBN without check ---------------")
res = i2p.get_matching_ppn("LoveColoredMasterSpark", check_isbn_validity=False)
print("Input ISBN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_id_used())
print("URL :", res.url)
print("Results :", str(res.get_results()))

# ISBN with 0 PPN match
print("\n\n--------------- ISBN with 0 PPN match ---------------")
res = i2p.get_matching_ppn(2212064004)
print("Input ISBN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_id_used())
print("URL :", res.url)
print("Results :", str(res.get_results()))

# Incorrect ISBN with 0 PPN match
print("\n\n--------------- Incorrect ISBN with 0 PPN match ---------------")
res = i2p.get_matching_ppn("2.907380.77.X", check_isbn_validity=False)
print("Input ISBN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_id_used())
print("URL :", res.url)
print("Results :", str(res.get_results()))

# ISBN with 1 PPN match
# --- MERGES RESULTS ---
print("\n\n--------------- ISBN with 1 PPN match ---------------")
res = i2p.get_matching_ppn("9782862764719")
print("Input ISBN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_id_used())
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# ISBN with multiple PPN match, all matches with holds
# --- MERGES RESULTS ---
print("\n\n--------------- ISBN with multiple PPN match (only with holdings) ---------------")
res = i2p.get_matching_ppn(2110860723)
print("Input ISBN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_id_used())
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# ISBN with multiple PPN match, some matches do not have holds
print("\n\n--------------- ISBN with multiple PPN match (some without holdings) ---------------")
res = i2p.get_matching_ppn("2-07-037026-7")
print("Input ISBN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_id_used())
print("URL :", res.url)
print("Results :", str(res.get_results()))

# ---------- Other IDs ----------

i2p = id2ppn.Abes_id2ppn(webservice=id2ppn.Webservice.ISSN, useJson=False)
# ISSN with hyphen
print("\n\n--------------- ISSN with hyphen ---------------")
res = i2p.get_matching_ppn("0012-5377")
print("Input ISSN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# ISSN without hyphen
print("\n\n--------------- ISSN without hyphen ---------------")
res = i2p.get_matching_ppn("07685785")
print("Input ISSN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# EAN
i2p = id2ppn.Abes_id2ppn(webservice=id2ppn.Webservice.EAN)
print("\n\n--------------- EAN ---------------")
res = i2p.get_matching_ppn("5060314994827")
print("Input EAN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# FRBN
i2p = id2ppn.Abes_id2ppn(webservice=id2ppn.Webservice.FRBN)
print("\n\n--------------- French Natonal Library ID (frBN) ---------------")
res = i2p.get_matching_ppn("472983100000004")
print("Input FRBN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# OCN
i2p = id2ppn.Abes_id2ppn(webservice=id2ppn.Webservice.OCN)
print("\n\n--------------- Worldcat ID (OCN) ---------------")
res = i2p.get_matching_ppn("882104914")
print("Input OCN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# DNB
i2p = id2ppn.Abes_id2ppn(webservice=id2ppn.Webservice.DNB)
print("\n\n--------------- German national Library ID (DNB) ---------------")
res = i2p.get_matching_ppn("1009232339")
print("Input DNB :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# UCATB
i2p = id2ppn.Abes_id2ppn(webservice=id2ppn.Webservice.UCATB)
print("\n\n--------------- UCATB ID ---------------")
res = i2p.get_matching_ppn("40394329")
print("Input UCATB :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# Cairn
i2p = id2ppn.Abes_id2ppn(webservice=id2ppn.Webservice.FRCAIRN)
print("\n\n--------------- Cairn ID ---------------")
res = i2p.get_matching_ppn("PUG_CHABO_2003_01")
print("Input FRCAIRNINFO :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# SprignerLN
i2p = id2ppn.Abes_id2ppn(webservice=id2ppn.Webservice.SPRINGERLN)
print("\n\n--------------- National Licence Sprigner ID ---------------")
res = i2p.get_matching_ppn("978-3-540-41727-9")
print("Input SpringerLN :", res.id)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))