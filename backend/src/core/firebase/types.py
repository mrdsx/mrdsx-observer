from google.cloud import firestore
from google.cloud.firestore_v1 import async_collection, async_document

AsyncFirestore = firestore.AsyncClient
AsyncDocumentReference = async_document.AsyncDocumentReference
AsyncCollectionReference = async_collection.AsyncCollectionReference
