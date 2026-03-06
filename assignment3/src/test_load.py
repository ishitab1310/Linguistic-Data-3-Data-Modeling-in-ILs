from parser import load_telugu_treebank, load_hindi_treebank


print("Loading Telugu treebank...")
telugu = load_telugu_treebank("data/telugu/iiit_hcu_intra_chunk_v1.conll")

print("Loading Hindi treebank...")
hindi = load_hindi_treebank("data/hindi")


print("\nTelugu tokens:", len(telugu))
print("Hindi tokens:", len(hindi))


print("\nSample Telugu rows:")
print(telugu.head())

print("\nSample Hindi rows:")
print(hindi.head())