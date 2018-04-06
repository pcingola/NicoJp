#!/usr/bin/env python

import unittest as ut
import canal as ca


class TestCanal(ut.TestCase):

    def test_aba_1(self):
        b = ca.BankAccount('bankbankbank Routing number: 098765451 bankbankbank')
        self.assertEqual(b.aba, '098765451')

    def test_aba_2(self):
        b = ca.BankAccount('bankbankbank ABA 098765451 bankbankbank')
        self.assertEqual(b.aba, '098765451')

    def test_account_1(self):
        b = ca.BankAccount('bankbankbank ACC NO: 382826277272 bankbankbank')
        self.assertEqual(b.account, '382826277272')

    def test_account_2(self):
        b = ca.BankAccount('bankbankbank ACCOUNT #382826277272 bankbankbank')
        self.assertEqual(b.account, '382826277272')

    def test_account_3(self):
        b = ca.BankAccount('bankbankbank ACCOUNT NO: 382826277272 bankbankbank')
        self.assertEqual(b.account, '382826277272')

    def test_account_4(self):
        b = ca.BankAccount('bankbankbank A/C NR. 382826277272 bankbankbank')
        self.assertEqual(b.account, '382826277272')

    def test_account_5(self):
        b = ca.BankAccount('bankbankbank CC 382826277272 bankbankbank')
        self.assertEqual(b.account, '382826277272')

    def test_account_6(self):
        b = ca.BankAccount("JPMRUS31  178992312   017323232")
        self.assertEqual(b.account, '178992312017323232')

    def test_account_7(self):
        b = ca.BankAccount("JPMRUS31  178992312-017323232")
        self.assertEqual(b.account, '178992312017323232')

    def test_account_8(self):
        b = ca.BankAccount("178992312.017323232")
        self.assertEqual(b.account, '178992312017323232')

    def test_bank_1(self):
        b = ca.BankAccount("CRESPI'S BANK SWIFT: CRESPI33S  ACCT: 30321253")
        self.assertEqual(b.swift, 'CRESPI33S')
        self.assertEqual(b.account, '30321253')

    def test_bank_2(self):
        b = ca.BankAccount("ACCOUNT NUMBER: 9003004000 IBAN: DE800912341230123012 SWIFT: SHQDE33")
        self.assertEqual(b.swift, 'SHQDE33')
        self.assertEqual(b.account, '9003004000')
        self.assertEqual(b.iban, 'DE800912341230123012')

    def test_bank_3(self):
        b = ca.BankAccount("BBVA FRANCES CHICAGO BRANCH SWIFT: BBVAUS33 ACCT: 33221123")
        self.assertEqual(b.swift, 'BBVAUS33')
        self.assertEqual(b.account, '33221123')

    def test_bank_4(self):
        sc = ca.SwiftCodes()
        b = ca.BankAccount("INTERM BANK: STANICIO'S BANK NEW YORK BRANCH JPMRUS31", sc)
        self.assertEqual(b.swift, 'JPMRUS31')

    def test_bank_5(self):
        sc = ca.SwiftCodes()
        b = ca.BankAccount("JPMRUS31  178992312   017323232", sc)
        self.assertEqual(b.swift, 'JPMRUS31')
        self.assertEqual(b.account, '178992312017323232')

    def test_bank_6(self):
        sc = ca.SwiftCodes()
        b = ca.BankAccount("BENEFICIARY BANK BBVA FRANCES ARGENTINA BFRPARBA CBU: 1230012301230123", sc)
        self.assertEqual(b.swift, 'BFRPARBA')
        self.assertEqual(b.cbu, '1230012301230123')

    def test_iban_1(self):
        b = ca.BankAccount('bankbankbank IBAN: AT3920029282727 bankbankbank')
        self.assertEqual(b.iban, 'AT3920029282727')

    def test_iban_2(self):
        b = ca.BankAccount('bankbankbank IBAN-NR. AT3920029282727 bankbankbank')
        self.assertEqual(b.iban, 'AT3920029282727')

    def test_iban_3(self):
        b = ca.BankAccount('bankbankbank IBAN NO. AT3920029282727 bankbankbank')
        self.assertEqual(b.iban, 'AT3920029282727')

    def test_iban_4(self):
        b = ca.BankAccount('bankbankbank IBAN-CODE:AT3920029282727 bankbankbank')
        self.assertEqual(b.iban, 'AT3920029282727')

    def test_iban_5(self):
        b = ca.BankAccount('bankbankbank IBAN-NR. : AT3920029282727 bankbankbank')
        self.assertEqual(b.iban, 'AT3920029282727')

    def test_iban_6(self):
        b = ca.BankAccount('bankbankbank IBAN NO.: AT3920029282727 bankbankbank')
        self.assertEqual(b.iban, 'AT3920029282727')

    def test_swift_1(self):
        b = ca.BankAccount('bankbankbank Swift:CRESPI33S bankbankbank')
        self.assertEqual(b.swift, 'CRESPI33S')

    def test_swift_2(self):
        b = ca.BankAccount('bankbankbank Swift number:CRESPI33S bankbankbank')
        self.assertEqual(b.swift, 'CRESPI33S')

    def test_swift_3(self):
        b = ca.BankAccount('bankbankbank Swift num: CRESPI33S bankbankbank')
        self.assertEqual(b.swift, 'CRESPI33S')

    def test_swift_4(self):
        b = ca.BankAccount('bankbankbank Swift Code: CRESPI33S bankbankbank')
        self.assertEqual(b.swift, 'CRESPI33S')

    def test_swift_5(self):
        b = ca.BankAccount('bankbankbank Swift Code CRESPI33S bankbankbank')
        self.assertEqual(b.swift, 'CRESPI33S')

    def test_swift_6(self):
        b = ca.BankAccount('bankbankbank Bic Code CRESPI33S bankbankbank')
        self.assertEqual(b.swift, 'CRESPI33S')

    def test_swift_7(self):
        b = ca.BankAccount('bankbankbank Bic CRESPI33S bankbankbank')
        self.assertEqual(b.swift, 'CRESPI33S')

    def test_swift_8(self):
        b = ca.BankAccount('bankbankbank Swift Code nr. CRESPI33S bankbankbank')
        self.assertEqual(b.swift, 'CRESPI33S')

    def test_swift_9(self):
        b = ca.BankAccount('bankbankbank Code number:CRESPI33S bankbankbank')
        self.assertEqual(b.swift, 'CRESPI33S')

    def test_swift_10(self):
        b = ca.BankAccount('bankbankbank Bic-code:CRESPI33S bankbankbank')
        self.assertEqual(b.swift, 'CRESPI33S')

if __name__ == '__main__':
    ut.main()
