import gc
import config.ConfigurationManager as cm

print("Now Booting!")
print("Instantiating ConfigurationManager...")
configManager = cm.ConfigurationManager()

for e in configManager.getConfig():
    print(str(e))

print("Enabling and Setting GC threshold.\n")
gc.enable()
gc.collect()
gc.set_threshold((gc.mem_alloc() + gc.mem_free())/5)

