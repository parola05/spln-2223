#!/usr/bin/env python3
import hshield.document_shield
from hshield.document_shield import DocumentShield
import os

path = os.path.dirname(__file__) + "/documentos_test.txt"
text = open(path, "r").read()
test = DocumentShield(text)

test.shield()
