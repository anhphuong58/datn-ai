import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
# Tạo kết nối với Google Drive API
drive_service = build('drive', 'v3', credentials=credentials)

# Định nghĩa ID của thư mục trên Google Drive
folder_id = '1vGb71Z__80B_fWDj1NM2vdGWMmrUWwBm'

# Hàm đệ quy để lưu các tệp tin trong thư mục vào một cấu trúc dữ liệu
def save_folder_content(drive_service, folder_id):
    folder_content = {}

    # Lấy danh sách các tệp tin trong thư mục
    results = drive_service.files().list(q=f"'{folder_id}' in parents and trashed=false").execute()
    files = results.get('files', [])

    # Lưu từng tệp tin trong thư mục vào cấu trúc dữ liệu
    for file in files:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            # Nếu là thư mục, đệ quy để lưu nội dung của thư mục con
            folder_content[file['name']] = save_folder_content(drive_service, file['id'])
        else:
            # Nếu là tệp tin, tải tệp tin và lưu nội dung vào biến
            file_content = io.BytesIO()
            request = drive_service.files().get_media(fileId=file['id'])
            downloader = MediaIoBaseDownload(file_content, request)
            done = False
            while done is False:
                _, done = downloader.next_chunk()
            folder_content[file['name']] = file_content.getvalue()

    return folder_content

# Lưu cấu trúc dữ liệu của thư mục từ Google Drive vào biến
folder_data = save_folder_content(drive_service, folder_id)

# In ra cấu trúc dữ liệu của thư mục
print(folder_data)