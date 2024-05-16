from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import hashlib
import binascii


MerchantID = settings.ENCRYPTION_KEY['MERCHANT_ID']
HASHKEY = settings.ENCRYPTION_KEY['HASH_KEY']
HASHIV = settings.ENCRYPTION_KEY['HASH_IV']
Version = settings.ENCRYPTION_KEY['VERSION']
ReturnUrl = settings.ENCRYPTION_KEY['RETURN_URL']
NotifyUrl = settings.ENCRYPTION_KEY['NOTIFY_URL']
PayGateWay = settings.ENCRYPTION_KEY['PAY_GATEWAY']
RespondType = settings.ENCRYPTION_KEY['RESPOND_TYPE']

orders = {}
def index(request):
    return render(request, 'paies/index.html', {'title': 'Express'})

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        data = request.POST

        # 使用 Unix Timestamp 作為訂單編號（金流也需要加入時間戳記）
        timestamp = timezone.now().timestamp()
        order = {
            **data,
            'MerchantID': MerchantID,
            'RespondType': 'JSON',
            'TimeStamp': timestamp,
            'Version': 2.0,
            'Amt': int(100),
            'MerchantOrderNo': timestamp,
            'ItemDesc': 'yoyoy',
            'ReturnURL': ReturnUrl,
            'NotifyURL': NotifyUrl,
            'CREDIT': 1,
        }
        print('訂單資料：', data, '\n')

        timestamp_int = int(timestamp)
        orders[timestamp_int] = order
        print(orders)
        
        return redirect('paies:check_order', timestamp_int)


    return HttpResponse('Method Not Allowed', status=405)

def gen_data_chain(order):
    return f"MerchantID={order['MerchantID']}&TimeStamp={order['TimeStamp']}&Version={order['Version']}&RespondType={order['RespondType']}&MerchantOrderNo={order['MerchantOrderNo']}&Amt={order['Amt']}&NotifyURL={order['NotifyURL']}&ReturnURL={order['ReturnURL']}&ItemDesc={order['ItemDesc']}"

def aes_encrypt(data):
    # 將密鑰和初始向量轉換為 bytes
    key_bytes = HASHKEY.encode('utf-8')[:32]
    iv_bytes = HASHIV.encode('utf-8')[:16]
    # print(key_bytes)
    # print(iv_bytes)

    # 創建 Cipher 物件，使用 AES 算法和 CBC 模式
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())

    # 創建 encryptor 對象
    encryptor = cipher.encryptor()

    # 計算填充所需的字節數
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode('utf-8')) + padder.finalize()
    # 加密資料
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # 返回加密後的資料的十六進制表示形式
    return ciphertext.hex()

def create_sha_encrypt(edata1):
    hash_string = f"HashKey={HASHKEY}&{edata1}&HashIV={HASHIV}"
    sha256_hash = hashlib.sha256(hash_string.encode()).hexdigest()

    return sha256_hash.upper()

# views.py
@csrf_exempt
def check_order(request, TimeStamp):
    
    order = {
        'MerchantID': MerchantID,
        'RespondType': 'JSON',
        'TimeStamp': TimeStamp,
        'Version': 2.0,
        'Amt': int(100),
        'MerchantOrderNo': TimeStamp,
        'ItemDesc': 'yoyoy',
        'ReturnURL': ReturnUrl,
        'NotifyURL': NotifyUrl,
        'CREDIT': 1
    }

    # 將要加密的資料串接為字串
    data_chain = gen_data_chain(order)
    
    encrypted_data = aes_encrypt(data_chain)

    # 進行 SHA256 加密
    sha_encrypt = create_sha_encrypt(encrypted_data)
    
    # 渲染訂單檢查頁面並傳遞相關數據
    return render(request, 'paies/check.html', {
        'MerchantID': MerchantID,
        'TradeInfo': encrypted_data,
        'TradeSha': sha_encrypt,
        'Version': Version,
    })

@csrf_exempt
def newebpay_return(request):
    # print(request)
    if request.method == 'POST':
        # 在這裡處理從藍新回傳的數據
        # 處理完畢後，重定向到結帳成功頁面
        
        return render(request, 'paies/success.html')
    else:
        # 如果是 GET 請求，可以根據需要進行其他處理
        return HttpResponse("Method Not Allowed", status=405)

@csrf_exempt
def newebpay_notify(request):
    if request.method == 'POST':
        # 在這裡處理從藍新回傳的數據
        # 處理完畢後，重定向到結帳成功頁面
        enc_data = request.POST.get('TradeInfo')
        print('notify: ', enc_data)
        return HttpResponse('Notify')
    else:
        # 如果是 GET 請求，可以根據需要進行其他處理
        return HttpResponse("Method Not Allowed", status=405)

def checkout_success(request):
    # 在這個視圖中，你可以顯示結帳成功的信息
    return render(request, 'paies/success.html', {'title': 'Checkout Success'})
# def decrypt_aes_cbc(data, key, iv):
#     try:
#         backend = default_backend()
#         cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
#         decryptor = cipher.decryptor()
#         decrypted_data = decryptor.update(data) + decryptor.finalize()
#         return remove_padding(decrypted_data)
#     except Exception as e:
#         print(f"解密失敗：{e}")
#         return None

# def remove_padding(data):
#     padding_length = data[-1]
#     return data[:-padding_length]

# # 使用示例
# key = b'qKiwUe90Wn2I4Ug1cvjl44lJsTGCeLtD'  # 替換為您的密鑰
# iv = b'CF4Ju2Dj3L4s8TIP'  # 替換為您的初始向量
# encrypted_data_hex = '976ba310320fa70903ab04f15192d6fbe50903765974d895cbb35bebbf010496931f402e0fa09a9f56401926e3ebb35c713bd202aa3efe6b34224ab41823708af1063be2ea5daf80fcd2264294f67701ee59043ae41dcad93703c92cdfccb7ba4a5925c85a63919d4f82c53f9604c9074f2c860db27b05768a1692a4349d0436bbfe4f4283edbc41b326b021ebea2b3f4c880347de32697b4aebf6302081ea253dbac156d3a2506b4f3766230740955f2bb4516455375bf449ade1fa049c702d2b5430ab745c2e7c572ba1728d88eff3b27ebbca8fdf4c7f2ffdf0bd7102425856d9669269f17f842c603a3249b244b7'  # 替換為加密後的十六進制字符串
# encrypted_data = binascii.unhexlify(encrypted_data_hex)
# decrypted_data = decrypt_aes_cbc(encrypted_data, key, iv)
# if decrypted_data:
#     print(f"解密後資料：{decrypted_data.decode('utf-8')}")
# else:
#     print("解密失敗")
