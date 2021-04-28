yum install git epel-release -y
yum install https://resources.ovirt.org/pub/yum-repo/ovirt-release43.rpm -y
yum install python-ovirt-engine-sdk4 -y
yum install python-pip -y
yum install wget -y
yum install net-tools -y

pip install numpy==1.12.0
pip install pandas==0.24.2
pip install xlrd==1.0.0
pip install configparser
pip install XlsxWriter

export USER_NAME='admin'
export PASSWORD='Admin123'
export CERT='https://rhvm02.han.private.mobifone.hn/ovirt-engine/services/pki-resource?resource=ca-certificate&format=X509-PEM-CA'

wget -O ca.pem --user $USER_NAME --password $PASSWORD --no-check-certificate $CERT
