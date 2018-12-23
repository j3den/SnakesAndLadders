import gc
import os

print("Now Booting!")
print("Enabling and Setting GC threshold.\n")
gc.enable()
gc.collect()
gc.set_threshold((gc.mem_alloc() + gc.mem_free())/5)
