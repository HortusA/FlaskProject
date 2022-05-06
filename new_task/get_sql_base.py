import os
import sqlite3

UPLOAD_BASES = '/home/alex/Документы/new_sql/'


path_to_base = os.path.join(os.path.abspath(UPLOAD_BASES), 'f_lk_payments.sql')
conn = sqlite3.connect(path_to_base)
cursor = conn.cursor()

