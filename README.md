# mobifone_rhvm
## Xuất thông tin danh sách máy ảo cùng thông tin LUN_VOLUME trong RHVM
### Kỹ sư thực hiện: Lâm Nguyễn (lam.nd@svtech.com.vn)

#### 1. Đặt vấn đề
-   Công cụ Cloud Form có thể export được thông tin cơ bản về máy ảo, địa chỉ ip của các máy ảo trong một cluster.  [Khảo sát](https://github.com/LamNguy/svtech_intership/blob/master/support/RHVM_export.pdf)
-   Cloud Form không xuất được thông tin các disk mà các máy ảo đang dùng cùng các LUN volume được cấp cho các máy ảo

### 2. Giải pháp
-   Dùng script (Python) để lấy thông tin máy ảo cùng các disk id, lun_id trên các host và xuất thông tin ra.
-   Input: chạy script và chọn cluster
-   Output: excel file chứa thông tin các máy ảo trên cluster đó (được chia thành các host)

### 3. Yêu cầu cài đặt
-   Môi trường Linux, đã test trên Centos7
-   Khuyến nghị chạy trên một máy ảo độc lập do script sẽ tương tác với RHVM, script yêu cầu các thư viện cài đặt thêm nên làm thế để tránh sự cố không mong muốn.
-   Mở firewall HTTPS từ máy ảo chạy script đến các node RHVM
-   Một tool để chuyển export excel sang một máy desktop để hiện thị (scp, winscp)

### 4. Cài script
```
git clone https://github.com/LamNguy/mobifone_rhvm
```

### 5. Cài đặt thư viện trên máy ảo
__Manual install__
```
yum install git epel-release -y
yum install https://resources.ovirt.org/pub/yum-repo/ovirt-release43.rpm -y
yum install python-ovirt-engine-sdk4 -y
yum install python-pip -y
yum install wget -y
pip install numpy==1.12.0
pip install pandas==0.24.2
pip install xlrd==1.0.0
pip install XlsxWriter
```
__Script install__ (kiểm tra lại file script)
```
bash /mobifone/rhvm/env_install.sh
```

### 6. Tải certificate
__Cách 1__: Có thể tải trực tiếp certificate trên giao diện portal RHVM
```
https://rhvm02.han.private.mobifone.hn/ovirt-engine/services/pki-resource?resource=ca-certificate&format=X509-PEM-CA'
```
__Cách 2__: Tải bằng wget, chạy script (thay đổi username/password)
```
export USER_NAME='admin'
export PASSWORD='Admin123444'
export CERT='https://rhvm02.han.private.mobifone.hn/ovirt-engine/services/pki-resource?resource=ca-certificate&format=X509-PEM-CA'
wget -O ca.pem --user $USER_NAME --password $PASSWORD --no-check-certificate $CERT
```

### 7. Cấu hình
Cấu hình file __adminrc__ cấu hình trong thư mục mobifone_rhvm.
Trong đó:
-   URL: trỏ tới api của rhvm, thay đổi domain tương ứng
-   USERNAME: username@profile, default profile: internal
-   PASSWORD
-   CERT_PATH: đường dẫn tới certificate
```
export URL='https://rhvm02.han.private.mobifone.vn/ovirt-engine/api'
export USER_NAME='admin@internal'
export PASSWORD='admin12311'
export CERT_PATH='/root/mobifone_rhvm/ca.pem'
```
__Active cấu hình__
```
. adminrc
```
### 8. Triển khai
```
cd ~/mobifone_rhvm/
python export.py
```
---
[root@dns mobifone_rhvm]# python export.py 
Connect to rhvm: True
List cluster in rhvm
__0:YH_blade_pool01__
__1:YH_type01_pool01__
__2:YH_type02_pool01__
Enter cluster name?
---
Connect true --> kết nối thành công
Script sẽ list ra danh sách các cluster trong RHVM, nhập cluster name (copy paste)

---
[root@dns mobifone_rhvm]# python export.py 
Connect to rhvm: True
List cluster in rhvm
0:YH_blade_pool01
1:YH_type01_pool01
2:YH_type02_pool01
Enter cluster name? __YH_blade_pool01__
---

#### Thông báo export successfully --> export thành công
---
root@dns mobifone_rhvm]# python export.py 
Connect to rhvm: True
List cluster in rhvm
0:YH_blade_pool01
1:YH_type01_pool01
2:YH_type02_pool01
Enter cluster name?YH_blade_pool01
__Exported successfully__
[root@dns mobifone_rhvm]# 
---
#### File export trong thư mục mobifone_rhvm, format tên là "clustername.xlsx"
---
[root@dns mobifone_rhvm]# ls  __YH_blade_pool01.xlsx__ 
__YH_blade_pool01.xlsx__
---
