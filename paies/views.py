from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Paies
import hashlib
import binascii
import json


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
        member = request.user
        # 使用 Unix Timestamp 作為訂單編號（金流也需要加入時間戳記）
        timestamp = int(timezone.now().timestamp())
        order = {
            'MerchantID': MerchantID,
            'RespondType': 'JSON',
            'TimeStamp': timestamp,
            'Version': 2.0,
            'Amt': int(100),
            'MerchantOrderNo': timestamp,
            'ItemDesc': 'Premium會員',
            'ReturnURL': ReturnUrl,
            'NotifyURL': NotifyUrl,
            'CREDIT': 1,
        }

        save_order = Paies(
            member = member,
            order = order['MerchantOrderNo'],
            amount = order['Amt']
        )
        save_order.save()
        # timestamp_int = int(timestamp)
        orders[timestamp] = order
        print(orders)
        
        return redirect('paies:check_order', timestamp)


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
    order = orders.get(TimeStamp)
    if not order:
        return HttpResponse("訂單編號錯誤", status=404)

    # 將要加密的資料串接為字串
    data_chain = gen_data_chain(order)
    
    # 進行 AES 加密
    encrypted_data = aes_encrypt(data_chain)

    # 進行 SHA256 加密
    sha_encrypt = create_sha_encrypt(encrypted_data)
    
    return render(request, 'paies/check.html', {
        'MerchantID': MerchantID,
        'TradeInfo': encrypted_data,
        'TradeSha': sha_encrypt,
        'Version': Version,
    })

@csrf_exempt
def newebpay_return(request):
    if request.method == 'POST':
        # 在這裡處理從藍新回傳的數據
        # 處理完畢後，重定向到結帳成功頁面
        enc_data = request.POST.get('TradeInfo')
        decrypt = decrypt_aes_cbc(enc_data, HASHKEY, HASHIV)

        decrypt_dict = json.loads(decrypt)
        print("decrypt_dict:", decrypt_dict)
        merchant_order = decrypt_dict["Result"]["MerchantOrderNo"]
        print(merchant_order)
        try:
            update_order = Paies.objects.get(order=merchant_order)
            update_order.amount = decrypt_dict["Result"]["Amt"]
            update_order.status = decrypt_dict["Status"]
            update_order.paid_at = decrypt_dict["Result"]["PayTime"]
            # 保存更改
            update_order.save()

            return render(request, 'paies/success.html')
        except Paies.DoesNotExist:
            return HttpResponse("訂单不存在", status=404)
        
    else:
        # 如果是 GET 請求，可以根據需要進行其他處理
        return HttpResponse("Method Not Allowed", status=405)

@csrf_exempt
def newebpay_notify(request):
    if request.method == 'POST':
        # 在這裡處理從藍新回傳的數據
        # 處理完畢後，重定向到結帳成功頁面
        
        return HttpResponse('Notify')
    else:
        # 如果是 GET 請求，可以根據需要進行其他處理
        return HttpResponse("Method Not Allowed", status=405)

def checkout_success(request):
    # 在這個視圖中，你可以顯示結帳成功的信息
    return render(request, 'paies/success.html', {'title': 'Checkout Success'})

def decrypt_aes_cbc(encrypted_data, key, iv):
    try:
        # 將密鑰和IV轉換為字節並確保長度正確
        key_bytes = key.encode('utf-8')[:32]
        print("key_bytes:", key_bytes)
        iv_bytes = iv.encode('utf-8')[:16]
        print("iv_bytes:", iv_bytes)

        encrypted_bytes = bytes.fromhex(encrypted_data)
        print("encrypted_bytes:", encrypted_bytes)

        # 創建 Cipher 物件
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
        print("cipher:", cipher)
        decryptor = cipher.decryptor()
        print("decryptor:", decryptor)
        decrypted_padded_data = decryptor.update(encrypted_bytes) + decryptor.finalize()
        print("decrypted_padded_data:", decrypted_padded_data)

        # 去除填充
        unpadder = padding.PKCS7(128).unpadder()
        print("unpadder:", unpadder)

        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        print("decrypted_data:", decrypted_data)

        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"解密失敗：{e}")
        return None

