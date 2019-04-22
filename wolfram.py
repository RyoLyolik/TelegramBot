import wolframalpha
client = wolframalpha.Client('APQHJJ-U3R9WKWHU')

res = client.query('plot y=x^2')
print(res['pod'][1]['subpod']['plaintext'])
# print(eval(res['pod'][1]['subpod']['plaintext'][4:]))
print(res)
