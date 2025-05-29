import pandas as pd

df = pd.read_csv('sales_data.csv')

print(df)

df['Ημερομηνία'] = pd.to_datetime(df['Ημερομηνία'])

df['Πωλητής'] = df['Πωλητής'].str.strip().str.lower().str.title()
df['Email'] = df['Email'].str.lower().str.replace('yahoo.gr','yahoo.com')
df['ΑΦΜ'] = df['ΑΦΜ'].astype(str)

df['ΑΦΜ'] = df['ΑΦΜ'].replace('NA', None)

criteria = (df['ΑΦΜ'].str.len() != 9) | (df['ΑΦΜ'].str == '000000000')
df['ΑΦΜ'] = ~criteria

df['Ηλικία'] = df['Ηλικία'].fillna(df['Ηλικία'].mean())

df['Τιμή'] = df['Τιμή'].fillna(method='ffill')
df['Έξοδα'] = df['Έξοδα'].fillna(method='ffill')

df['Σύνολο'] = df['Τιμή'] * df['Ποσότητα']
df['Καθαρό_Κέρδος'] = df['Σύνολο'] - df['Έξοδα']

#Πόσες πωλήσεις έγιναν ανά κατάστημα;
print(df.groupby('Κατάστημα')['Ποσότητα'].sum())

#Ποιο προϊόν έφερε τα περισσότερα καθαρά κέρδη συνολικά;
print(df.groupby('Προϊόν')['Καθαρό_Κέρδος'].sum().idxmax())

#Ποιος πωλητής είχε τη μεγαλύτερη μέση τιμή πώλησης;

print(df.groupby('Πωλητής')['Τιμή'].mean().idxmax())

#Ποιο κατάστημα έχει τον υψηλότερο μέσο όρο καθαρών κερδών;
print(df.groupby('Κατάστημα')['Καθαρό_Κέρδος'].mean().idxmax())

#Αντιμετώπισε τα duplicates, αν υπάρχουν
df = df.drop_duplicates()

# Υπολόγισε τον μέσο όρο πωλήσεων ανά ηλικιακή ομάδα
# Δημιουργία ηλικιακών ομάδων
bins = [20, 30, 40, 50]
labels = ['18-30', '31-45', '46-100']
df['Ηλικιακή_Ομάδα'] = pd.cut(df['Ηλικία'], bins=bins, labels=labels)

# Υπολογισμός μέσου όρου πωλήσεων ανά ηλικιακή ομάδα
print(df.groupby('Ηλικιακή_Ομάδα')['Ποσότητα'].mean())

print(df)