# # 使用示例
# key_bytes: b'qKiwUe90Wn2I4Ug1cvjl44lJsTGCeLtD'

# iv_bytes: b'CF4Ju2Dj3L4s8TIP'

# encrypted_bytes: b'\x9e\xa6\xa6\xab\xef&\x97d\xba\x89I\n\x05\xaa\x98\x7f\xa8\xe99;q\xd4\x0ey6L.\x19l\x83m;\xf7\x9a\xa4\'\xab\xc3\xa63\xc4\x9c\xdcMt\xb6\xb4/\xba \x81\xb1\xda\xd8\r_\xd8\x0e\xa5\xa2\xd1\xadQKX\xacx\xac\x9b\xf8\x83\xca\xa9\x8cEOQ\xdd:\xde<k\xe8X2\xd8"\x92B\x11Vf\x00\x00\xcf\x12\xa0\x8a\x1d\x8d(t\xa0\xb0\xa4\xe0x\x1b\xeeOS\x8b\x80\x8a\xe3\x89\x98\xd7\xa5\x0cbKZ\x17\xad\x10\xa7\x0b\xfb\xa8\x9a|zr\xfcC\xef\xd2\xd7C\xab\xa3\xef\xeb\xcb\xf3P\x912\xe1\xe4\xb7\x9c\xc1X~JY\xba522.\xb4\x02\xeaU\\@\xa3\xd0\x92k\xf0v\xc8\xec`^\xb5V\xe5\x14\xfc\xf6X\xac\n\xfc\x8d\xec&[\x8c\xe5\x1d\x1c\xea77\x92\x12&\xea*\x91\x8d\xd4/\xae\xb9\xbe\x89\x08M}\xd7\xf3\x10\xe9\x88\x14\x7f\xbbe\x8fALbq\x07\xe3\xe0o|*\xf3\xe6@\xd1\xd1q\xfc\xea\xd6>s\x85\xa6W\x0e\xc4\xfca+\xf3\x15\xdaX\xa1\x8b\xc5\xa3\x08\xe7c\xcb\xc6\x7f\x81W\xfdD\xf4\xc4\xf6\xc7\x88\xd7g>U<+$\xc1Q\x9f\x07\xca7\xd5\xe1\xf4y\xa0}\xbeo4\x1b\x17~\xd8BI\xecg\xc4J\xda\xd7\xb9\x1e.\x9f|\x96r\xcc\xd3\x13!N\xf5?.\x16\x8e\x17B\x13"\xbc\x84\xe1\xa2U\xc2Q\x90\x11E5a\x1f\xc6\x7f\xfb\x03wT\xaf/j\xb1\xa5^n\xd3\x7f\xdf\xf4,7$\x9cH\xb0ao\x83\xff\x83\nv\xbb\xae\xe2\x13\xf5J4\xac\xf4\xe5\xbb\xff\xd6\xa5k,\x08:f\xfe\xfaV\xf6.\xa2\xfc\xb8QW\r\xc5\xf7_K\x9f\xb2\x06\xc7l\xa6\xa9\xbe|\x1f,\xb6z\xda\xef\xbc\xb9\xf7a\xe0\x90Ibb\x11O\xce\xba!\x14!\x7f\xf0\x95\xabM\xa2o\x9b\xd5\n\xac\x03P\x81`\x04\xaa\xecaJD\xa5f\x984H\xbd\x05\x85\x83\xb5s\x02\x05T\xc9\xff\xe5\x0c'

# cipher: <cryptography.hazmat.primitives.ciphers.base.Cipher object at 0x10612d160>

# decryptor: <cryptography.hazmat.primitives.ciphers.base._CipherContext object at 0x10612c290>

