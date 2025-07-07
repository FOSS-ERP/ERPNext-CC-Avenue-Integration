import frappe
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json
import frappe
from frappe import _
from ccavenue_integration.IFRAME_KIT.ccavutil import encrypt , decrypt
from string import Template
from Crypto.Random import get_random_bytes
import json
from frappe.utils import now
from pay_ccavenue import CCAvenue


def get_items():
    doc = frappe.get_doc("CCAvenue Settings")
    if doc.enable:
        access_code = doc.access_code
        WORKING_KEY = doc.working_key
        ACCESS_CODE = doc.access_code
        MERCHANT_CODE = doc.merchant_code
        REDIRECT_URL = doc.redirect_url
        CANCEL_URL = doc.cancel_url

        my_string = WORKING_KEY
        
        key = my_string
        form_data = {}
        encrypted_data = encrypt(form_data, key)
        url = "https://api.ccavenue.com/apis/servlet/DoWebTrans"
        # print(ACCESS_CODE)
        payload = {
            "request_type": "JSON",
            "access_code": ACCESS_CODE,
            "command": "getInvoiceItems",
            "response_type": "JSON",
        }

        import requests
        response = requests.post(url, data=payload, headers={})
        
        response = response.text.split('=')[2]
        print(response)
        data = decrypt(response, key)

        json_data = json.loads(data)

        print(json_data["Invoice_Item_Result"]["item_List"]["item"])

        for row in json_data["Invoice_Item_Result"]["item_List"]["item"]:
            if row['type'] == "ITEM":
                if frappe.db.exists("Item", row['name']):
                    continue
                else:
                    print(row['name'])

        # return dataNBrand logo


# Myntra Account Management
# Nykaa Account Management
# Amazon Lisitng
# Mesho Onboarding
# Copyright
# PMEGP
# CITUS
# ASPIRE
# LMCS for MSMEs
# International Cooperation
# Marketing Assistance Scheme
# RMA against Bank Guarantee
# GST Reg. Amendment
# IEC Registration
# IEC Reg. Amendment
# GST Monthly under 1Cr
# GST Monthly with reconunder1Cr
# GST Monthlywith recon 1 to 5Cr
# GST Monthly with recon 5to10Cr
# GST Monthly for annual
# GST Quarterly under 1Cr
# GST Quarterly for annual
# E invoicing Onboarding
# Amazon.com onboarding
# Pernia Account Management
# Aza Account Management
# Intl 6 platforms for 1 year
# Intl 6 platforms onboarding
# TQUS
# Single Point Reg Scheme
# ISEC
# Government fees
# Bundle Package Intermediate
# Ecommerce Bundle package
# BP Preparation More than 1 Cr
# One to One Expert Advisory
# Digital Sol Standard Plan
# Digital Sol Customised Plan
# Beautypreneur Skin and Hair
# BP Skin And Hair And Advance
# Intermediate Webinar
# DSC
# eCommerce website
# Account Manager
# Brnad logo
# Basic Beauty Skill Training
# Social Social Media Marketing
# Standard Website Development
# C40  Bronze Social Media Optim
# Bronze Social Media optm
# Website eCommerce
# Trade mark certificate
# Additional gov .fees
# Firm audit
# Amazon .com
# Amazon onboard
# Purplle Account Management
# Tata Cliq Account Management
# Tata Platte Account Management
# ECommerce Package Full Program
# ECommerce Package Intermediate
# GST Custom Advisory
# Company Registration Pvt Ltd
# Company Registration LLP
# TAN
# PAN
# Udyam
# FSSAI
# Shop and Establishment
# Trademark
# compliance Turnover Less 1Cr
# compliance Turnover 1 To 5Cr
# compliance Turnover 5 to 10Cr
# Annual Returns and Compliance
# Tata Cliq Onboarding
# Aza Fashions Onboarding
# MirrawLux Onboarding
# Ajio Account Management
# MirrawLux Account Management
# Karma Place Account Management
# Ogaan Account Management
# Jaipore Account Management
# GST Composition scheme 1to 5Cr
# GST Composition scheme 5to10Cr
# GST Composition scheme annual
# ECommerce Package Advance
# ECommerce Package Pro 1to1
# 1 MG Onboarding
# Co Reg Partnership Firm
# E invoicing SAAS
# Myntra onboarding and listing
# BP Preparation 20 Lakhs
# Beautypreneur Skin Services