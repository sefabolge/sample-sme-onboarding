import os
from datetime import datetime

def user_document_path(instance, filename):
    username = instance.application.user.username
    doc_type = instance.doc_type
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{doc_type}_{timestamp}.{ext}"
    return os.path.join("documents", username, filename)
