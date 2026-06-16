import sys
import requests
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

# Xử lý import UI linh hoạt theo cấu trúc thư mục của bạn
try:
    from ui.transposition import Ui_Dialog
except ModuleNotFoundError:
    try:
        from cau2.ui.transposition import Ui_Dialog
    except ModuleNotFoundError:
        # Dự phòng nếu chạy file trực tiếp cùng thư mục với file UI
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from transposition import Ui_Dialog
    
class MyApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # Kết nối sự kiện Click của nút bấm với hàm xử lý
        self.ui.encrypt_btn.clicked.connect(self.call_api_encrypt)
        self.ui.decrypt_btn.clicked.connect(self.call_api_decrypt)
        
    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/transposition/encrypt"
        
        # Lấy dữ liệu từ giao diện
        plaintext = self.ui.plain_text.toPlainText().strip()
        key_raw = self.ui.key.toPlainText().strip()
        
        # Kiểm tra dữ liệu đầu vào
        if not plaintext or not key_raw:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập đầy đủ Plaintext và Key!")
            return
            
        if not key_raw.isdigit():
            QMessageBox.warning(self, "Lỗi cấu hình", "Key phải là một số nguyên!")
            return

        # Khớp định dạng payload với Flask API nhận ('plaintext' và 'key')
        payload = {
            "plaintext": plaintext,
            "key": int(key_raw)
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                # Hiển thị kết quả mã hóa lên ô cipher_text
                self.ui.cipher_text.setPlainText(result.get("ciphertext", ""))
            else:
                error_msg = response.json().get("error", "Lỗi không xác định từ Server")
                QMessageBox.critical(self, "Lỗi Server", f"Mã lỗi {response.status_code}: {error_msg}")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Lỗi kết nối", "Không thể kết nối tới Flask Server. Bạn đã bật Server chưa?")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/transposition/decrypt"
        
        # Lấy dữ liệu từ giao diện
        ciphertext = self.ui.cipher_text.toPlainText().strip()
        key_raw = self.ui.key.toPlainText().strip()
        
        # Kiểm tra dữ liệu đầu vào
        if not ciphertext or not key_raw:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập đầy đủ Ciphertext và Key!")
            return
            
        if not key_raw.isdigit():
            QMessageBox.warning(self, "Lỗi cấu hình", "Key phải là một số nguyên!")
            return

        # Khớp định dạng payload với Flask API nhận ('ciphertext' và 'key')
        payload = {
            "ciphertext": ciphertext,
            "key": int(key_raw)
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                # Hiển thị kết quả giải mã lên ô plain_text
                self.ui.plain_text.setPlainText(result.get("plaintext", ""))
            else:
                error_msg = response.json().get("error", "Lỗi không xác định từ Server")
                QMessageBox.critical(self, "Lỗi Server", f"Mã lỗi {response.status_code}: {error_msg}")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Lỗi kết nối", "Không thể kết nối tới Flask Server. Bạn đã bật Server chưa?")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())