# decrypted_padded_data: b'{"Status":"SUCCESS","Message":"\\u6388\\u6b0a\\u6210\\u529f","Result":{"MerchantID":"MS152422619","Amt":100,"TradeNo":"24060120360253122","MerchantOrderNo":"1717245344","RespondType":"JSON","IP":"223.136.181.83","EscrowBank":"HNCB","PaymentType":"CREDIT","RespondCode":"00","Auth":"843241","Card6No":"400022","Card4No":"1111","Exp":"3312","AuthBank":"KGI","TokenUseStatus":0,"InstFirst":0,"InstEach":0,"Inst":0,"ECI":"","PayTime":"2024-06-01 20:36:02","PaymentMethod":"CREDIT"}}\x06\x06\x06\x06\x06\x06'

# unpadder: <cryptography.hazmat.primitives.padding._PKCS7UnpaddingContext object at 0x10612db50>

# decrypted_data: b'{"Status":"SUCCESS","Message":"\\u6388\\u6b0a\\u6210\\u529f","Result":{"MerchantID":"MS152422619","Amt":100,"TradeNo":"24060120360253122","MerchantOrderNo":"1717245344","RespondType":"JSON","IP":"223.136.181.83","EscrowBank":"HNCB","PaymentType":"CREDIT","RespondCode":"00","Auth":"843241","Card6No":"400022","Card4No":"1111","Exp":"3312","AuthBank":"KGI","TokenUseStatus":0,"InstFirst":0,"InstEach":0,"Inst":0,"ECI":"","PayTime":"2024-06-01 20:36:02","PaymentMethod":"CREDIT"}}'

# notify:  9ea6a6abef269764ba89490a05aa987fa8e9393b71d40e79364c2e196c836d3bf79aa427abc3a633c49cdc4d74b6b42fba2081b1dad80d5fd80ea5a2d1ad514b58ac78ac9bf883caa98c454f51dd3ade3c6be85832d82292421156660000cf12a08a1d8d2874a0b0a4e0781bee4f538b808ae38998d7a50c624b5a17ad10a70bfba89a7c7a72fc43efd2d743aba3efebcbf3509132e1e4b79cc1587e4a59ba3532322eb402ea555c40a3d0926bf076c8ec605eb556e514fcf658ac0afc8dec265b8ce51d1cea3737921226ea2a918dd42faeb9be89084d7dd7f310e988147fbb658f414c627107e3e06f7c2af3e640d1d171fcead63e7385a6570ec4fc612bf315da58a18bc5a308e763cbc67f8157fd44f4c4f6c788d7673e553c2b24c1519f07ca37d5e1f479a07dbe6f341b177ed84249ec67c44adad7b91e2e9f7c9672ccd313214ef53f2e168e17421322bc84e1a255c25190114535611fc67ffb037754af2f6ab1a55e6ed37fdff42c37249c48b0616f83ff830a76bbaee213f54a34acf4e5bbffd6a56b2c083a66fefa56f62ea2fcb851570dc5f75f4b9fb206c76ca6a9be7c1f2cb67adaefbcb9f761e090496262114fceba2114217ff095ab4da26f9bd50aac0350816004aaec614a44a566983448bd058583b573020554c9ffe50c

# decrypt:  {"Status":"SUCCESS","Message":"\u6388\u6b0a\u6210\u529f","Result":{"MerchantID":"MS152422619","Amt":100,"TradeNo":"24060120360253122","MerchantOrderNo":"1717245344","RespondType":"JSON","IP":"223.136.181.83","EscrowBank":"HNCB","PaymentType":"CREDIT","RespondCode":"00","Auth":"843241","Card6No":"400022","Card4No":"1111","Exp":"3312","AuthBank":"KGI","TokenUseStatus":0,"InstFirst":0,"InstEach":0,"Inst":0,"ECI":"","PayTime":"2024-06-01 20:36:02","PaymentMethod":"CREDIT"}}
