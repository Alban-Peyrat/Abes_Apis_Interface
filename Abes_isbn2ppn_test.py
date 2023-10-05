import Abes_isbn2ppn as isbn2ppn

i2p = isbn2ppn.Abes_isbn2ppn()

# Check ISBN validity
print("\n\n--------------- Invalid ISBN with check ---------------")
res = i2p.get_matching_ppn("LoveColoredMasterSpark")
print("Input ISBN :", res.input_isbn)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_isbn_used())
print("URL :", res.url)
print("Results :", str(res.get_results()))

# Do not check ISBN validity
print("\n\n--------------- Invalid ISBN without check ---------------")
res = i2p.get_matching_ppn("LoveColoredMasterSpark", check_isbn_validity=False)
print("Input ISBN :", res.input_isbn)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_isbn_used())
print("URL :", res.url)
print("Results :", str(res.get_results()))

# ISBN with 0 PPN match
print("\n\n--------------- ISBN with 0 PPN match ---------------")
res = i2p.get_matching_ppn(2212064004)
print("Input ISBN :", res.input_isbn)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_isbn_used())
print("URL :", res.url)
print("Results :", str(res.get_results()))

# Incorrect ISBN with 0 PPN match
print("\n\n--------------- Incorrect ISBN with 0 PPN match ---------------")
res = i2p.get_matching_ppn("2.907380.77.X", check_isbn_validity=False)
print("Input ISBN :", res.input_isbn)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_isbn_used())
print("URL :", res.url)
print("Results :", str(res.get_results()))

# ISBN with 1 PPN match
# --- MERGES RESULTS ---
print("\n\n--------------- ISBN with 1 PPN match ---------------")
res = i2p.get_matching_ppn("9782862764719")
print("Input ISBN :", res.input_isbn)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_isbn_used())
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# ISBN with multiple PPN match, all matches with holds
# --- MERGES RESULTS ---
print("\n\n--------------- ISBN with multiple PPN match (only with holdings) ---------------")
res = i2p.get_matching_ppn(2110860723)
print("Input ISBN :", res.input_isbn)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_isbn_used())
print("URL :", res.url)
print("Results :", str(res.get_results(merge=True)))

# ISBN with multiple PPN match, some matches do not have holds
print("\n\n--------------- ISBN with multiple PPN match (some without holdings) ---------------")
res = i2p.get_matching_ppn("2-07-037026-7")
print("Input ISBN :", res.input_isbn)
print("Status :", res.status)
print("Error message :", res.error_msg)
print("HTTP Status code :", str(res.HTTP_status_code))
print("Used ISBN :", res.get_isbn_used())
print("URL :", res.url)
print("Results :", str(res.get_results()))