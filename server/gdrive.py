from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from pathlib import Path

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.file']

def getService():
    """
    Get the google drive service (v2)

    Returns
    ----------
     - service: Resource
        A Resource object allowing access to the Google Drive API
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, refresh them.
    if not creds or not creds.valid:
        creds.refresh(Request())
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v2', credentials=creds)
    return service


def uploadFile(filepath, parent="root"):
    """ 
    Upload a file to google drive, will not upload if it already exists

    Inputs
    -----------
     - filepath - pathlib.Path
        The path to the file on the local system

     - parent - String (optional)
        The drive ID of the parent we want to upload to
    """
    service = getService()

    parent = getOrCreatePath(filepath.parents[0], parent)

    # Check if file exists
    query = "title='{}'".format(filepath.name)
    children = service.children().list(
                      folderId=parent, 
                      q=query).execute()
    results = children.get('items', [])

    # If file doesn't already exist, create it
    if len(results) == 0:
        f = MediaFileUpload(str(filepath), resumable=True)
        if not f.mimetype():
            f = MediaFileUpload(str(filepath), 'application/octet-stream', resumable=True)

        body = {
                'title': filepath.name,
                'parents': [{'id': parent}]
                }

        request = service.files().insert(
                body=body,
                media_body=f).execute()


def getOrCreatePath(path, parent="root"):
    """
    Returns the ID of a path starting at parent, creating that path if it does not exist

    Inputs
    -----------
     - path - pathlib.Path
        The path we want to get

     - parent - String (optional)
        The drive ID of the parent 

    Returns
    -----------
     - folder_id - String
        The drive ID of the path's final folder
    """
    service = getService()

    parent_id = parent
    for folder in path.parts:
        # Get folder if it exists on GoogleDrive
        query = "mimeType='application/vnd.google-apps.folder' and title='{}'".format(folder)
        children = service.children().list(
                          folderId=parent_id, 
                          q=query).execute()
        results = children.get('items', [])

        # If folder exists
        if len(results) > 0:
            parent_id = results[0]['id']

        # If folder does not exist we must create it
        else:
            parent_id = createFolder(folder, parent_id)

    return parent_id

    
def createFolder(name, parent="root"):
    """
    Create a folder in google drive

    Inputs
    -----------
     - name - String
        The name of the new folder

     - parent - String (optional)
        The drive ID of the parent we want to insert a folder in

    Returns
    -----------
     - folder_id - String
        The drive ID of the created folder
    """
    service = getService()

    body = {
            'title': name,
            'mimeType': 'application/vnd.google-apps.folder'
            }

    if parent:
        body['parents'] = [{'id': parent}]
    
    request = service.files().insert(
            body=body, fields='id').execute()

    folder_id = request.get('id')
    return folder_id


if __name__ == '__main__':
    uploadFile(Path("uploads/test2.txt"), "1OU2lDhrsLSr-l2MR0-3rbYV4bzwyOtQA")
