# Sử dụng hình ảnh Ubuntu làm cơ sở
FROM ubuntu:latest

# Cập nhật danh sách gói và cài đặt Python3, pip và venv
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Tạo và kích hoạt môi trường ảo
RUN python3 -m venv /opt/venv

# Cài đặt các gói Python trong môi trường ảo
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install fastapi
RUN /opt/venv/bin/pip install sqlalchemy
RUN /opt/venv/bin/pip install mysql-connector-python
RUN /opt/venv/bin/pip install pymysql
RUN /opt/venv/bin/pip install requests
RUN /opt/venv/bin/pip install pydantic
RUN /opt/venv/bin/pip install uvicorn

# Thiết lập PATH để sử dụng môi trường ảo theo mặc định
ENV PATH="/opt/venv/bin:$PATH"

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép các tệp của bạn vào container
COPY ./api .

# Mở port 8000 để truy cập ứng dụng
EXPOSE 8000

# Chạy ứng dụng FastAPI khi container khởi động
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]