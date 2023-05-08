"""
security.py
state of the art for running safe
#################################

Hashing
=======
SHA-2 and BLACK2 are recommended
SHA-1 and MD5 are insecure

Timming attack risk 
===================
never use == for comparing hash values

Symmetric Enscryption
=====================

"""

import cryptography
import hashlib,hmac,secrets

#TODO:
