from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from io import BytesIO
import zipfile

# Xác thực OAuth2 với Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

# Tạo đối tượng GoogleDrive
drive = GoogleDrive(gauth)

# Định nghĩa ID của thư mục trên Google Drive
folder_id = '1vGb71Z__80B_fWDj1NM2vdGWMmrUWwBm'

# Tải nội dung của thư mục từ Google Drive
folder = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

# Tạo một danh sách chứa dữ liệu của các tệp trong thư mục
file_data_list = []

# Duyệt qua các tệp trong thư mục
for file in folder:
    # Kiểm tra xem tệp có phải là tệp nén (zip) hay không
    if file['mimeType'] == 'application/zip':
        # Tải tệp nén vào bộ nhớ Python
        zip_file = drive.CreateFile({'id': file['id']})
        zip_file.GetContentFile('temp.zip')
        
        # Giải nén tệp nén
        with zipfile.ZipFile('temp.zip', 'r') as zip_ref:
            # Duyệt qua các tệp trong tệp nén
            for inner_file_name in zip_ref.namelist():
                inner_file_content = zip_ref.read(inner_file_name)
                file_data_list.append(inner_file_content)
        
        # Xóa tệp nén tạm sau khi đã giải nén
        os.remove('temp.zip')
    else:
        # Tải tệp từ Google Drive trực tiếp vào bộ nhớ Python
        file_content = drive.CreateFile({'id': file['id']}).GetContentString()
        file_data_list.append(file_content)

# Xử lý dữ liệu của các tệp trong danh sách file_data_list theo nhu cầu của bạn
# ...

# Ví dụ: In ra nội dung của các tệp
for file_data in file_data_list:
    print(file_data)
