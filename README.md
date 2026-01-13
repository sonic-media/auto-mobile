# Mobile Cookie Import Tool

Công cụ GUI để quản lý cookie files và thao tác với file CSV cho mobile automation.

## Files trong project:

### `gui.py` - Giao diện chính

GUI PySide6 với các tính năng:

- **Load Cookie Button**: Upload file .txt vào thư mục `/cookies`
- **Refresh Table Button**: Cập nhật bảng hiển thị dữ liệu CSV
- **CSV Table**: Hiển thị thông tin chi tiết với 4 cột:
  - **Model**: Model thiết bị tương ứng
  - **Serial**: ID thiết bị từ ADB
  - **Username**: Username được detect từ tên file cookie
  - **Cookie File**: Tên file cookie trong thư mục `/cookies`

### `helpers/csv.py` - Module tiện ích CSV

Class `CSVHelper` với các phương thức:

#### Đọc dữ liệu:

- `read_csv(file_path, delimiter=',')` - Đọc toàn bộ file CSV
- `read_row(file_path, row_index, delimiter=',')` - Đọc một hàng cụ thể
- `read_column(file_path, col_index, delimiter=',')` - Đọc một cột cụ thể
- `get_cell(file_path, row_index, col_index, delimiter=',')` - Đọc một ô cụ thể

#### Ghi dữ liệu:

- `write_csv(file_path, data, delimiter=',')` - Ghi toàn bộ dữ liệu vào CSV
- `write_row(file_path, row_index, row_data, delimiter=',')` - Ghi một hàng
- `write_column(file_path, col_index, col_data, delimiter=',')` - Ghi một cột
- `append_row(file_path, row_data, delimiter=',')` - Thêm hàng mới
- `update_cell(file_path, row_index, col_index, value, delimiter=',')` - Cập nhật một ô

#### Thông tin file:

- `get_csv_shape(file_path, delimiter=',')` - Lấy kích thước (số hàng, số cột)

### `index.py` - Logic automation

Script ADB để tự động import cookie vào Firefox trên mobile device.

### `data.csv` - File dữ liệu

Chứa thông tin device serial và đường dẫn cookie files.

## Cách sử dụng:

1. **Chạy GUI**: `python gui.py`
2. **Upload cookie**: Click "Load Cookie" để chọn file .txt
3. **Xem dữ liệu**: Click "Refresh Table" để cập nhật bảng với:
   - Model và Serial của thiết bị kết nối
   - Username được detect từ tên file
   - Danh sách file cookie

## Ví dụ sử dụng CSVHelper:

```python
from helpers.csv import CSVHelper

# Đọc toàn bộ file
data = CSVHelper.read_csv('data.csv')

# Đọc hàng đầu tiên
row = CSVHelper.read_row('data.csv', 0)

# Đọc cột đầu tiên
column = CSVHelper.read_column('data.csv', 0)

# Ghi dữ liệu mới
CSVHelper.write_csv('data.csv', [['Device', 'Cookie'], ['ABC123', 'path/to/cookie.txt']])

# Cập nhật ô cụ thể
CSVHelper.update_cell('data.csv', 1, 1, 'new_cookie.txt')
```

## Yêu cầu:

- Python 3.x
- PySide6: `pip install PySide6`
- ADB (cho mobile automation)
