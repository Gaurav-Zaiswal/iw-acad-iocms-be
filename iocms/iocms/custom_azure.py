from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    azure_container = 'media'
    expiration_secs = None
    overwrite_files = True

class AzureStaticStorage(AzureStorage):
    azure_container = 'static'
    expiration_secs = None
    overwrite_files = True
    